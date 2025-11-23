# -*- coding: utf-8 -*-
"""
Create dashboard customization tables
"""
from sqlalchemy import text
from app.database import SessionLocal

def create_tables():
    db = SessionLocal()
    
    try:
        # Dashboard settings table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS dashboard_settings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                website_name VARCHAR(255) DEFAULT 'CarWash',
                primary_color VARCHAR(50) DEFAULT '#667eea',
                background_color VARCHAR(50) DEFAULT '#f5f5f5',
                sidebar_color VARCHAR(50) DEFAULT '#2c3e50',
                layout_type VARCHAR(50) DEFAULT 'grid',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Dashboard modules table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS dashboard_modules (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                module_name VARCHAR(255) NOT NULL,
                module_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                position INTEGER DEFAULT 0,
                width VARCHAR(50) DEFAULT 'full',
                is_visible BOOLEAN DEFAULT TRUE,
                config JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        db.commit()
        
        print("="*60)
        print("DASHBOARD CUSTOMIZATION TABLES CREATED")
        print("="*60)
        print("\nTables created:")
        print("- dashboard_settings: Store website name, colors, layout")
        print("- dashboard_modules: Store dashboard widgets/modules")
        print("\nFeatures:")
        print("- Customize website name")
        print("- Change colors (primary, background, sidebar)")
        print("- Change layout type")
        print("- Add/Edit/Delete dashboard modules")
        print("- Reorder modules")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
