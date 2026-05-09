from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import database
from datetime import datetime
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(database.User).filter(database.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def check_subscription_active(
    current_user: database.User = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    """Dependency that blocks write operations when subscription is expired."""
    if not current_user.business_number:
        return current_user  # No business = allow (pre-onboarding)

    subscription = (
        db.query(database.Subscription)
        .filter(database.Subscription.business_number == current_user.business_number)
        .first()
    )

    if subscription is None:
        return current_user  # No subscription record = allow (pre-onboarding state)

    if subscription.status == "active":
        return current_user

    if subscription.status == "trial":
        if (
            subscription.trial_end_date
            and datetime.utcnow() < subscription.trial_end_date
        ):
            return current_user
        # Trial expired — update status
        subscription.status = "expired"
        subscription.updated_at = datetime.utcnow()
        db.commit()

    # Expired or cancelled
    raise HTTPException(
        status_code=403,
        detail="Subscription required. Please subscribe to continue.",
        headers={"X-Subscription-Required": "true"},
    )
