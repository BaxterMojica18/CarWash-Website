from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app import schemas, crud, database
from app.dependencies import get_current_user, oauth2_scheme
from app.permissions import get_user_permissions, is_admin_or_owner
import os
from typing import Optional, List

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_optional_query(token: Optional[str] = Query(None), db: Session = Depends(database.get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, credentials.email)
    if not user or not crud.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    permissions = get_user_permissions(user)
    access_token = create_access_token(data={"sub": user.email, "is_demo": user.is_demo})
    return {"access_token": access_token, "token_type": "bearer", "is_demo": user.is_demo, "permissions": permissions}

@router.post("/demo-login", response_model=schemas.Token)
def demo_login(db: Session = Depends(database.get_db)):
    demo_email = "demo@carwash.com"
    demo_password = "demo123"
    
    user = crud.get_user_by_email(db, demo_email)
    if not user:
        user = crud.create_user(db, demo_email, demo_password, is_demo=True)
    
    permissions = get_user_permissions(user)
    access_token = create_access_token(data={"sub": user.email, "is_demo": user.is_demo})
    return {"access_token": access_token, "token_type": "bearer", "is_demo": user.is_demo, "permissions": permissions}

@router.get("/me/permissions", response_model=schemas.UserPermissions)
def get_my_permissions(current_user: database.User = Depends(get_current_user)):
    roles = [role.name for role in current_user.roles]
    permissions = get_user_permissions(current_user)
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": roles,
        "permissions": permissions
    }

@router.get("/users", response_model=List[schemas.UserPermissions])
def list_users(db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    users = db.query(database.User).all()
    current_user_roles = [role.name for role in current_user.roles]
    is_superadmin_user = "superadmin" in current_user_roles
    
    result = []
    for user in users:
        user_roles = [role.name for role in user.roles if not role.name.startswith('custom_')]
        
        # Hide superadmin users from non-superadmin users
        if "superadmin" in user_roles and not is_superadmin_user:
            continue
        
        permissions = get_user_permissions(user)
        result.append({
            "user_id": user.id,
            "email": user.email,
            "roles": user_roles,
            "permissions": permissions
        })
    return result

@router.post("/users")
def create_user(data: schemas.CreateUser, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    existing_user = crud.get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user with default password
    default_password = "password123"
    new_user = crud.create_user(db, data.email, default_password, is_demo=False)
    
    # Assign role
    role = db.query(database.Role).filter(database.Role.name == data.role).first()
    if role:
        new_user.roles.append(role)
        db.commit()
    
    return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/users/{user_id}")
def get_user_details(user_id: int, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = [role.name for role in user.roles]
    permissions = get_user_permissions(user)
    
    return {
        "user_id": user.id,
        "email": user.email,
        "roles": roles,
        "permissions": permissions
    }

@router.put("/users/roles")
def update_user_roles(data: schemas.UpdateUserRoles, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    user = db.query(database.User).filter(database.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.roles.clear()
    for role_name in data.roles:
        role = db.query(database.Role).filter(database.Role.name == role_name).first()
        if role:
            user.roles.append(role)
    
    db.commit()
    return {"message": "User roles updated successfully"}

@router.put("/users/permissions")
def update_user_permissions(data: schemas.UpdateUserPermissions, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    user = db.query(database.User).filter(database.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    custom_role_name = f"custom_{user.id}"
    custom_role = db.query(database.Role).filter(database.Role.name == custom_role_name).first()
    
    if not custom_role:
        custom_role = database.Role(name=custom_role_name, description=f"Custom permissions for user {user.id}")
        db.add(custom_role)
        db.commit()
    
    custom_role.permissions.clear()
    for perm_name in data.permissions:
        perm = db.query(database.Permission).filter(database.Permission.name == perm_name).first()
        if perm:
            custom_role.permissions.append(perm)
    
    if custom_role not in user.roles:
        user.roles.append(custom_role)
    
    db.commit()
    return {"message": "User permissions updated successfully"}

@router.get("/permissions/all")
def get_all_permissions(db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    permissions = db.query(database.Permission).all()
    return [{"name": p.name, "description": p.description} for p in permissions]

@router.get("/roles/all")
def get_all_roles(db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    roles = db.query(database.Role).filter(~database.Role.name.startswith('custom_')).all()
    result = []
    for role in roles:
        perms = [p.name for p in role.permissions]
        result.append({"name": role.name, "description": role.description, "permissions": perms})
    return result
