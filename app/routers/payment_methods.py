from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db, PaymentMethod
from app.dependencies import get_current_user
from app.permissions import is_admin_or_owner
from pydantic import BaseModel
from datetime import datetime
import base64
import os

router = APIRouter()

class PaymentMethodCreate(BaseModel):
    name: str
    icon: str = None
    account_number: str = None
    is_active: bool = True

class PaymentMethodResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None
    qr_image: Optional[str] = None
    account_number: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(PaymentMethod).filter(PaymentMethod.is_active == True).all()

@router.post("/", response_model=PaymentMethodResponse)
def create_payment_method(payment: PaymentMethodCreate, db: Session = Depends(get_db), current_user = Depends(is_admin_or_owner)):
    pm = PaymentMethod(name=payment.name, icon=payment.icon, account_number=payment.account_number, is_active=payment.is_active, created_at=datetime.now())
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm

@router.put("/{payment_id}", response_model=PaymentMethodResponse)
async def update_payment_method(
    payment_id: int,
    name: str = Form(...),
    icon: str = Form(None),
    account_number: str = Form(None),
    is_active: bool = Form(True),
    qr_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(is_admin_or_owner)
):
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == payment_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    pm.name = name
    pm.icon = icon
    pm.account_number = account_number
    pm.is_active = is_active
    
    if qr_image:
        contents = await qr_image.read()
        pm.qr_image = base64.b64encode(contents).decode('utf-8')
    
    db.commit()
    db.refresh(pm)
    return pm

@router.delete("/{payment_id}")
def delete_payment_method(payment_id: int, db: Session = Depends(get_db), current_user = Depends(is_admin_or_owner)):
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == payment_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Payment method not found")
    pm.is_active = False
    db.commit()
    return {"message": "Payment method deactivated"}
