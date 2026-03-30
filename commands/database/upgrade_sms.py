import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:NewSecurePass2025!@localhost:5432/carwash_db")

def upgrade():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone_number VARCHAR;"))
            print("Added phone_number column to users table.")
        except Exception as e:
            print(f"Column might already exist or error: {e}")
            
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER UNIQUE REFERENCES users(id),
                    sms_opt_in BOOLEAN DEFAULT TRUE
                );
            """))
            print("Created user_preferences table.")
        except Exception as e:
            print(f"Error creating user_preferences table: {e}")
            
        conn.commit()

if __name__ == "__main__":
    upgrade()
