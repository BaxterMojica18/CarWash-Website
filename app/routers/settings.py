from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/locations", response_model=List[schemas.Location])
def get_locations(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_locations(db, current_user.id)

@router.post("/locations", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.create_location(db, location, current_user.id)

@router.put("/locations/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    db_location = crud.update_location(db, location_id, location, current_user.id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    db_location = crud.delete_location(db, location_id, current_user.id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}

@router.get("/products", response_model=List[schemas.ProductService])
def get_products(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_products_services(db, current_user.id)

@router.post("/products", response_model=schemas.ProductService)
def create_product(product: schemas.ProductServiceCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.create_product_service(db, product, current_user.id)

@router.put("/products/{product_id}", response_model=schemas.ProductService)
def update_product(product_id: int, product: schemas.ProductServiceCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    db_product = crud.update_product_service(db, product_id, product, current_user.id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
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
def save_theme(theme: schemas.CustomThemeCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.save_custom_theme(db, current_user.id, theme)

@router.put("/theme/{theme_id}/activate", response_model=schemas.CustomTheme)
def activate_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    theme = crud.activate_theme(db, current_user.id, theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.delete("/theme/{theme_id}")
def delete_theme(theme_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    crud.delete_theme(db, theme_id)
    return {"message": "Theme deleted"}

@router.get("/business", response_model=schemas.BusinessInfo)
def get_business(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    info = crud.get_business_info(db, current_user.id)
    if not info:
        raise HTTPException(status_code=404, detail="Business info not found")
    return info

@router.post("/business", response_model=schemas.BusinessInfo)
def save_business(info: schemas.BusinessInfoCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.save_business_info(db, current_user.id, info)

@router.get("/invoice-custom", response_model=schemas.InvoiceCustomization)
def get_invoice_custom(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    custom = crud.get_invoice_customization(db, current_user.id)
    if not custom:
        raise HTTPException(status_code=404, detail="Invoice customization not found")
    return custom

@router.post("/invoice-custom", response_model=schemas.InvoiceCustomization)
def save_invoice_custom(custom: schemas.InvoiceCustomizationCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.save_invoice_customization(db, current_user.id, custom)
