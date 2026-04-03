from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission

router = APIRouter()

@router.get("/", response_model=List[schemas.CartItemResponse])
def get_cart(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_cart_items(db, current_user.id)

@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    cart_item = crud.add_to_cart(db, current_user.id, item.product_service_id, item.quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return cart_item

@router.patch("/{item_id}", response_model=schemas.CartItemResponse)
def update_cart_item(item_id: int, item: schemas.CartItemUpdate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    cart_item = crud.update_cart_item(db, item_id, current_user.id, item.quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item

@router.delete("/{item_id}")
def remove_cart_item(item_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    cart_item = crud.remove_cart_item(db, item_id, current_user.id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@router.delete("/clear/all")
def clear_cart(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    crud.clear_cart(db, current_user.id)
    return {"message": "Cart cleared"}
