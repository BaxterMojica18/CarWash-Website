from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import is_admin_or_owner
from app.demo_limits import DemoLimits

router = APIRouter()

@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(reservation_data: schemas.ReservationCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    DemoLimits.check_limit(db, current_user, "reservations")
    reservation = crud.create_reservation(
        db, 
        current_user.id, 
        reservation_data.service_id, 
        reservation_data.location_id, 
        reservation_data.vehicle_plate
    )
    if not reservation:
        raise HTTPException(status_code=400, detail="Invalid service or service not found")
    DemoLimits.increment_usage(db, current_user, "reservations")
    return reservation

@router.get("/", response_model=List[schemas.ReservationResponse])
def get_reservations(location_id: int = None, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    if "admin" in role_names or "owner" in role_names:
        return crud.get_reservations(db, location_id=location_id)
    return crud.get_reservations(db, current_user.id)

@router.get("/queue", response_model=List[schemas.ReservationResponse])
def get_queue(location_id: int, db: Session = Depends(database.get_db), current_user = Depends(is_admin_or_owner)):
    return crud.get_queue(db, location_id)

@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    reservation = crud.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    role_names = [role.name for role in current_user.roles]
    if reservation.client_id != current_user.id and "admin" not in role_names and "owner" not in role_names:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return reservation

@router.patch("/{reservation_id}/status", response_model=schemas.ReservationResponse)
def update_reservation_status(reservation_id: int, status_data: schemas.ReservationStatusUpdate, db: Session = Depends(database.get_db), current_user = Depends(is_admin_or_owner)):
    reservation = crud.update_reservation_status(db, reservation_id, status_data.status)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
