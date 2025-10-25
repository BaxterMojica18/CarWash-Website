from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    is_demo: bool

class LocationBase(BaseModel):
    name: str
    address: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    class Config:
        from_attributes = True

class ProductServiceBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    type: str
    quantity: Optional[float] = None
    quantity_unit: Optional[str] = None

class ProductServiceCreate(ProductServiceBase):
    pass

class ProductService(ProductServiceBase):
    id: int
    class Config:
        from_attributes = True

class InvoiceItemCreate(BaseModel):
    product_service_id: int
    quantity: int
    unit_price: float

class InvoiceItem(BaseModel):
    id: int
    product_service_id: int
    quantity: int
    unit_price: float
    subtotal: float
    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    customer_name: str
    location_id: int
    items: List[InvoiceItemCreate]

class Invoice(BaseModel):
    id: int
    invoice_number: str
    date: datetime
    customer_name: str
    total_amount: float
    location_id: int
    items: List[InvoiceItem]
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_revenue: float
    monthly_wash_count: int
    total_invoices: int
    active_locations: int

class CustomThemeCreate(BaseModel):
    preset_name: str
    text_color: str = "black"
    text_brightness: int = 100
    card_color: str = "white"
    card_brightness: int = 100
    input_color: str = "white"
    input_brightness: int = 100
    button_color: str = "#667eea"
    sidebar_color: str = "#2c3e50"
    sidebar_active_color: str = "#34495e"
    bg_color: str = "#f5f5f5"
    dropdown_color: str = "white"
    dropdown_brightness: int = 100
    delete_button_brightness: int = 100
    delete_button_saturation: int = 100

class CustomTheme(CustomThemeCreate):
    id: int
    user_id: int
    is_active: bool
    class Config:
        from_attributes = True

class BusinessInfoCreate(BaseModel):
    business_name: str
    logo: Optional[str] = None
    logo_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class BusinessInfo(BusinessInfoCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class InvoiceCustomizationCreate(BaseModel):
    invoice_address: Optional[str] = None
    invoice_phone: Optional[str] = None
    invoice_email: Optional[str] = None

class InvoiceCustomization(InvoiceCustomizationCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserProfileCreate(BaseModel):
    name: str
    role: str
    photo: Optional[str] = None

class UserProfile(UserProfileCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True
