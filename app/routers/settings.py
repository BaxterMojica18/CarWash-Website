from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.permissions import has_permission
from app.demo_limits import DemoLimits

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
    from app.permissions import get_user_permissions
    perms = get_user_permissions(current_user)
    if 'view_locations' not in perms and 'manage_locations' not in perms:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.get_locations(db, current_user.id)

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
    return crud.get_products_services(db, current_user.id)

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
    theme = crud.get_active_theme(db, current_user.id)
    if not theme:
        return None
    return theme

@router.get("/theme/all", response_model=List[schemas.CustomTheme])
def get_all_themes(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    try:
        return crud.get_all_themes(db, current_user.id)
    except Exception as e:
        print(f"Error in get_all_themes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/theme", response_model=schemas.CustomTheme)
def save_theme(theme: schemas.CustomThemeCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    return crud.save_custom_theme(db, current_user.id, theme)

@router.put("/theme/{theme_id}/activate", response_model=schemas.CustomTheme)
def activate_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    theme = crud.activate_theme(db, current_user.id, theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.delete("/theme/{theme_id}")
def delete_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    crud.delete_theme(db, theme_id)
    return {"message": "Theme deleted"}

@router.get("/business", response_model=schemas.BusinessInfo)
def get_business(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    info = crud.get_business_info(db, current_user.id)
    if not info:
        raise HTTPException(status_code=404, detail="Business info not found")
    return info

@router.post("/business", response_model=schemas.BusinessInfo)
def save_business(info: schemas.BusinessInfoCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    return crud.save_business_info(db, current_user.id, info)

@router.get("/invoice-custom", response_model=schemas.InvoiceCustomization)
def get_invoice_custom(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    custom = crud.get_invoice_customization(db, current_user.id)
    if not custom:
        raise HTTPException(status_code=404, detail="Invoice customization not found")
    return custom

@router.post("/invoice-custom", response_model=schemas.InvoiceCustomization)
def save_invoice_custom(custom: schemas.InvoiceCustomizationCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_settings"))):
    return crud.save_invoice_customization(db, current_user.id, custom)

@router.get("/profile", response_model=schemas.UserProfile)
def get_profile(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    profile = crud.get_user_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/profile", response_model=schemas.UserProfile)
def save_profile(profile: schemas.UserProfileCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.save_user_profile(db, current_user.id, profile)

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
