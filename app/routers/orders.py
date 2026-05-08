from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission, is_admin_or_owner
from app.demo_limits import DemoLimits
from app.crud import get_business_user_ids
from app.audit import log_audit, get_client_ip
from app.notification_service import create_notification, notify_business_admins
from app.email_service import (
    send_order_confirmation_client,
    send_order_notification_owner,
    send_order_status_update,
    DEMO_NOTIFICATION_EMAIL,
)
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


def _order_items_payload(order):
    return [
        {
            "name": item.product_service.name if item.product_service else "Item",
            "quantity": item.quantity,
            "subtotal": item.subtotal,
        }
        for item in (order.items or [])
    ]


@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order_data: schemas.OrderCreate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    DemoLimits.check_limit(db, current_user, "orders")
    order = crud.create_order_from_cart(db, current_user.id, order_data.payment_method)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    DemoLimits.increment_usage(db, current_user, "orders")
    items = _order_items_payload(order)
    owner_email = _get_owner_email(db, current_user) or DEMO_NOTIFICATION_EMAIL
    threading.Thread(
        target=send_order_confirmation_client,
        args=(
            current_user.email,
            order.order_number,
            items,
            order.total_amount,
            order.payment_method,
        ),
        daemon=True,
    ).start()
    threading.Thread(
        target=send_order_notification_owner,
        args=(
            owner_email,
            order.order_number,
            current_user.email,
            items,
            order.total_amount,
            order.payment_method,
        ),
        daemon=True,
    ).start()
    log_audit(
        db,
        current_user.id,
        "create",
        "order",
        order.id,
        {"order_number": order.order_number, "total": order.total_amount},
        get_client_ip(request),
    )
    notify_business_admins(
        db,
        current_user.business_number,
        "New Order Placed",
        f"Order #{order.order_number} has been placed",
        "order",
    )
    return order


@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(database.get_db), current_user=Depends(get_current_user)
):
    role_names = [role.name for role in current_user.roles]
    if "admin" in role_names or "owner" in role_names or "superadmin" in role_names:
        # Scope to business: only show orders from users in the same business
        biz_ids = get_business_user_ids(db, current_user)
        orders = (
            db.query(database.Order)
            .filter(database.Order.client_id.in_(biz_ids))
            .order_by(database.Order.created_at.desc())
            .all()
        )
        return orders
    return crud.get_orders(db, current_user.id)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    role_names = [role.name for role in current_user.roles]
    if (
        order.client_id != current_user.id
        and "admin" not in role_names
        and "owner" not in role_names
        and "superadmin" not in role_names
    ):
        raise HTTPException(status_code=403, detail="Access denied")

    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status_data: schemas.OrderStatusUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_admin_or_owner),
):
    order = crud.update_order_status(db, order_id, status_data.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    client = db.query(database.User).filter(database.User.id == order.client_id).first()
    if client:
        threading.Thread(
            target=send_order_status_update,
            args=(client.email, order.order_number, status_data.status),
            daemon=True,
        ).start()
    log_audit(
        db,
        current_user.id,
        "update",
        "order",
        order_id,
        {"status": status_data.status},
        get_client_ip(request),
    )
    create_notification(
        db,
        order.client_id,
        "Order Status Updated",
        f"Your order #{order.order_number} status changed to {status_data.status}",
        "order",
    )
    return order
