from app.database import SessionLocal, engine
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        # Add qr_image and account_number columns
        db.execute(text("ALTER TABLE payment_methods ADD COLUMN IF NOT EXISTS qr_image TEXT"))
        db.execute(text("ALTER TABLE payment_methods ADD COLUMN IF NOT EXISTS account_number VARCHAR"))
        db.commit()
        print("✅ Payment methods table updated with qr_image and account_number columns")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
