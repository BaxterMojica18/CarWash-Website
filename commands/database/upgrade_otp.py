"""
Migration: Add otp_code column to password_reset_tokens table.
Run inside Docker: docker-compose exec web python commands/database/upgrade_otp.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:NewSecurePass2025!@db:5432/carwash_db")
engine = create_engine(DATABASE_URL)

def upgrade():
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'password_reset_tokens' AND column_name = 'otp_code'
        """))
        if result.fetchone():
            print("[OTP Migration] otp_code column already exists. Skipping.")
            return

        conn.execute(text("ALTER TABLE password_reset_tokens ADD COLUMN otp_code VARCHAR(6)"))
        conn.execute(text("CREATE INDEX ix_password_reset_tokens_otp_code ON password_reset_tokens (otp_code)"))
        conn.commit()
        print("[OTP Migration] Successfully added otp_code column to password_reset_tokens.")

if __name__ == "__main__":
    upgrade()
