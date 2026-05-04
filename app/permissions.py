from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.dependencies import get_current_user

def has_permission(permission_name: str):
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Get user roles and permissions
        user_permissions = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)
        
        if permission_name not in user_permissions:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return current_user
    return permission_checker

def get_user_permissions(user: User):
    permissions = set()
    for role in user.roles:
        for perm in role.permissions:
            permissions.add(perm.name)
    return list(permissions)

def is_admin_or_owner(current_user: User = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    if "admin" not in role_names and "owner" not in role_names and "superadmin" not in role_names:
        raise HTTPException(status_code=403, detail="Admin or Owner access required")
    return current_user

def is_superadmin(current_user: User = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    if "superadmin" not in role_names:
        raise HTTPException(status_code=403, detail="Superadmin access required")
    return current_user

def is_client(current_user: User = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    # A user is a client if they have the client role OR if they don't have any staff/admin roles
    # (some systems default to client). Let's strictly check for client role and NO staff/admin roles.
    is_c = "client" in role_names
    is_staff_admin = any(r in role_names for r in ["staff", "admin", "owner", "superadmin"])
    
    if is_staff_admin or not is_c:
        # If they are staff/admin, they shouldn't access client endpoints
        raise HTTPException(status_code=403, detail="Client access only")
        
    return current_user

def is_staff_or_admin(current_user: User = Depends(get_current_user)):
    role_names = [role.name for role in current_user.roles]
    if not any(r in role_names for r in ["staff", "admin", "owner", "superadmin"]):
        raise HTTPException(status_code=403, detail="Staff or Admin access required")
    return current_user
