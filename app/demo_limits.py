"""
Demo account usage limits enforcement
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import User

class DemoLimits:
    @staticmethod
    def check_limit(db: Session, user: User, limit_type: str):
        """Check if user has reached their limit"""
        if not user.is_demo:
            return True
        
        result = db.execute(
            text("SELECT * FROM demo_usage_limits WHERE user_id = :uid"),
            {"uid": user.id}
        ).fetchone()
        
        if not result:
            return True
        
        limits = {
            "products": (result[1], result[5]),  # (created, max)
            "services": (result[2], result[6]),
            "orders": (result[3], result[7]),
            "reservations": (result[4], result[8])
        }
        
        if limit_type in limits:
            created, max_allowed = limits[limit_type]
            if created >= max_allowed:
                raise HTTPException(
                    status_code=403,
                    detail=f"Demo account limit reached: Maximum {max_allowed} {limit_type} allowed"
                )
        
        return True
    
    @staticmethod
    def increment_usage(db: Session, user: User, limit_type: str):
        """Increment usage counter for demo user"""
        if not user.is_demo:
            return
        
        column_map = {
            "products": "products_created",
            "services": "services_created",
            "orders": "orders_created",
            "reservations": "reservations_created"
        }
        
        if limit_type in column_map:
            db.execute(text(f"""
                UPDATE demo_usage_limits 
                SET {column_map[limit_type]} = {column_map[limit_type]} + 1
                WHERE user_id = :uid
            """), {"uid": user.id})
            db.commit()
    
    @staticmethod
    def get_usage_stats(db: Session, user: User):
        """Get current usage statistics for demo user"""
        if not user.is_demo:
            return None
        
        result = db.execute(
            text("SELECT * FROM demo_usage_limits WHERE user_id = :uid"),
            {"uid": user.id}
        ).fetchone()
        
        if not result:
            return None
        
        return {
            "products": {"used": result[1], "max": result[5]},
            "services": {"used": result[2], "max": result[6]},
            "orders": {"used": result[3], "max": result[7]},
            "reservations": {"used": result[4], "max": result[8]}
        }
