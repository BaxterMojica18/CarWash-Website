"""
Notifications API — CRUD for user notifications and preferences.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app import database
from app.dependencies import get_current_user
from app.notification_service import get_or_create_preferences

router = APIRouter()


class NotificationPreferenceUpdate(BaseModel):
    order_notifications: Optional[bool] = None
    reservation_notifications: Optional[bool] = None
    payment_notifications: Optional[bool] = None
    coupon_notifications: Optional[bool] = None
    flash_sale_notifications: Optional[bool] = None
    permission_notifications: Optional[bool] = None


@router.get("/")
def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """
    Paginated list of notifications for the current user.
    Excludes soft-deleted notifications. Includes unread_count.
    """
    # Base query: user's non-deleted notifications
    query = db.query(database.Notification).filter(
        database.Notification.user_id == current_user.id,
        database.Notification.deleted_at == None,
    )

    # Unread count
    unread_count = query.filter(database.Notification.is_read == False).count()

    # Re-create base query for total and pagination (unread filter consumed it)
    base_query = db.query(database.Notification).filter(
        database.Notification.user_id == current_user.id,
        database.Notification.deleted_at == None,
    )

    total = base_query.count()

    # Paginate
    offset = (page - 1) * page_size
    notifications = (
        base_query.order_by(database.Notification.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": n.is_read,
                "link": n.link,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in notifications
        ],
        "unread_count": unread_count,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Mark a single notification as read. Verifies ownership."""
    notification = (
        db.query(database.Notification)
        .filter(database.Notification.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this notification"
        )

    notification.is_read = True
    db.commit()

    return {"message": "Notification marked as read"}


@router.patch("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Mark all unread notifications as read for the current user."""
    db.query(database.Notification).filter(
        database.Notification.user_id == current_user.id,
        database.Notification.is_read == False,
        database.Notification.deleted_at == None,
    ).update({"is_read": True})
    db.commit()

    return {"message": "All notifications marked as read"}


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Soft-delete a notification. Verifies ownership."""
    notification = (
        db.query(database.Notification)
        .filter(database.Notification.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this notification"
        )

    notification.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Notification deleted"}


@router.get("/preferences")
def get_notification_preferences(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Return current user's notification preferences. Lazy-creates if missing."""
    prefs = get_or_create_preferences(db, current_user.id)

    if prefs is None:
        raise HTTPException(
            status_code=500, detail="Failed to load notification preferences"
        )

    return {
        "order_notifications": prefs.order_notifications,
        "reservation_notifications": prefs.reservation_notifications,
        "payment_notifications": prefs.payment_notifications,
        "coupon_notifications": prefs.coupon_notifications,
        "flash_sale_notifications": prefs.flash_sale_notifications,
        "permission_notifications": prefs.permission_notifications,
    }


@router.put("/preferences")
def update_notification_preferences(
    prefs_update: NotificationPreferenceUpdate,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Update current user's notification preferences."""
    prefs = get_or_create_preferences(db, current_user.id)

    if prefs is None:
        raise HTTPException(
            status_code=500, detail="Failed to load notification preferences"
        )

    # Update only provided fields
    update_data = prefs_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prefs, field, value)

    db.commit()
    db.refresh(prefs)

    return {
        "message": "Notification preferences updated",
        "order_notifications": prefs.order_notifications,
        "reservation_notifications": prefs.reservation_notifications,
        "payment_notifications": prefs.payment_notifications,
        "coupon_notifications": prefs.coupon_notifications,
        "flash_sale_notifications": prefs.flash_sale_notifications,
        "permission_notifications": prefs.permission_notifications,
    }
