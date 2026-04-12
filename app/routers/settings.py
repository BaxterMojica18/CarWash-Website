from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission
from app.demo_limits import DemoLimits
from app.crud import get_business_user_ids, get_business_owner_id

class PaymentMethodCreate(BaseModel):
    name: str
    icon: str
    is_active: bool

class PaymentMethodResponse(BaseModel):
    id: int
    name: str
    icon: str
    is_active: bool
    class Config:
        from_attributes = True

router = APIRouter()

@router.get("/locations", response_model=List[schemas.Location])
def get_locations(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    biz_ids = get_business_user_ids(db, current_user)
    return crud.get_locations(db, current_user.id, business_user_ids=biz_ids)

@router.post("/locations", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_locations"))):
    return crud.create_location(db, location, current_user.id)

@router.put("/locations/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_locations"))):
    db_location = crud.update_location(db, location_id, location, current_user.id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_locations"))):
    db_location = crud.delete_location(db, location_id, current_user.id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}

@router.get("/products", response_model=List[schemas.ProductService])
def get_products(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    biz_ids = get_business_user_ids(db, current_user)
    return crud.get_products_services(db, current_user.id, business_user_ids=biz_ids)

@router.post("/products", response_model=schemas.ProductService)
def create_product(product: schemas.ProductServiceCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_products"))):
    if product.type == "product":
        DemoLimits.check_limit(db, current_user, "products")
    else:
        DemoLimits.check_limit(db, current_user, "services")
    
    result = crud.create_product_service(db, product, current_user.id)
    
    if product.type == "product":
        DemoLimits.increment_usage(db, current_user, "products")
    else:
        DemoLimits.increment_usage(db, current_user, "services")
    
    return result

@router.put("/products/{product_id}", response_model=schemas.ProductService)
def update_product(product_id: int, product: schemas.ProductServiceCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_products"))):
    db_product = crud.update_product_service(db, product_id, product, current_user.id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_products"))):
    db_product = crud.delete_product_service(db, product_id, current_user.id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/theme/active")
def get_active_theme(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    owner_id = get_business_owner_id(db, current_user)
    # If user is a client, try to return the client-specific theme first
    is_client = current_user.account_type == 'client'
    if is_client:
        client_theme = crud.get_active_theme(db, owner_id, for_client=True)
        if client_theme:
            return client_theme
    # Fall back to the staff/admin theme
    theme = crud.get_active_theme(db, owner_id, for_client=False)
    if not theme:
        return None
    return theme

@router.get("/theme/all", response_model=List[schemas.CustomTheme])
def get_all_themes(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    try:
        owner_id = get_business_owner_id(db, current_user)
        return crud.get_all_themes(db, owner_id, for_client=False)
    except Exception as e:
        print(f"Error in get_all_themes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Client-specific theme endpoints (admin sets a different theme for clients)
@router.get("/theme/client/active")
def get_client_active_theme(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    owner_id = get_business_owner_id(db, current_user)
    theme = crud.get_active_theme(db, owner_id, for_client=True)
    if not theme:
        return None
    return theme

@router.get("/theme/client/all", response_model=List[schemas.CustomTheme])
def get_all_client_themes(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    owner_id = get_business_owner_id(db, current_user)
    return crud.get_all_themes(db, owner_id, for_client=True)

@router.post("/theme", response_model=schemas.CustomTheme)
def save_theme(theme: schemas.CustomThemeCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    owner_id = get_business_owner_id(db, current_user)
    return crud.save_custom_theme(db, owner_id, theme)

@router.put("/theme/{theme_id}/activate", response_model=schemas.CustomTheme)
def activate_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    owner_id = get_business_owner_id(db, current_user)
    theme = crud.activate_theme(db, owner_id, theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.delete("/theme/{theme_id}")
def delete_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    crud.delete_theme(db, theme_id)
    return {"message": "Theme deleted"}

@router.get("/business", response_model=schemas.BusinessInfo)
def get_business(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    owner_id = get_business_owner_id(db, current_user)
    info = crud.get_business_info(db, current_user.id, owner_id=owner_id)
    if not info:
        raise HTTPException(status_code=404, detail="Business info not found")
    return info

@router.post("/business", response_model=schemas.BusinessInfo)
def save_business(info: schemas.BusinessInfoCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    owner_id = get_business_owner_id(db, current_user)
    return crud.save_business_info(db, owner_id, info)

@router.get("/invoice-custom", response_model=schemas.InvoiceCustomization)
def get_invoice_custom(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    owner_id = get_business_owner_id(db, current_user)
    custom = crud.get_invoice_customization(db, owner_id)
    if not custom:
        raise HTTPException(status_code=404, detail="Invoice customization not found")
    return custom

@router.post("/invoice-custom", response_model=schemas.InvoiceCustomization)
def save_invoice_custom(custom: schemas.InvoiceCustomizationCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    owner_id = get_business_owner_id(db, current_user)
    return crud.save_invoice_customization(db, owner_id, custom)

@router.get("/profile", response_model=schemas.UserProfile)
def get_profile(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    profile = crud.get_user_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    # Inject business number from the user model dynamically
    setattr(profile, "business_number", current_user.business_number)
    return profile

@router.post("/profile", response_model=schemas.UserProfile)
def save_profile(profile: schemas.UserProfileCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.save_user_profile(db, current_user.id, profile)

@router.get("/preferences", response_model=schemas.UserPreferenceResponse)
def get_preferences(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_user_preferences(db, current_user.id)

@router.post("/preferences", response_model=schemas.UserPreferenceResponse)
def update_preferences(pref: schemas.UserPreferenceUpdate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.update_user_preferences(db, current_user.id, pref)

@router.get("/phone")
def get_phone(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    user = db.query(database.User).filter(database.User.id == current_user.id).first()
    return {"phone_number": user.phone_number if user else None}

@router.post("/phone")
def update_phone(phone_data: schemas.UserPhoneUpdate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    crud.update_user_phone(db, current_user.id, phone_data.phone_number)
    return {"message": "Phone number updated successfully"}

@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_payment_methods(db)

@router.post("/payment-methods", response_model=PaymentMethodResponse)
def create_payment_method(pm: PaymentMethodCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    return crud.create_payment_method(db, pm.name, pm.icon, pm.is_active)

@router.put("/payment-methods/{pm_id}", response_model=PaymentMethodResponse)
def update_payment_method(pm_id: int, pm: PaymentMethodCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    result = crud.update_payment_method(db, pm_id, pm.name, pm.icon, pm.is_active)
    if not result:
        raise HTTPException(status_code=404, detail="Payment method not found")
    return result

@router.delete("/payment-methods/{pm_id}")
def delete_payment_method(pm_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    result = crud.delete_payment_method(db, pm_id)
    if not result:
        raise HTTPException(status_code=404, detail="Payment method not found")
    return {"message": "Payment method deleted"}

class JoinBusinessRequest(BaseModel):
    business_code: str

@router.post("/notification-email")
def save_notification_email(data: dict, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    """Save the fallback notification email for demo/unlinked accounts."""
    import os
    email = data.get("email", "").strip()
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    # Store in environment at runtime (affects current process only)
    os.environ["DEMO_NOTIFICATION_EMAIL"] = email
    # Also persist in business_info email field for the owner
    from app.crud import get_business_owner_id, save_business_info
    owner_id = get_business_owner_id(db, current_user)
    info = db.query(database.BusinessInfo).filter(database.BusinessInfo.user_id == owner_id).first()
    if info:
        info.email = email
        db.commit()
    return {"message": "Notification email updated"}


@router.get("/business-code")
def get_business_code(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    if not current_user.business_number:
        raise HTTPException(status_code=404, detail="No business code found")
    return {"business_code": current_user.business_number}

@router.post("/join-business")
def join_business(data: JoinBusinessRequest, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    code = data.business_code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Business code is required")
    owner = db.query(database.User).filter(database.User.business_number == code).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Invalid business code")
    if current_user.business_number == code:
        raise HTTPException(status_code=400, detail="You are already part of this business")
    current_user.business_number = code
    db.commit()
    return {"message": "Successfully joined the business"}
