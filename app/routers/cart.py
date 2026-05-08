from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission, is_client
from app.audit import log_audit, get_client_ip

router = APIRouter()


@router.get("/", response_model=List[schemas.CartItemResponse])
def get_cart(db: Session = Depends(database.get_db), current_user=Depends(is_client)):
    return crud.get_cart_items(db, current_user.id)


@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(
    item: schemas.CartItemCreate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_client),
):
    cart_item = crud.add_to_cart(
        db, current_user.id, item.product_service_id, item.quantity
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found")
    log_audit(
        db,
        current_user.id,
        "create",
        "cart_item",
        cart_item.id,
        {"product_service_id": item.product_service_id, "quantity": item.quantity},
        get_client_ip(request),
    )
    return cart_item


@router.patch("/{item_id}", response_model=schemas.CartItemResponse)
def update_cart_item(
    item_id: int,
    item: schemas.CartItemUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_client),
):
    cart_item = crud.update_cart_item(db, item_id, current_user.id, item.quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    log_audit(
        db,
        current_user.id,
        "update",
        "cart_item",
        item_id,
        {"quantity": item.quantity},
        get_client_ip(request),
    )
    return cart_item


@router.delete("/{item_id}")
def remove_cart_item(
    item_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_client),
):
    cart_item = crud.remove_cart_item(db, item_id, current_user.id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    log_audit(
        db,
        current_user.id,
        "delete",
        "cart_item",
        item_id,
        None,
        get_client_ip(request),
    )
    return {"message": "Item removed from cart"}


@router.delete("/clear/all")
def clear_cart(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user=Depends(is_client),
):
    crud.clear_cart(db, current_user.id)
    log_audit(
        db,
        current_user.id,
        "delete",
        "cart_item",
        None,
        {"action": "clear_all"},
        get_client_ip(request),
    )
    return {"message": "Cart cleared"}
