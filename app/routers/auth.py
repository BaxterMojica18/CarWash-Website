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

@router.post("/register")
def register(reg_data: schemas.UserRegister, db: Session = Depends(database.get_db)):
    try:
        user = crud.register_user(db, reg_data)
        return {"message": "Success", "user_id": user.id, "business_number": user.business_number}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    biz = current_user.business_number or '__global__'
    if True: # unconditional fetch for the user
        user_hidden_settings = db.query(database.UserSidebarSetting).filter(
            database.UserSidebarSetting.user_id == current_user.id,
            database.UserSidebarSetting.is_visible == False,
            database.UserSidebarSetting.business_number == biz
        ).all()
        hidden_tabs = list(set([s.page_name for s in user_hidden_settings]))
        
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": roles,
        "permissions": permissions,
        "hidden_sidebar_tabs": hidden_tabs,
        "business_number": current_user.business_number
    }

@router.get("/users", response_model=List[schemas.UserPermissions])
def list_users(db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    # Scope users to the same business
    if current_user.business_number:
        users = db.query(database.User).filter(
            database.User.business_number == current_user.business_number
        ).all()
    else:
        users = db.query(database.User).all()
    
    current_user_roles = [role.name for role in current_user.roles]
    is_superadmin_user = "superadmin" in current_user_roles
    
    result = []
    for user in users:
        user_roles = [role.name for role in user.roles if not role.name.startswith('custom_')]
        
        # Hide superadmin users from non-superadmin users
        if "superadmin" in user_roles and not is_superadmin_user:
            continue
            
        # Hide soft-deleted users
        if user.is_active is False:
            continue
        
        permissions = get_user_permissions(user)
        
        hidden_tabs = []
        biz = user.business_number or '__global__'
        if True: # unconditional fetch for the user
            hidden_settings = db.query(database.UserSidebarSetting).filter(
                database.UserSidebarSetting.user_id == user.id,
                database.UserSidebarSetting.is_visible == False,
                database.UserSidebarSetting.business_number == biz
            ).all()
            hidden_tabs = list(set([s.page_name for s in hidden_settings]))
            
        result.append({
            "user_id": user.id,
            "email": user.email,
            "roles": user_roles,
            "permissions": permissions,
            "hidden_sidebar_tabs": hidden_tabs,
            "business_number": user.business_number
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
    biz = user.business_number or '__global__'
    if True: # unconditional fetch for the user
        hidden_settings = db.query(database.UserSidebarSetting).filter(
            database.UserSidebarSetting.user_id == user.id,
            database.UserSidebarSetting.is_visible == False,
            database.UserSidebarSetting.business_number == biz
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

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
    if current_user.business_number and user.business_number != current_user.business_number:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
        
    import datetime
    timestamp = int(datetime.datetime.now().timestamp())
    
    # Soft delete: prefix email to allow registering and reuse, wipe out roles to disable access
    user.email = f"deleted_{timestamp}_{user.id}_{user.email}"
    user.password_hash = "disabled"
    user.is_active = False
    user.deleted_at = datetime.datetime.now()
    user.roles.clear()
    
    db.commit()
    return {"message": "User soft deleted successfully"}

@router.get("/roles/all")
def get_all_roles(db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    roles = db.query(database.Role).filter(~database.Role.name.startswith('custom_')).all()
    result = []
    for role in roles:
        perms = [p.name for p in role.permissions]
        result.append({"id": role.id, "name": role.name, "description": role.description, "permissions": perms})
    return result

@router.get("/users/{user_id}/sidebar")
def get_user_sidebar_settings(user_id: int, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    biz = current_user.business_number or '__global__'
    settings = db.query(database.UserSidebarSetting).filter(
        database.UserSidebarSetting.user_id == user_id,
        database.UserSidebarSetting.business_number == biz
    ).all()
    return {s.page_name: s.is_visible for s in settings}

@router.put("/users/{user_id}/sidebar")
def update_user_sidebar_settings(user_id: int, data: schemas.UpdateSidebarSettings, db: Session = Depends(database.get_db), current_user: database.User = Depends(is_admin_or_owner)):
    biz = current_user.business_number or '__global__'
    for page_name, is_visible in data.settings.items():
        setting = db.query(database.UserSidebarSetting).filter(
            database.UserSidebarSetting.user_id == user_id,
            database.UserSidebarSetting.page_name == page_name,
            database.UserSidebarSetting.business_number == biz
        ).first()
        if setting:
            setting.is_visible = is_visible
        else:
            setting = database.UserSidebarSetting(user_id=user_id, page_name=page_name, is_visible=is_visible, business_number=biz)
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
    
    # Note: Only OTP method is used now.
    
    if user:
        reset_data = crud.create_password_reset_token(db, user.id)
        reset_token = reset_data["token"]
        otp_code = reset_data["otp_code"]
        
        email_sent = send_otp_email(request.email, otp_code)
        
        if not email_sent:
            # Fallback for dev: log to console
            print(f"\n{'='*50}")
            print(f"FAILED TO SEND EMAIL. Console fallback link:")
            print(f"PASSWORD RESET for {request.email} (method: otp)")
            print(f"OTP Code: {otp_code}")
            print(f"Expires in 15 minutes")
            print(f"{'='*50}\n")
            
            raise HTTPException(
                status_code=500, 
                detail="Failed to send the email due to server configuration or firewall blocking. (Check if Render is blocking port 587). The OTP code was printed to the server console."
            )
    
    msg = "If an account with that email exists, a 6-digit verification code has been sent."
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


