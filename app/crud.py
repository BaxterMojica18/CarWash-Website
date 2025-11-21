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
    return db.query(database.Location).filter(
        database.Location.user_id == user_id,
        database.Location.status == "A"
    ).all()

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
        db_location.status = "D"
        db_location.deleted_at = datetime.now()
        db.commit()
        db.refresh(db_location)
    return db_location

def get_products_services(db: Session, user_id: int):
    return db.query(database.ProductService).filter(
        database.ProductService.status == "A"
    ).all()

def create_product_service(db: Session, product: schemas.ProductServiceCreate, user_id: int):
    db_product = database.ProductService(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.flush()
    
    # Generate product_id or service_id
    if product.type == 'product':
        db_product.product_id = f"PROD-{str(db_product.id).zfill(6)}"
    else:
        db_product.service_id = f"SERV-{str(db_product.id).zfill(6)}"
    
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
        db_product.quantity = product.quantity
        db_product.quantity_unit = product.quantity_unit
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product_service(db: Session, product_id: int, user_id: int):
    db_product = db.query(database.ProductService).filter(
        database.ProductService.id == product_id,
        database.ProductService.user_id == user_id
    ).first()
    if db_product:
        db_product.status = "D"
        db_product.deleted_at = datetime.now()
        db.commit()
        db.refresh(db_product)
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
    return db.query(database.Invoice).filter(database.Invoice.status == "A").all()

def delete_invoice(db: Session, invoice_id: int, user_id: int):
    db_invoice = db.query(database.Invoice).filter(
        database.Invoice.id == invoice_id,
        database.Invoice.user_id == user_id
    ).first()
    if db_invoice:
        db_invoice.status = "D"
        db_invoice.deleted_at = datetime.now()
        db.commit()
        db.refresh(db_invoice)
    return db_invoice

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

def get_user_profile(db: Session, user_id: int):
    return db.query(database.UserProfile).filter(database.UserProfile.user_id == user_id).first()

def save_user_profile(db: Session, user_id: int, profile: schemas.UserProfileCreate):
    db_profile = get_user_profile(db, user_id)
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
    else:
        db_profile = database.UserProfile(**profile.dict(), user_id=user_id)
        db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Cart CRUD
def get_cart_items(db: Session, client_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(database.CartItem).options(
        joinedload(database.CartItem.product_service)
    ).filter(database.CartItem.client_id == client_id).all()

def add_to_cart(db: Session, client_id: int, product_service_id: int, quantity: int):
    product = db.query(database.ProductService).filter(database.ProductService.id == product_service_id).first()
    if not product:
        return None
    
    cart_item = db.query(database.CartItem).filter(
        database.CartItem.client_id == client_id,
        database.CartItem.product_service_id == product_service_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = database.CartItem(
            client_id=client_id,
            product_service_id=product_service_id,
            quantity=quantity,
            price_at_add=product.price,
            created_at=datetime.now()
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, item_id: int, client_id: int, quantity: int):
    cart_item = db.query(database.CartItem).filter(
        database.CartItem.id == item_id,
        database.CartItem.client_id == client_id
    ).first()
    if cart_item:
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
    return cart_item

def remove_cart_item(db: Session, item_id: int, client_id: int):
    cart_item = db.query(database.CartItem).filter(
        database.CartItem.id == item_id,
        database.CartItem.client_id == client_id
    ).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
    return cart_item

def clear_cart(db: Session, client_id: int):
    db.query(database.CartItem).filter(database.CartItem.client_id == client_id).delete()
    db.commit()

# Order CRUD
def create_order_from_cart(db: Session, client_id: int, payment_method: str = None):
    cart_items = get_cart_items(db, client_id)
    if not cart_items:
        return None
    
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    total = sum(item.quantity * item.price_at_add for item in cart_items)
    
    order = database.Order(
        order_number=order_number,
        client_id=client_id,
        status="pending",
        total_amount=total,
        payment_method=payment_method,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for item in cart_items:
        order_item = database.OrderItem(
            order_id=order.id,
            product_service_id=item.product_service_id,
            quantity=item.quantity,
            unit_price=item.price_at_add,
            subtotal=item.quantity * item.price_at_add
        )
        db.add(order_item)
    
    db.commit()
    clear_cart(db, client_id)
    db.refresh(order)
    return order

def get_orders(db: Session, client_id: int = None):
    from sqlalchemy.orm import joinedload
    query = db.query(database.Order).options(
        joinedload(database.Order.items).joinedload(database.OrderItem.product_service)
    )
    if client_id:
        query = query.filter(database.Order.client_id == client_id)
    return query.order_by(database.Order.created_at.desc()).all()

def get_order(db: Session, order_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(database.Order).options(
        joinedload(database.Order.items).joinedload(database.OrderItem.product_service)
    ).filter(database.Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if order:
        order.status = status
        order.updated_at = datetime.now()
        db.commit()
        db.refresh(order)
    return order

# Reservation CRUD
def create_reservation(db: Session, client_id: int, service_id: int, location_id: int, vehicle_plate: str):
    service = db.query(database.ProductService).filter(database.ProductService.id == service_id).first()
    if not service or service.type != 'service':
        return None
    
    max_position = db.query(database.Reservation).filter(
        database.Reservation.location_id == location_id,
        database.Reservation.status.in_(['pending', 'accepted', 'in_progress'])
    ).with_entities(database.Reservation.queue_position).order_by(database.Reservation.queue_position.desc()).first()
    
    queue_position = (max_position[0] + 1) if max_position and max_position[0] else 1
    
    reservation_number = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    reservation = database.Reservation(
        reservation_number=reservation_number,
        client_id=client_id,
        service_id=service_id,
        location_id=location_id,
        vehicle_plate=vehicle_plate,
        status="pending",
        queue_position=queue_position,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def get_reservations(db: Session, client_id: int = None, location_id: int = None):
    from sqlalchemy.orm import joinedload
    query = db.query(database.Reservation).options(
        joinedload(database.Reservation.service),
        joinedload(database.Reservation.location)
    )
    if client_id:
        query = query.filter(database.Reservation.client_id == client_id)
    if location_id:
        query = query.filter(database.Reservation.location_id == location_id)
    return query.order_by(database.Reservation.created_at.desc()).all()

def get_reservation(db: Session, reservation_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(database.Reservation).options(
        joinedload(database.Reservation.service),
        joinedload(database.Reservation.location)
    ).filter(database.Reservation.id == reservation_id).first()

def update_reservation_status(db: Session, reservation_id: int, status: str):
    reservation = db.query(database.Reservation).filter(database.Reservation.id == reservation_id).first()
    if not reservation:
        return None
    
    old_status = reservation.status
    reservation.status = status
    reservation.updated_at = datetime.now()
    
    if status in ['completed', 'cancelled'] and old_status in ['pending', 'accepted', 'in_progress']:
        location_id = reservation.location_id
        old_position = reservation.queue_position
        reservation.queue_position = None
        db.commit()
        
        if old_position:
            db.query(database.Reservation).filter(
                database.Reservation.location_id == location_id,
                database.Reservation.queue_position > old_position,
                database.Reservation.status.in_(['pending', 'accepted', 'in_progress'])
            ).update({database.Reservation.queue_position: database.Reservation.queue_position - 1})
    
    db.commit()
    db.refresh(reservation)
    return reservation

def get_queue(db: Session, location_id: int):
    return db.query(database.Reservation).filter(
        database.Reservation.location_id == location_id,
        database.Reservation.status.in_(['pending', 'accepted', 'in_progress'])
    ).order_by(database.Reservation.queue_position).all()

# Payment Methods CRUD
def get_payment_methods(db: Session):
    return db.query(database.PaymentMethod).all()

def create_payment_method(db: Session, name: str, icon: str, is_active: bool):
    pm = database.PaymentMethod(name=name, icon=icon, is_active=is_active, created_at=datetime.now())
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm

def update_payment_method(db: Session, pm_id: int, name: str, icon: str, is_active: bool):
    pm = db.query(database.PaymentMethod).filter(database.PaymentMethod.id == pm_id).first()
    if pm:
        pm.name = name
        pm.icon = icon
        pm.is_active = is_active
        db.commit()
        db.refresh(pm)
    return pm

def delete_payment_method(db: Session, pm_id: int):
    pm = db.query(database.PaymentMethod).filter(database.PaymentMethod.id == pm_id).first()
    if pm:
        db.delete(pm)
        db.commit()
    return pm
