from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import database
from app.routers.auth import get_current_user, is_admin_or_owner
from app.audit import log_audit, get_client_ip
from app.notification_service import create_notification
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()


# ── Helpers ────────────────────────────────────────────────────────────────────


def _notify_active_business_users(
    db: Session, business_number: str, title: str, message: str
):
    """Notify all active users in the business about a flash sale."""
    try:
        active_users = (
            db.query(database.User)
            .filter(
                database.User.business_number == business_number,
                database.User.is_active == True,
                database.User.deleted_at == None,
            )
            .all()
        )
        for user in active_users:
            create_notification(db, user.id, title, message, "flash_sale")
    except Exception:
        pass  # Never block the calling operation


# ── Schemas ────────────────────────────────────────────────────────────────────


class FlashSaleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    discount_type: str = "percentage"
    discount_value: float
    starts_at: datetime
    ends_at: datetime
    is_active: bool = True
    product_ids: List[int] = []


class FlashSaleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    product_ids: Optional[List[int]] = None


# ── Helper ─────────────────────────────────────────────────────────────────────


def flash_sale_to_dict(fs: database.FlashSale) -> dict:
    return {
        "id": fs.id,
        "title": fs.title,
        "description": fs.description,
        "discount_type": fs.discount_type,
        "discount_value": fs.discount_value,
        "starts_at": fs.starts_at.isoformat() if fs.starts_at else None,
        "ends_at": fs.ends_at.isoformat() if fs.ends_at else None,
        "is_active": fs.is_active,
        "business_number": fs.business_number,
        "created_at": fs.created_at.isoformat() if fs.created_at else None,
        "deleted_at": fs.deleted_at.isoformat() if fs.deleted_at else None,
        "product_ids": [item.product_service_id for item in fs.items],
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("/flash-sales")
def list_flash_sales(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    biz = current_user.business_number
    user_roles = [r.name for r in current_user.roles]
    is_manager = any(r in user_roles for r in ("owner", "admin", "superadmin"))

    query = db.query(database.FlashSale).filter(database.FlashSale.deleted_at == None)
    if biz:
        query = query.filter(
            (database.FlashSale.business_number == biz)
            | (database.FlashSale.business_number == None)
        )

    sales = query.order_by(database.FlashSale.starts_at.desc()).all()

    if not is_manager:
        now = datetime.utcnow()
        sales = [s for s in sales if s.is_active and s.starts_at <= now <= s.ends_at]

    return [flash_sale_to_dict(s) for s in sales]


@router.post("/flash-sales")
def create_flash_sale(
    data: FlashSaleCreate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    if data.ends_at <= data.starts_at:
        raise HTTPException(status_code=400, detail="ends_at must be after starts_at")

    fs = database.FlashSale(
        title=data.title,
        description=data.description,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
        is_active=data.is_active,
        business_number=current_user.business_number,
    )
    db.add(fs)
    db.flush()

    for pid in data.product_ids:
        db.add(database.FlashSaleItem(flash_sale_id=fs.id, product_service_id=pid))

    db.commit()
    db.refresh(fs)
    log_audit(
        db,
        current_user.id,
        "create",
        "flash_sale",
        fs.id,
        {"title": data.title},
        get_client_ip(request),
    )

    # Notify all active business users about the new flash sale
    if current_user.business_number and fs.is_active:
        _notify_active_business_users(
            db,
            current_user.business_number,
            "New Flash Sale",
            f"Flash sale '{fs.title}' is now active!",
        )

    return flash_sale_to_dict(fs)


@router.put("/flash-sales/{sale_id}")
def update_flash_sale(
    sale_id: int,
    data: FlashSaleUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    fs = (
        db.query(database.FlashSale)
        .filter(database.FlashSale.id == sale_id, database.FlashSale.deleted_at == None)
        .first()
    )
    if not fs:
        raise HTTPException(status_code=404, detail="Flash sale not found")

    if data.title is not None:
        fs.title = data.title
    if data.description is not None:
        fs.description = data.description
    if data.discount_type is not None:
        fs.discount_type = data.discount_type
    if data.discount_value is not None:
        fs.discount_value = data.discount_value
    if data.starts_at is not None:
        fs.starts_at = data.starts_at
    if data.ends_at is not None:
        fs.ends_at = data.ends_at
    if data.is_active is not None:
        fs.is_active = data.is_active

    if data.product_ids is not None:
        db.query(database.FlashSaleItem).filter(
            database.FlashSaleItem.flash_sale_id == sale_id
        ).delete()
        for pid in data.product_ids:
            db.add(
                database.FlashSaleItem(flash_sale_id=sale_id, product_service_id=pid)
            )

    db.commit()
    db.refresh(fs)
    log_audit(
        db,
        current_user.id,
        "update",
        "flash_sale",
        sale_id,
        {"title": fs.title},
        get_client_ip(request),
    )
    return flash_sale_to_dict(fs)


@router.patch("/flash-sales/{sale_id}/toggle")
def toggle_flash_sale(
    sale_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    fs = (
        db.query(database.FlashSale)
        .filter(database.FlashSale.id == sale_id, database.FlashSale.deleted_at == None)
        .first()
    )
    if not fs:
        raise HTTPException(status_code=404, detail="Flash sale not found")
    fs.is_active = not fs.is_active
    db.commit()
    log_audit(
        db,
        current_user.id,
        "update",
        "flash_sale",
        sale_id,
        {"is_active": fs.is_active},
        get_client_ip(request),
    )

    # Notify all active business users when flash sale is activated
    if fs.is_active and current_user.business_number:
        _notify_active_business_users(
            db,
            current_user.business_number,
            "Flash Sale Activated",
            f"Flash sale '{fs.title}' is now active!",
        )

    return {"id": sale_id, "is_active": fs.is_active}


@router.delete("/flash-sales/{sale_id}")
def delete_flash_sale(
    sale_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    fs = (
        db.query(database.FlashSale)
        .filter(database.FlashSale.id == sale_id, database.FlashSale.deleted_at == None)
        .first()
    )
    if not fs:
        raise HTTPException(status_code=404, detail="Flash sale not found")
    fs.deleted_at = datetime.utcnow()
    fs.is_active = False
    db.commit()
    log_audit(
        db,
        current_user.id,
        "delete",
        "flash_sale",
        sale_id,
        {"title": fs.title},
        get_client_ip(request),
    )
    return {"message": "Flash sale deleted", "id": sale_id}
