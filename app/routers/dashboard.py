from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.dependencies import get_current_user
from app.permissions import is_superadmin

router = APIRouter()

class DashboardSettings(BaseModel):
    website_name: str
    primary_color: str
    background_color: str
    sidebar_color: str
    button_color: str = '#667eea'
    text_color: str = '#333333'
    sidebar_active_color: str = '#34495e'
    card_color: str = '#ffffff'
    card_text_color: str = '#333333'
    layout_type: str

class DashboardModule(BaseModel):
    module_name: str
    module_type: str
    title: str
    position: int
    width: str
    is_visible: bool
    config: Optional[dict] = None

class DashboardModuleResponse(DashboardModule):
    id: int

@router.get("/settings")
def get_dashboard_settings(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = db.execute(
        text("""SELECT website_name, primary_color, background_color, sidebar_color, 
                layout_type, button_color, text_color, sidebar_active_color, card_color, card_text_color 
                FROM dashboard_settings WHERE user_id = :uid ORDER BY id DESC LIMIT 1"""),
        {"uid": current_user.id}
    ).fetchone()
    
    if not result:
        return {
            "website_name": "CarWash",
            "primary_color": "#667eea",
            "background_color": "#f5f5f5",
            "sidebar_color": "#2c3e50",
            "button_color": "#667eea",
            "text_color": "#333333",
            "sidebar_active_color": "#34495e",
            "card_color": "#ffffff",
            "card_text_color": "#333333",
            "layout_type": "grid"
        }
    
    return {
        "website_name": result[0],
        "primary_color": result[1],
        "background_color": result[2],
        "sidebar_color": result[3],
        "layout_type": result[4],
        "button_color": result[5] or "#667eea",
        "text_color": result[6] or "#333333",
        "sidebar_active_color": result[7] or "#34495e",
        "card_color": result[8] or "#ffffff",
        "card_text_color": result[9] or "#333333"
    }

@router.post("/settings")
def save_dashboard_settings(settings: DashboardSettings, db: Session = Depends(get_db), current_user = Depends(is_superadmin)):
    existing = db.execute(
        text("SELECT id FROM dashboard_settings WHERE user_id = :uid"),
        {"uid": current_user.id}
    ).fetchone()
    
    if existing:
        db.execute(text("""
            UPDATE dashboard_settings 
            SET website_name = :name, primary_color = :primary, 
                background_color = :bg, sidebar_color = :sidebar, 
                button_color = :button, text_color = :text,
                sidebar_active_color = :sidebar_active, card_color = :card, card_text_color = :card_text,
                layout_type = :layout, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = :uid
        """), {
            "name": settings.website_name,
            "primary": settings.primary_color,
            "bg": settings.background_color,
            "sidebar": settings.sidebar_color,
            "button": settings.button_color,
            "text": settings.text_color,
            "sidebar_active": settings.sidebar_active_color,
            "card": settings.card_color,
            "card_text": settings.card_text_color,
            "layout": settings.layout_type,
            "uid": current_user.id
        })
    else:
        db.execute(text("""
            INSERT INTO dashboard_settings 
            (user_id, website_name, primary_color, background_color, sidebar_color, button_color, text_color, sidebar_active_color, card_color, card_text_color, layout_type)
            VALUES (:uid, :name, :primary, :bg, :sidebar, :button, :text, :sidebar_active, :card, :card_text, :layout)
        """), {
            "uid": current_user.id,
            "name": settings.website_name,
            "primary": settings.primary_color,
            "bg": settings.background_color,
            "sidebar": settings.sidebar_color,
            "button": settings.button_color,
            "text": settings.text_color,
            "sidebar_active": settings.sidebar_active_color,
            "card": settings.card_color,
            "card_text": settings.card_text_color,
            "layout": settings.layout_type
        })
    
    db.commit()
    return {"message": "Settings saved successfully"}

@router.get("/modules", response_model=List[DashboardModuleResponse])
def get_dashboard_modules(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = db.execute(
        text("SELECT * FROM dashboard_modules WHERE user_id = :uid ORDER BY position"),
        {"uid": current_user.id}
    ).fetchall()
    
    modules = []
    for row in result:
        modules.append({
            "id": row[0],
            "module_name": row[2],
            "module_type": row[3],
            "title": row[4],
            "position": row[5],
            "width": row[6],
            "is_visible": row[7],
            "config": row[8] or {}
        })
    
    return modules

@router.post("/modules")
def create_dashboard_module(module: DashboardModule, db: Session = Depends(get_db), current_user = Depends(is_superadmin)):
    import json
    result = db.execute(text("""
        INSERT INTO dashboard_modules 
        (user_id, module_name, module_type, title, position, width, is_visible, config)
        VALUES (:uid, :name, :type, :title, :pos, :width, :visible, :config)
        RETURNING id
    """), {
        "uid": current_user.id,
        "name": module.module_name,
        "type": module.module_type,
        "title": module.title,
        "pos": module.position,
        "width": module.width,
        "visible": module.is_visible,
        "config": json.dumps(module.config) if module.config else None
    })
    
    db.commit()
    module_id = result.fetchone()[0]
    return {"id": module_id, "message": "Module created successfully"}

@router.put("/modules/{module_id}")
def update_dashboard_module(module_id: int, module: DashboardModule, db: Session = Depends(get_db), current_user = Depends(is_superadmin)):
    import json
    db.execute(text("""
        UPDATE dashboard_modules 
        SET module_name = :name, module_type = :type, title = :title, 
            position = :pos, width = :width, is_visible = :visible, 
            config = :config, updated_at = CURRENT_TIMESTAMP
        WHERE id = :id AND user_id = :uid
    """), {
        "id": module_id,
        "uid": current_user.id,
        "name": module.module_name,
        "type": module.module_type,
        "title": module.title,
        "pos": module.position,
        "width": module.width,
        "visible": module.is_visible,
        "config": json.dumps(module.config) if module.config else None
    })
    
    db.commit()
    return {"message": "Module updated successfully"}

@router.delete("/modules/{module_id}")
def delete_dashboard_module(module_id: int, db: Session = Depends(get_db), current_user = Depends(is_superadmin)):
    db.execute(
        text("DELETE FROM dashboard_modules WHERE id = :id AND user_id = :uid"),
        {"id": module_id, "uid": current_user.id}
    )
    db.commit()
    return {"message": "Module deleted successfully"}
