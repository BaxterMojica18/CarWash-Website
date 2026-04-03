from app.database import SessionLocal, PaymentMethod
from datetime import datetime

def seed_payment_methods():
    db = SessionLocal()
    try:
        # Check if payment methods already exist
        existing = db.query(PaymentMethod).first()
        if existing:
            print("Payment methods already exist")
            return
        
        # Create default payment methods
        methods = [
            PaymentMethod(name="Cash", icon="💵", is_active=True, created_at=datetime.now()),
            PaymentMethod(name="E-Wallet", icon="📱", is_active=True, created_at=datetime.now()),
            PaymentMethod(name="Bank Transfer", icon="🏦", is_active=True, created_at=datetime.now()),
        ]
        
        for method in methods:
            db.add(method)
        
        db.commit()
        print("✅ Payment methods created: Cash, E-Wallet, Bank Transfer")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_payment_methods()
