"""
Notification service module for creating and managing notifications.

All functions use try/except to never block the calling operation on failure.
"""

import logging
from sqlalchemy.orm import Session
from app.database import Notification, NotificationPreference, User

logger = logging.getLogger(__name__)


def get_or_create_preferences(db: Session, user_id: int) -> NotificationPreference:
    """
    Returns existing notification preferences for a user, or creates a new
    record with all defaults set to True (lazy initialization).

    Returns None only if both lookup and creation fail.
    """
    try:
        prefs = (
            db.query(NotificationPreference)
            .filter(NotificationPreference.user_id == user_id)
            .first()
        )
        if prefs:
            return prefs

        # Create with all defaults True (SQLAlchemy column defaults handle this)
        prefs = NotificationPreference(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
        return prefs
    except Exception as e:
        logger.error(
            f"Failed to get/create notification preferences for user {user_id}: {e}"
        )
        try:
            db.rollback()
        except Exception:
            pass
        return None


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str,
    link: str = None,
) -> Notification | None:
    """
    Create a notification for a user after checking their preferences.

    Returns None if:
    - The user has disabled this notification type
    - An error occurs during creation

    Never raises exceptions that would block the calling operation.
    """
    try:
        # Check user preferences before creating
        prefs = get_or_create_preferences(db, user_id)
        if prefs is not None:
            type_field = f"{notification_type}_notifications"
            if hasattr(prefs, type_field) and not getattr(prefs, type_field):
                return None  # User disabled this type

        # Create notification
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            link=link,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    except Exception as e:
        logger.error(f"Failed to create notification for user {user_id}: {e}")
        try:
            db.rollback()
        except Exception:
            pass
        return None


def notify_business_admins(
    db: Session,
    business_number: str,
    title: str,
    message: str,
    notification_type: str,
    link: str = None,
) -> list:
    """
    Send a notification to all admin/owner/superadmin users in a business.

    Queries all users with account_type in ('admin', 'owner', 'superadmin')
    for the given business_number, then calls create_notification for each.

    Returns a list of created notifications (may contain None entries for
    users who have disabled the notification type or where creation failed).

    Never raises exceptions that would block the calling operation.
    """
    try:
        admins = (
            db.query(User)
            .filter(
                User.business_number == business_number,
                User.account_type.in_(["admin", "owner", "superadmin"]),
                User.is_active == True,
                User.deleted_at == None,
            )
            .all()
        )

        results = []
        for admin in admins:
            result = create_notification(
                db, admin.id, title, message, notification_type, link
            )
            results.append(result)
        return results
    except Exception as e:
        logger.error(
            f"Failed to notify business admins for business {business_number}: {e}"
        )
        try:
            db.rollback()
        except Exception:
            pass
        return []
