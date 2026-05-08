from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import is_admin_or_owner
from app.demo_limits import DemoLimits
from app.crud import get_business_user_ids
from app.audit import log_audit, get_client_ip
from app.email_service import (
    send_reservation_confirmation_client,
    send_reservation_notification_owner,
    send_reservation_status_update,
    DEMO_NOTIFICATION_EMAIL,
)
from app.notification_service import create_notification
import threading

router = APIRouter()


def _get_owner_email(db, current_user):
    if current_user.business_number:
        owner = (
            db.query(database.User)
            .filter(
                database.User.business_number == current_user.business_number,
                database.User.account_type == "owner",
            )
            .first()
        )
        return owner.email if owner else None
    return None


@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation_data: schemas.ReservationCreate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    DemoLimits.check_limit(db, current_user, "reservations")
    reservation = crud.create_reservation(
        db,
        current_user.id,
        reservation_data.service_id,
        reservation_data.location_id,
        reservation_data.vehicle_plate,
    )
    if not reservation:
        raise HTTPException(
            status_code=400, detail="Invalid service or service not found"
        )
    DemoLimits.increment_usage(db, current_user, "reservations")
    owner_email = _get_owner_email(db, current_user) or DEMO_NOTIFICATION_EMAIL
    threading.Thread(
        target=send_reservation_confirmation_client,
        args=(
            current_user.email,
            reservation.reservation_number,
            reservation.service.name,
            reservation.location.name,
            reservation.vehicle_plate,
            reservation.queue_position or 0,
        ),
        daemon=True,
    ).start()
    threading.Thread(
        target=send_reservation_notification_owner,
        args=(
            owner_email,
            reservation.reservation_number,
            current_user.email,
            reservation.service.name,
            reservation.location.name,
            reservation.vehicle_plate,
            reservation.queue_position or 0,
        ),
        daemon=True,
    ).start()
    log_audit(
        db,
        current_user.id,
        "create",
        "reservation",
        reservation.id,
        {
            "reservation_number": reservation.reservation_number,
            "vehicle_plate": reservation_data.vehicle_plate,
        },
        get_client_ip(request),
    )
    return reservation


@router.get("/", response_model=List[schemas.ReservationResponse])
def get_reservations(
    location_id: int = None,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    role_names = [role.name for role in current_user.roles]
    if "admin" in role_names or "owner" in role_names or "superadmin" in role_names:
        # Scope to business: only show reservations from users in the same business
        biz_ids = get_business_user_ids(db, current_user)
        from sqlalchemy.orm import joinedload

        query = (
            db.query(database.Reservation)
            .options(
                joinedload(database.Reservation.service),
                joinedload(database.Reservation.location),
            )
            .filter(database.Reservation.client_id.in_(biz_ids))
        )
        if location_id:
            query = query.filter(database.Reservation.location_id == location_id)
        return query.order_by(database.Reservation.created_at.desc()).all()
    return crud.get_reservations(db, current_user.id)


@router.get("/queue", response_model=List[schemas.ReservationResponse])
def get_queue(
    location_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_admin_or_owner),
):
    return crud.get_queue(db, location_id)


@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    reservation = crud.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    role_names = [role.name for role in current_user.roles]
    if (
        reservation.client_id != current_user.id
        and "admin" not in role_names
        and "owner" not in role_names
        and "superadmin" not in role_names
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    return reservation


@router.patch("/{reservation_id}/status", response_model=schemas.ReservationResponse)
def update_reservation_status(
    reservation_id: int,
    status_data: schemas.ReservationStatusUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_admin_or_owner),
):
    reservation = crud.update_reservation_status(db, reservation_id, status_data.status)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    client = (
        db.query(database.User)
        .filter(database.User.id == reservation.client_id)
        .first()
    )
    if client:
        threading.Thread(
            target=send_reservation_status_update,
            args=(client.email, reservation.reservation_number, status_data.status),
            daemon=True,
        ).start()
    log_audit(
        db,
        current_user.id,
        "update",
        "reservation",
        reservation_id,
        {"status": status_data.status},
        get_client_ip(request),
    )
    create_notification(
        db,
        reservation.client_id,
        "Reservation Status Updated",
        f"Your reservation #{reservation.reservation_number} status changed to {status_data.status}",
        "reservation",
    )
    return reservation
