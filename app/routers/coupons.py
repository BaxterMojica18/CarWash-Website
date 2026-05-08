from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import database
from app.routers.auth import get_current_user, is_admin_or_owner
from app.audit import log_audit, get_client_ip
from app.notification_service import notify_business_admins
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# ── Schemas ────────────────────────────────────────────────────────────────────


class CouponCreate(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str = "percentage"  # "percentage" or "fixed"
    discount_value: float
    min_spend: float = 0
    max_uses: Optional[int] = None
    stock: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True


class CouponUpdate(BaseModel):
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_spend: Optional[float] = None
    max_uses: Optional[int] = None
    stock: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class CouponValidate(BaseModel):
    code: str
    cart_total: float = 0


# ── Helper ─────────────────────────────────────────────────────────────────────


def coupon_to_dict(c: database.Coupon) -> dict:
    return {
        "id": c.id,
        "code": c.code,
        "description": c.description,
        "discount_type": c.discount_type,
        "discount_value": c.discount_value,
        "min_spend": c.min_spend,
        "max_uses": c.max_uses,
        "uses_count": c.uses_count,
        "stock": c.stock,
        "expires_at": c.expires_at.isoformat() if c.expires_at else None,
        "is_active": c.is_active,
        "business_number": c.business_number,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "deleted_at": c.deleted_at.isoformat() if c.deleted_at else None,
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("/coupons")
def list_coupons(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """List active (non-deleted) coupons for the current business.
    - Owners/admins see all; clients see only active + not-expired ones."""
    biz = current_user.business_number
    query = db.query(database.Coupon).filter(database.Coupon.deleted_at == None)
    if biz:
        query = query.filter(
            (database.Coupon.business_number == biz)
            | (database.Coupon.business_number == None)
        )

    user_roles = [r.name for r in current_user.roles]
    is_manager = any(r in user_roles for r in ("owner", "admin", "superadmin"))

    coupons = query.all()

    if not is_manager:
        # Filter for clients: only show active, unexpired, in-stock coupons
        now = datetime.utcnow()
        coupons = [
            c
            for c in coupons
            if c.is_active
            and (c.expires_at is None or c.expires_at > now)
            and (c.stock is None or c.stock > 0)
        ]

    return [coupon_to_dict(c) for c in coupons]


@router.post("/coupons")
def create_coupon(
    data: CouponCreate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    existing = (
        db.query(database.Coupon)
        .filter(
            database.Coupon.code == data.code.upper(),
            database.Coupon.deleted_at == None,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")

    coupon = database.Coupon(
        code=data.code.upper().strip(),
        description=data.description,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
        min_spend=data.min_spend,
        max_uses=data.max_uses,
        stock=data.stock,
        expires_at=data.expires_at,
        is_active=data.is_active,
        business_number=current_user.business_number,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    log_audit(
        db,
        current_user.id,
        "create",
        "coupon",
        coupon.id,
        {"code": coupon.code},
        get_client_ip(request),
    )
    return coupon_to_dict(coupon)


@router.put("/coupons/{coupon_id}")
def update_coupon(
    coupon_id: int,
    data: CouponUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    coupon = (
        db.query(database.Coupon)
        .filter(database.Coupon.id == coupon_id, database.Coupon.deleted_at == None)
        .first()
    )
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    if data.description is not None:
        coupon.description = data.description
    if data.discount_type is not None:
        coupon.discount_type = data.discount_type
    if data.discount_value is not None:
        coupon.discount_value = data.discount_value
    if data.min_spend is not None:
        coupon.min_spend = data.min_spend
    if data.max_uses is not None:
        coupon.max_uses = data.max_uses
    if data.stock is not None:
        coupon.stock = data.stock
    if data.expires_at is not None:
        coupon.expires_at = data.expires_at
    if data.is_active is not None:
        coupon.is_active = data.is_active

    db.commit()
    db.refresh(coupon)
    log_audit(
        db,
        current_user.id,
        "update",
        "coupon",
        coupon_id,
        {"code": coupon.code},
        get_client_ip(request),
    )
    return coupon_to_dict(coupon)


@router.delete("/coupons/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    """Soft delete — sets deleted_at timestamp and deactivates."""
    coupon = (
        db.query(database.Coupon)
        .filter(database.Coupon.id == coupon_id, database.Coupon.deleted_at == None)
        .first()
    )
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    coupon.deleted_at = datetime.utcnow()
    coupon.is_active = False
    db.commit()
    log_audit(
        db,
        current_user.id,
        "delete",
        "coupon",
        coupon_id,
        {"code": coupon.code},
        get_client_ip(request),
    )
    return {"message": "Coupon deleted", "id": coupon_id}


@router.post("/coupons/validate")
def validate_coupon(
    data: CouponValidate,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Validate a coupon code and return the discount amount."""
    now = datetime.utcnow()
    coupon = (
        db.query(database.Coupon)
        .filter(
            database.Coupon.code == data.code.upper().strip(),
            database.Coupon.deleted_at == None,
            database.Coupon.is_active == True,
        )
        .first()
    )

    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid or expired coupon code")

    if coupon.expires_at and coupon.expires_at < now:
        raise HTTPException(status_code=400, detail="This coupon has expired")

    if coupon.stock is not None and coupon.stock <= 0:
        raise HTTPException(status_code=400, detail="This coupon is out of stock")

    if coupon.max_uses is not None and coupon.uses_count >= coupon.max_uses:
        raise HTTPException(
            status_code=400, detail="This coupon has reached its usage limit"
        )

    if data.cart_total < coupon.min_spend:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum spend of ₱{coupon.min_spend:.2f} required for this coupon",
        )

    # Calculate discount
    if coupon.discount_type == "percentage":
        discount_amount = round(data.cart_total * (coupon.discount_value / 100), 2)
    else:  # fixed
        discount_amount = min(coupon.discount_value, data.cart_total)

    # Notify business admins that a coupon was applied
    if current_user.business_number:
        notify_business_admins(
            db,
            current_user.business_number,
            "Coupon Applied",
            f"Coupon '{coupon.code}' was used",
            "coupon",
        )

    return {
        "valid": True,
        "code": coupon.code,
        "description": coupon.description,
        "discount_type": coupon.discount_type,
        "discount_value": coupon.discount_value,
        "discount_amount": discount_amount,
        "stock": coupon.stock,
        "expires_at": coupon.expires_at.isoformat() if coupon.expires_at else None,
    }
