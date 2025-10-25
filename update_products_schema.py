from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Add quantity column to products_services
    try:
        conn.execute(text("ALTER TABLE products_services ADD COLUMN quantity FLOAT"))
        conn.commit()
        print("Added quantity column")
    except Exception as e:
        print(f"quantity column might already exist: {e}")
    
    # Add quantity_unit column to products_services
    try:
        conn.execute(text("ALTER TABLE products_services ADD COLUMN quantity_unit VARCHAR"))
        conn.commit()
        print("Added quantity_unit column")
    except Exception as e:
        print(f"quantity_unit column might already exist: {e}")
    
    # Add delete button customization to theme
    try:
        conn.execute(text("ALTER TABLE settings_theme_selection ADD COLUMN delete_button_brightness INTEGER DEFAULT 100"))
        conn.execute(text("ALTER TABLE settings_theme_selection ADD COLUMN delete_button_saturation INTEGER DEFAULT 100"))
        conn.commit()
        print("Added delete button customization columns")
    except Exception as e:
        print(f"Delete button columns might already exist: {e}")

print("Migration complete!")
