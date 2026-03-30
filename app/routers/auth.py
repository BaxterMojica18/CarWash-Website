from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app import schemas, crud, database
from app.dependencies import get_current_user, oauth2_scheme
from app.permissions import get_user_permissions, is_admin_or_owner
from app.email_service import send_password_reset_email, send_otp_email
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

@router.post("/firebase-login", response_model=schemas.Token)
def firebase_login(request: schemas.FirebaseLoginRequest, db: Session = Depends(database.get_db)):
    from app.firebase_auth import verify_firebase_token
    
    try:
        # Verify the Firebase Token
        decoded_token = verify_firebase_token(request.id_token)
        
        # Ensure the token email matches the request email for security
        if decoded_token.get("email") != request.email:
            raise HTTPException(status_code=401, detail="Token email mismatch")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
        
    # Get or create the local PostgreSQL user
    user = crud.get_or_create_firebase_user(db, email=request.email, name=request.display_name)
    
    # Generate the app's standard JWT so the rest of the application works seamlessly
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
def get_my_permissions(current_user: database.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    roles = [role.name for role in current_user.roles]
    permissions = get_user_permissions(current_user)
    
    hidden_tabs = []
    role_ids = [r.id for r in current_user.roles]
    if role_ids:
        hidden_settings = db.query(database.RoleSidebarSetting).filter(
            database.RoleSidebarSetting.role_id.in_(role_ids),
            database.RoleSidebarSetting.is_visible == False
        ).all()
        hidden_tabs = list(set([s.page_name for s in hidden_settings]))
        
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": roles,
        "permissions": permissions,
        "hidden_sidebar_tabs": hidden_tabs
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
        
        hidden_tabs = []
        role_ids = [r.id for r in user.roles]
        if role_ids:
            hidden_settings = db.query(database.RoleSidebarSetting).filter(
                database.RoleSidebarSetting.role_id.in_(role_ids),
                database.RoleSidebarSetting.is_visible == False
            ).all()
            hidden_tabs = list(set([s.page_name for s in hidden_settings]))
            
        result.append({
            "user_id": user.id,
            "email": user.email,
            "roles": user_roles,
            "permissions": permissions,
            "hidden_sidebar_tabs": hidden_tabs
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
    
    hidden_tabs = []
    role_ids = [r.id for r in user.roles]
    if role_ids:
        hidden_settings = db.query(database.RoleSidebarSetting).filter(
            database.RoleSidebarSetting.role_id.in_(role_ids),
            database.RoleSidebarSetting.is_visible == False
        ).all()
        hidden_tabs = list(set([s.page_name for s in hidden_settings]))
    
    return {
        "user_id": user.id,
        "email": user.email,
        "roles": roles,
        "permissions": permissions,
        "hidden_sidebar_tabs": hidden_tabs
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
        result.append({"id": role.id, "name": role.name, "description": role.description, "permissions": perms})
    return result

@router.get("/roles/{role_id}/sidebar")
def get_role_sidebar_settings(role_id: int, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    settings = db.query(database.RoleSidebarSetting).filter(database.RoleSidebarSetting.role_id == role_id).all()
    return {s.page_name: s.is_visible for s in settings}

@router.put("/roles/{role_id}/sidebar")
def update_role_sidebar_settings(role_id: int, data: schemas.UpdateSidebarSettings, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    for page_name, is_visible in data.settings.items():
        setting = db.query(database.RoleSidebarSetting).filter(
            database.RoleSidebarSetting.role_id == role_id,
            database.RoleSidebarSetting.page_name == page_name
        ).first()
        if setting:
            setting.is_visible = is_visible
        else:
            setting = database.RoleSidebarSetting(role_id=role_id, page_name=page_name, is_visible=is_visible)
            db.add(setting)
    db.commit()
    return {"message": "Sidebar settings updated successfully"}

@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, http_request: Request, db: Session = Depends(database.get_db)):
    """Request a password reset. Sends either a reset link or OTP code based on user's choice."""
    user = crud.get_user_by_email(db, request.email)
    reset_method = request.reset_method or "link"
    
    # If not found locally, check if they exist in Firebase Auth 
    # (they might have registered via Firebase but never logged in locally yet)
    if not user:
        try:
            from firebase_admin import auth as firebase_auth
            fb_user = firebase_auth.get_user_by_email(request.email)
            # Create them locally so password reset tokens can be associated
            user = crud.get_or_create_firebase_user(
                db, 
                email=request.email, 
                name=fb_user.display_name or "User"
            )
            print(f"[AUTH] Recovered Firebase user {request.email} into local DB for password reset.")
        except Exception as e:
            pass # User doesn't exist anywhere
    
    if user:
        reset_data = crud.create_password_reset_token(db, user.id)
        reset_token = reset_data["token"]
        otp_code = reset_data["otp_code"]
        base_url = str(http_request.base_url).rstrip("/")
        
        email_sent = False
        if reset_method == "otp":
            email_sent = send_otp_email(request.email, otp_code)
        else:
            email_sent = send_password_reset_email(request.email, reset_token, base_url)
        
        if not email_sent:
            # Fallback: log to console if email fails
            print(f"\n{'='*50}")
            print(f"PASSWORD RESET for {request.email} (method: {reset_method})")
            print(f"Token: {reset_token}")
            print(f"OTP Code: {otp_code}")
            print(f"Reset URL: {base_url}/reset-password.html?token={reset_token}")
            print(f"Expires in 15 minutes")
            print(f"{'='*50}\n")
    
    if reset_method == "otp":
        msg = "If an account with that email exists, a 6-digit verification code has been sent."
    else:
        msg = "If an account with that email exists, a password reset link has been sent."
    
    return {"message": msg}

@router.post("/verify-otp")
def verify_otp(request: schemas.VerifyOtpRequest, db: Session = Depends(database.get_db)):
    """Verify a 6-digit OTP code. Returns the reset token if valid."""
    token = crud.validate_otp_code(db, request.email, request.otp_code)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    return {"message": "Code verified successfully", "token": token}

@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    """Reset password using a valid token."""
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    user = crud.validate_password_reset_token(db, request.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    crud.reset_password(db, user.id, request.new_password)
    crud.invalidate_reset_token(db, request.token)
    
    # Try to update the matching user's password in Firebase Auth as well
    try:
        from firebase_admin import auth as firebase_auth
        try:
            firebase_user = firebase_auth.get_user_by_email(user.email)
            firebase_auth.update_user(firebase_user.uid, password=request.new_password)
            print(f"[AUTH] Successfully synced new password to Firebase for {user.email}")
        except firebase_auth.UserNotFoundError:
            print(f"[AUTH] Firebase user not found for {user.email}, skipping Firebase password update.")
    except Exception as e:
        print(f"[AUTH] Warning: Failed to sync password to Firebase: {e}")
    
    return {"message": "Password has been reset successfully. You can now log in with your new password."}


