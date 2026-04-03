from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import database, schemas
from datetime import datetime, timedelta
import uuid
import random
from typing import List as TypingList

def get_business_user_ids(db: Session, user: database.User) -> TypingList[int]:
    """Get all user IDs that belong to the same business (share same business_number).
    This is the core of multi-tenant data isolation."""
    if not user.business_number:
        return [user.id]
    
    users = db.query(database.User.id).filter(
        database.User.business_number == user.business_number
    ).all()
    return [u[0] for u in users] if users else [user.id]

def get_business_owner_id(db: Session, user: database.User) -> int:
    """Get the owner's user_id for this business. Settings are stored under the owner."""
    if not user.business_number:
        return user.id
    
    owner = db.query(database.User).filter(
        database.User.business_number == user.business_number,
        database.User.account_type == 'owner'
    ).first()
    return owner.id if owner else user.id

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

def register_user(db: Session, reg_data: schemas.UserRegister):
    # Check if user already exists
    if get_user_by_email(db, reg_data.email):
        raise Exception("User already exists")
    
    hashed_password = get_password_hash(reg_data.password)
    
    business_number = reg_data.business_number
    if reg_data.account_type == 'owner':
        # Generate a unique business number
        # For simplicity, we just generate one and check if it exists
        while True:
            business_number = f"BN-{random.randint(100000, 999999)}"
            existing = db.query(database.User).filter(database.User.business_number == business_number, database.User.account_type == 'owner').first()
            if not existing:
                break
    elif business_number:
        # Check if the business number exists and belongs to an owner
        owner = db.query(database.User).filter(database.User.business_number == business_number, database.User.account_type == 'owner').first()
        if not owner:
            # If not found among owners, maybe just check if it exists at all? 
            # User said "admins, staffs, and clients can put in... so they can be considered as part of the same business"
            # This implies they need a valid business number from an owner.
            raise Exception("Invalid business number. Please ask your business owner for the correct code.")
    
    user = database.User(
        email=reg_data.email, 
        password_hash=hashed_password, 
        phone_number=reg_data.phone,
        account_type=reg_data.account_type,
        business_number=business_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assign roles based on account_type
    role_name = reg_data.account_type
    # Mapping for permissions
    db_role = db.query(database.Role).filter(database.Role.name == role_name).first()
    if db_role:
        user.roles.append(db_role)
    
    # Create profile
    profile = database.UserProfile(
        user_id=user.id,
        name=reg_data.fullName,
        role=role_name
    )
    db.add(profile)
    
    # If owner, create business info
    if reg_data.account_type == 'owner':
        business_info = database.BusinessInfo(
            user_id=user.id,
            business_name=f"{reg_data.fullName}'s Car Wash"
        )
        db.add(business_info)

    db.commit()
    db.refresh(user)
    return user

def get_locations(db: Session, user_id: int, business_user_ids: TypingList[int] = None):
    query = db.query(database.Location).filter(database.Location.status == "A")
    if business_user_ids:
        query = query.filter(database.Location.user_id.in_(business_user_ids))
    else:
        query = query.filter(database.Location.user_id == user_id)
    return query.all()

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

def get_products_services(db: Session, user_id: int, business_user_ids: TypingList[int] = None):
    query = db.query(database.ProductService).filter(database.ProductService.status == "A")
    if business_user_ids:
        query = query.filter(database.ProductService.user_id.in_(business_user_ids))
    else:
        query = query.filter(database.ProductService.user_id == user_id)
    return query.all()

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

def get_invoices(db: Session, business_user_ids: TypingList[int] = None):
    query = db.query(database.Invoice).filter(database.Invoice.status == "A")
    if business_user_ids:
        query = query.filter(database.Invoice.user_id.in_(business_user_ids))
    return query.all()

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

def get_dashboard_stats(db: Session, business_user_ids: TypingList[int] = None):
    inv_query = db.query(database.Invoice)
    loc_query = db.query(database.Location)
    
    if business_user_ids:
        inv_query = inv_query.filter(database.Invoice.user_id.in_(business_user_ids))
        loc_query = loc_query.filter(database.Location.user_id.in_(business_user_ids))
    
    total_revenue = inv_query.with_entities(
        database.Invoice.total_amount
    ).all()
    total_revenue = sum([r[0] for r in total_revenue]) if total_revenue else 0
    
    total_invoices = inv_query.count()
    active_locations = loc_query.filter(database.Location.status == "A").count()
    
    return {
        "total_revenue": total_revenue,
        "monthly_wash_count": total_invoices,
        "total_invoices": total_invoices,
        "active_locations": active_locations
    }

def get_active_theme(db: Session, user_id: int, for_client: bool = False):
    return db.query(database.CustomTheme).filter(
        database.CustomTheme.user_id == user_id,
        database.CustomTheme.is_active == True,
        database.CustomTheme.for_client == for_client
    ).first()

def get_all_themes(db: Session, user_id: int, for_client: bool = None):
    query = db.query(database.CustomTheme).filter(database.CustomTheme.user_id == user_id)
    if for_client is not None:
        query = query.filter(database.CustomTheme.for_client == for_client)
    return query.all()

def save_custom_theme(db: Session, user_id: int, theme: schemas.CustomThemeCreate):
    for_client = getattr(theme, 'for_client', False)
    # Deactivate only themes of the same type (staff or client)
    db.query(database.CustomTheme).filter(
        database.CustomTheme.user_id == user_id,
        database.CustomTheme.for_client == for_client
    ).update({"is_active": False})
    db_theme = database.CustomTheme(**theme.dict(), user_id=user_id, is_active=True)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def activate_theme(db: Session, user_id: int, theme_id: int):
    theme = db.query(database.CustomTheme).filter(database.CustomTheme.id == theme_id).first()
    if theme:
        # Deactivate only themes of the same type (staff or client)
        db.query(database.CustomTheme).filter(
            database.CustomTheme.user_id == user_id,
            database.CustomTheme.for_client == theme.for_client
        ).update({"is_active": False})
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

def get_business_info(db: Session, user_id: int, owner_id: int = None):
    """Get business info. Uses owner_id if provided (for staff/admin looking up their business owner's info)."""
    lookup_id = owner_id if owner_id else user_id
    return db.query(database.BusinessInfo).filter(database.BusinessInfo.user_id == lookup_id).first()

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
    profile = db.query(database.UserProfile).filter(database.UserProfile.user_id == user_id).first()
    if not profile:
        user = db.query(database.User).filter(database.User.id == user_id).first()
        if user:
            role = user.roles[0].name if user.roles else "user"
            profile = database.UserProfile(
                user_id=user_id,
                name=user.email.split("@")[0].capitalize(),
                role=role.capitalize()
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
    return profile

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

# User Preferences and Phone
def get_user_preferences(db: Session, user_id: int):
    pref = db.query(database.UserPreference).filter(database.UserPreference.user_id == user_id).first()
    # Create default preference if it doesn't exist
    if not pref:
        pref = database.UserPreference(user_id=user_id, sms_opt_in=True)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref

def update_user_preferences(db: Session, user_id: int, pref_update: schemas.UserPreferenceUpdate):
    pref = get_user_preferences(db, user_id)
    pref.sms_opt_in = pref_update.sms_opt_in
    db.commit()
    db.refresh(pref)
    return pref

def update_user_phone(db: Session, user_id: int, phone_number: str):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if user:
        user.phone_number = phone_number
        db.commit()
        db.refresh(user)
    return user

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

# Password Reset CRUD
def create_password_reset_token(db: Session, user_id: int) -> dict:
    # Invalidate any existing unused tokens for this user
    db.query(database.PasswordResetToken).filter(
        database.PasswordResetToken.user_id == user_id,
        database.PasswordResetToken.used == False
    ).update({"used": True})
    
    token = str(uuid.uuid4())
    otp_code = str(random.randint(100000, 999999))
    reset_token = database.PasswordResetToken(
        user_id=user_id,
        token=token,
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    db.add(reset_token)
    db.commit()
    return {"token": token, "otp_code": otp_code}

def validate_password_reset_token(db: Session, token: str):
    reset_token = db.query(database.PasswordResetToken).filter(
        database.PasswordResetToken.token == token,
        database.PasswordResetToken.used == False
    ).first()
    
    if not reset_token:
        return None
    
    if reset_token.expires_at < datetime.utcnow():
        return None
    
    user = db.query(database.User).filter(database.User.id == reset_token.user_id).first()
    return user

def reset_password(db: Session, user_id: int, new_password: str):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if user:
        user.password_hash = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
    return user

def invalidate_reset_token(db: Session, token: str):
    reset_token = db.query(database.PasswordResetToken).filter(
        database.PasswordResetToken.token == token
    ).first()
    if reset_token:
        reset_token.used = True
        db.commit()

def validate_otp_code(db: Session, email: str, otp_code: str):
    """Validate a 6-digit OTP code for a given email. Returns the reset token string if valid."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    reset_entry = db.query(database.PasswordResetToken).filter(
        database.PasswordResetToken.user_id == user.id,
        database.PasswordResetToken.otp_code == otp_code,
        database.PasswordResetToken.used == False
    ).first()
    
    if not reset_entry:
        return None
    
    if reset_entry.expires_at < datetime.utcnow():
        return None
    
    return reset_entry.token

def get_or_create_firebase_user(db: Session, email: str, name: str = None):
    """
    Finds an existing user by email or creates a new one 
    if they authenticated via Firebase for the first time.
    """
    user = get_user_by_email(db, email)
    
    if not user:
        # Generate a random strong password for the local DB wrapper
        random_password = str(uuid.uuid4())
        user = create_user(db, email=email, password=random_password, is_demo=False)
        
        # Assign 'client' role by default
        client_role = db.query(database.Role).filter(database.Role.name == "client").first()
        if client_role:
            user.roles.append(client_role)
            db.commit()
            
        # Always create a profile to prevent 404 Errors on /profile endpoint
        # The schema uses 'name' and 'role' fields
        profile_name = name if name else f"User {email.split('@')[0].capitalize()}"
            
        profile = database.UserProfile(
            user_id=user.id,
            name=profile_name,
            role="client"
        )
        db.add(profile)
        db.commit()
        db.refresh(user)
            
    return user
