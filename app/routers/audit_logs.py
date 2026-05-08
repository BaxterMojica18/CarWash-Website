"""
Audit Logs API — view audit trail scoped by business.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app import database
from app.dependencies import get_current_user
from app.permissions import is_admin_or_owner

router = APIRouter()


@router.get("/")
def get_audit_logs(
    user_filter: Optional[int] = Query(None),
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    """
    List audit log entries scoped to the current user's business.
    Only admins/owners can access this endpoint.
    """
    # Base query: join audit_logs with users to scope by business_number
    query = db.query(database.AuditLog).join(
        database.User, database.AuditLog.user_id == database.User.id
    )

    # Multi-tenant scoping
    if current_user.business_number:
        query = query.filter(
            database.User.business_number == current_user.business_number
        )

    # Filters
    if user_filter is not None:
        query = query.filter(database.AuditLog.user_id == user_filter)
    if action:
        query = query.filter(database.AuditLog.action == action)
    if resource_type:
        query = query.filter(database.AuditLog.resource_type == resource_type)
    if date_from:
        query = query.filter(database.AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(database.AuditLog.created_at <= date_to)

    # Total count for pagination
    total = query.count()

    # Paginate
    offset = (page - 1) * page_size
    entries = (
        query.order_by(database.AuditLog.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "entries": [
            {
                "id": e.id,
                "user_id": e.user_id,
                "user_email": e.user.email if e.user else None,
                "action": e.action,
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "details": e.details,
                "ip_address": e.ip_address,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in entries
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
