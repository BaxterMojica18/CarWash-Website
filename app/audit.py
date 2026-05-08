"""
Audit logging utility for tracking user actions across the system.
"""

import json
import logging
from sqlalchemy.orm import Session
from fastapi import Request
from app.database import AuditLog

logger = logging.getLogger(__name__)


def log_audit(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int = None,
    details: dict = None,
    ip_address: str = None,
):
    """
    Record an audit log entry. Wraps the INSERT in try/except so audit
    failures never break the main request flow.
    """
    try:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
        )
        db.add(entry)
        db.commit()
    except Exception as e:
        logger.error(f"Audit log failed: {e}")
        try:
            db.rollback()
        except Exception:
            pass


def get_client_ip(request: Request) -> str:
    """
    Extract the client IP from the request. Checks X-Forwarded-For first
    (common behind reverse proxies like Render/Vercel), then falls back
    to the direct client host.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can be a comma-separated list; first is the real client
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"
