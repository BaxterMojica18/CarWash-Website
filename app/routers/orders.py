from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission, is_admin_or_owner
from app.demo_limits import DemoLimits

router = APIRouter()

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    DemoLimits.check_limit(db, current_user, "orders")
    order = crud.create_order_from_cart(db, current_user.id, order_data.payment_method)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    DemoLimits.increment_usage(db, current_user, "orders")
    return order

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    if "admin" in role_names or "owner" in role_names:
        return crud.get_orders(db)
    return crud.get_orders(db, current_user.id)

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    role_names = [role.name for role in current_user.roles]
    if order.client_id != current_user.id and "admin" not in role_names and "owner" not in role_names:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order

@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_data: schemas.OrderStatusUpdate, db: Session = Depends(database.get_db), current_user = Depends(is_admin_or_owner)):
    order = crud.update_order_status(db, order_id, status_data.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
