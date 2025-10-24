from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import database, schemas
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(database.User).filter(database.User.email == email).first()

def create_user(db: Session, email: str, password: str, is_demo: bool = False):
    hashed_password = get_password_hash(password)
    user = database.User(email=email, password_hash=hashed_password, is_demo=is_demo)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_locations(db: Session, user_id: int):
    return db.query(database.Location).filter(database.Location.user_id == user_id).all()

def create_location(db: Session, location: schemas.LocationCreate, user_id: int):
    db_location = database.Location(**location.dict(), user_id=user_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: int, location: schemas.LocationCreate, user_id: int):
    db_location = db.query(database.Location).filter(
        database.Location.id == location_id,
        database.Location.user_id == user_id
    ).first()
    if db_location:
        db_location.name = location.name
        db_location.address = location.address
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int, user_id: int):
    db_location = db.query(database.Location).filter(
        database.Location.id == location_id,
        database.Location.user_id == user_id
    ).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location

def get_products_services(db: Session, user_id: int):
    return db.query(database.ProductService).filter(database.ProductService.user_id == user_id).all()

def create_product_service(db: Session, product: schemas.ProductServiceCreate, user_id: int):
    db_product = database.ProductService(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_service(db: Session, product_id: int, product: schemas.ProductServiceCreate, user_id: int):
    db_product = db.query(database.ProductService).filter(
        database.ProductService.id == product_id,
        database.ProductService.user_id == user_id
    ).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.description = product.description
        db_product.type = product.type
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product_service(db: Session, product_id: int, user_id: int):
    db_product = db.query(database.ProductService).filter(
        database.ProductService.id == product_id,
        database.ProductService.user_id == user_id
    ).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def create_invoice(db: Session, invoice: schemas.InvoiceCreate, user_id: int):
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    total = sum(item.quantity * item.unit_price for item in invoice.items)
    
    db_invoice = database.Invoice(
        invoice_number=invoice_number,
        date=datetime.now(),
        customer_name=invoice.customer_name,
        total_amount=total,
        location_id=invoice.location_id,
        user_id=user_id
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    for item in invoice.items:
        db_item = database.InvoiceItem(
            invoice_id=db_invoice.id,
            product_service_id=item.product_service_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(database.Invoice).filter(database.Invoice.id == invoice_id).first()

def get_invoices(db: Session):
    return db.query(database.Invoice).all()

def get_dashboard_stats(db: Session):
    total_revenue = db.query(database.Invoice).with_entities(
        database.Invoice.total_amount
    ).all()
    total_revenue = sum([r[0] for r in total_revenue]) if total_revenue else 0
    
    total_invoices = db.query(database.Invoice).count()
    active_locations = db.query(database.Location).count()
    
    return {
        "total_revenue": total_revenue,
        "monthly_wash_count": total_invoices,
        "total_invoices": total_invoices,
        "active_locations": active_locations
    }

def get_active_theme(db: Session, user_id: int):
    return db.query(database.CustomTheme).filter(
        database.CustomTheme.user_id == user_id,
        database.CustomTheme.is_active == True
    ).first()

def get_all_themes(db: Session, user_id: int):
    return db.query(database.CustomTheme).filter(database.CustomTheme.user_id == user_id).all()

def save_custom_theme(db: Session, user_id: int, theme: schemas.CustomThemeCreate):
    db.query(database.CustomTheme).filter(database.CustomTheme.user_id == user_id).update({"is_active": False})
    db_theme = database.CustomTheme(**theme.dict(), user_id=user_id, is_active=True)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def activate_theme(db: Session, user_id: int, theme_id: int):
    db.query(database.CustomTheme).filter(database.CustomTheme.user_id == user_id).update({"is_active": False})
    theme = db.query(database.CustomTheme).filter(database.CustomTheme.id == theme_id).first()
    if theme:
        theme.is_active = True
        db.commit()
        db.refresh(theme)
    return theme

def delete_theme(db: Session, theme_id: int):
    theme = db.query(database.CustomTheme).filter(database.CustomTheme.id == theme_id).first()
    if theme:
        db.delete(theme)
        db.commit()
    return theme

def get_business_info(db: Session, user_id: int):
    return db.query(database.BusinessInfo).filter(database.BusinessInfo.user_id == user_id).first()

def save_business_info(db: Session, user_id: int, info: schemas.BusinessInfoCreate):
    db_info = get_business_info(db, user_id)
    if db_info:
        for key, value in info.dict().items():
            setattr(db_info, key, value)
    else:
        db_info = database.BusinessInfo(**info.dict(), user_id=user_id)
        db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

def get_invoice_customization(db: Session, user_id: int):
    return db.query(database.InvoiceCustomization).filter(database.InvoiceCustomization.user_id == user_id).first()

def save_invoice_customization(db: Session, user_id: int, custom: schemas.InvoiceCustomizationCreate):
    db_custom = get_invoice_customization(db, user_id)
    if db_custom:
        for key, value in custom.dict().items():
            setattr(db_custom, key, value)
    else:
        db_custom = database.InvoiceCustomization(**custom.dict(), user_id=user_id)
        db.add(db_custom)
    db.commit()
    db.refresh(db_custom)
    return db_custom
