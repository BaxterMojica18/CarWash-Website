from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Table,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from urllib.parse import unquote
import os
from pathlib import Path

# Load .env only in local development (not on Render/production)
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and "%" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    if len(parts) == 2:
        user_pass = parts[0].replace("postgresql://", "")
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            DATABASE_URL = f"postgresql://{user}:{unquote(password)}@{parts[1]}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_demo = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True)
    phone_number = Column(String, nullable=True)
    account_type = Column(String, nullable=True)  # admin, staff, client, owner
    business_number = Column(String, index=True, nullable=True)
    invoices = relationship("Invoice", back_populates="creator")
    roles = relationship("Role", secondary=user_roles)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String)
    role = Column(String)
    photo = Column(String, nullable=True)


class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    sms_opt_in = Column(Boolean, default=True)


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="A")
    deleted_at = Column(DateTime, nullable=True)
    invoices = relationship("Invoice", back_populates="location")


class ProductService(Base):
    __tablename__ = "products_services"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=True, index=True)
    service_id = Column(String, nullable=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    type = Column(String)
    quantity = Column(Float, nullable=True)
    quantity_unit = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="A")
    deleted_at = Column(DateTime, nullable=True)


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    date = Column(DateTime)
    customer_name = Column(String)
    total_amount = Column(Float)
    location_id = Column(Integer, ForeignKey("locations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="A")
    deleted_at = Column(DateTime, nullable=True)
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
    for_client = Column(
        Boolean, default=False
    )  # True = client-facing theme, False = staff/admin theme

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

    # Delete button customization
    delete_button_brightness = Column(Integer, default=100)
    delete_button_saturation = Column(Integer, default=100)


class BusinessInfo(Base):
    __tablename__ = "business_info"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    business_name = Column(String)
    business_sub_name = Column(String, nullable=True)
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


class ReportCache(Base):
    __tablename__ = "reports_cache"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String)
    filter_period = Column(String)
    filter_value = Column(String)
    generated_at = Column(DateTime)
    total_sales = Column(Float)
    total_invoices = Column(Integer)


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    product_service_id = Column(Integer, ForeignKey("products_services.id"))
    quantity = Column(Integer)
    price_at_add = Column(Float)
    created_at = Column(DateTime)
    client = relationship("User")
    product_service = relationship("ProductService")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    total_amount = Column(Float)
    payment_method = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    client = relationship("User")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_service_id = Column(Integer, ForeignKey("products_services.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    order = relationship("Order", back_populates="items")
    product_service = relationship("ProductService")


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    reservation_number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("products_services.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    vehicle_plate = Column(String)
    status = Column(String, default="pending")
    queue_position = Column(Integer, nullable=True)
    estimated_start_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    client = relationship("User")
    service = relationship("ProductService")
    location = relationship("Location")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    qr_image = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    otp_code = Column(String(6), nullable=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class DashboardSettings(Base):
    __tablename__ = "dashboard_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    website_name = Column(String)
    primary_color = Column(String)
    background_color = Column(String)
    sidebar_color = Column(String)
    layout_type = Column(String)
    button_color = Column(String)
    text_color = Column(String)
    sidebar_active_color = Column(String)
    card_color = Column(String)
    card_text_color = Column(String)
    updated_at = Column(DateTime, server_default=func.now())


class DashboardModule(Base):
    __tablename__ = "dashboard_modules"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_name = Column(String)
    module_type = Column(String)
    title = Column(String)
    position = Column(Integer)
    width = Column(String)
    is_visible = Column(Boolean, default=True)
    config = Column(String, nullable=True)
    updated_at = Column(DateTime, server_default=func.now())


class UserSidebarSetting(Base):
    __tablename__ = "user_sidebar_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    page_name = Column(String)
    is_visible = Column(Boolean, default=True)
    business_number = Column(String, default="__global__")


class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    discount_type = Column(String, default="percentage")  # "percentage" or "fixed"
    discount_value = Column(Float, nullable=False)
    min_spend = Column(Float, default=0)
    max_uses = Column(Integer, nullable=True)  # None = unlimited
    uses_count = Column(Integer, default=0)
    stock = Column(Integer, nullable=True)  # remaining voucher stock
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    business_number = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)  # soft delete


class FlashSale(Base):
    __tablename__ = "flash_sales"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    discount_type = Column(String, default="percentage")  # "percentage" or "fixed"
    discount_value = Column(Float, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    business_number = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    items = relationship("FlashSaleItem", back_populates="flash_sale")


class FlashSaleItem(Base):
    __tablename__ = "flash_sale_items"
    id = Column(Integer, primary_key=True, index=True)
    flash_sale_id = Column(Integer, ForeignKey("flash_sales.id"), nullable=False)
    product_service_id = Column(
        Integer, ForeignKey("products_services.id"), nullable=False
    )
    flash_sale = relationship("FlashSale", back_populates="items")
    product_service = relationship("ProductService")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # "create", "update", "delete"
    resource_type = Column(
        String, nullable=False
    )  # "product", "service", "order", etc.
    resource_id = Column(Integer, nullable=True)
    details = Column(String, nullable=True)  # JSON string
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(
        String, nullable=False
    )  # "order", "reservation", "payment", "coupon", "flash_sale", "permission"
    is_read = Column(Boolean, default=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)  # soft delete
    user = relationship("User")


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    order_notifications = Column(Boolean, default=True)
    reservation_notifications = Column(Boolean, default=True)
    payment_notifications = Column(Boolean, default=True)
    coupon_notifications = Column(Boolean, default=True)
    flash_sale_notifications = Column(Boolean, default=True)
    permission_notifications = Column(Boolean, default=True)


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


if __name__ == "__main__":
    create_tables()
    print("PostgreSQL tables created successfully.")


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    concern = Column(String, nullable=False)
    status = Column(String, default="open")
    reply = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    replied_at = Column(DateTime, nullable=True)
