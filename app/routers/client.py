from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=schemas.ClientDashboard)
def get_client_dashboard(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    orders = crud.get_orders(db, current_user.id)
    reservations = crud.get_reservations(db, current_user.id)
    
    active_orders = [o for o in orders if o.status not in ['completed', 'cancelled']]
    order_history = [o for o in orders if o.status in ['completed', 'cancelled']]
    
    active_reservations = [r for r in reservations if r.status not in ['completed', 'cancelled']]
    reservation_history = [r for r in reservations if r.status in ['completed', 'cancelled']]
    
    return {
        "active_orders": active_orders,
        "order_history": order_history,
        "active_reservations": active_reservations,
        "reservation_history": reservation_history
    }
