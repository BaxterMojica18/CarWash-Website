from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from urllib.parse import unquote
import os
from pathlib import Path

# Force load from the correct .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and '%' in DATABASE_URL:
    parts = DATABASE_URL.split('@')
    if len(parts) == 2:
        user_pass = parts[0].replace('postgresql://', '')
        if ':' in user_pass:
            user, password = user_pass.split(':', 1)
            DATABASE_URL = f"postgresql://{user}:{unquote(password)}@{parts[1]}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_demo = Column(Boolean, default=False)
    invoices = relationship("Invoice", back_populates="creator")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    invoices = relationship("Invoice", back_populates="location")

class ProductService(Base):
    __tablename__ = "products_services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    date = Column(DateTime)
    customer_name = Column(String)
    total_amount = Column(Float)
    location_id = Column(Integer, ForeignKey("locations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    location = relationship("Location", back_populates="invoices")
    creator = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_service_id = Column(Integer, ForeignKey("products_services.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    invoice = relationship("Invoice", back_populates="items")

class CustomTheme(Base):
    __tablename__ = "settings_theme_selection"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    preset_name = Column(String)
    is_active = Column(Boolean, default=False)
    
    # Text colors: black, dark-grey, white
    text_color = Column(String, default="black")
    text_brightness = Column(Integer, default=100)
    
    # Card colors: white, grey, dark-blue
    card_color = Column(String, default="white")
    card_brightness = Column(Integer, default=100)
    
    # Input field colors: white, grey, dark-blue
    input_color = Column(String, default="white")
    input_brightness = Column(Integer, default=100)
    
    # Button color (any hex color)
    button_color = Column(String, default="#667eea")
    
    # Sidebar color (any hex color)
    sidebar_color = Column(String, default="#2c3e50")
    
    # Sidebar active button color (any hex color)
    sidebar_active_color = Column(String, default="#34495e")
    
    # Background color (any hex color)
    bg_color = Column(String, default="#f5f5f5")
    
    # Dropdown color: white, grey, dark-blue
    dropdown_color = Column(String, default="white")
    dropdown_brightness = Column(Integer, default=100)

class BusinessInfo(Base):
    __tablename__ = "business_info"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    business_name = Column(String)
    logo = Column(String, nullable=True)
    logo_type = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

class InvoiceCustomization(Base):
    __tablename__ = "invoice_customization"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    invoice_address = Column(String, nullable=True)
    invoice_phone = Column(String, nullable=True)
    invoice_email = Column(String, nullable=True)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

if __name__ == '__main__':
    create_tables()
    print("PostgreSQL tables created successfully.")
