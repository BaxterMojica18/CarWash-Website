from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, crud
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/complete")
def complete_onboarding(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Mark onboarding as completed for the current user. Idempotent."""
    if current_user.onboarding_completed:
        return {"message": "Already completed"}

    crud.mark_onboarding_completed(db, current_user.id)
    return {"message": "Onboarding completed successfully"}


@router.get("/status")
def get_onboarding_status(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Get onboarding completion status for the current user."""
    completed = crud.get_onboarding_status(db, current_user.id)
    return {"onboarding_completed": completed}
