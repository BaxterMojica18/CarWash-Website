# -*- coding: utf-8 -*-
"""
Create superadmin role and owner account
"""
from app.database import SessionLocal, User, Role, Permission, role_permissions
from app.crud import create_user

def create_superadmin():
    db = SessionLocal()
    
    try:
        superadmin_role = db.query(Role).filter(Role.name == "superadmin").first()
        if not superadmin_role:
            superadmin_role = Role(name="superadmin", description="Super Administrator - Full system control")
            db.add(superadmin_role)
            db.commit()
            print("Created superadmin role")
        
        all_perms = db.query(Permission).all()
        db.execute(role_permissions.delete().where(role_permissions.c.role_id == superadmin_role.id))
        for perm in all_perms:
            db.execute(role_permissions.insert().values(role_id=superadmin_role.id, permission_id=perm.id))
        db.commit()
        
        owner = db.query(User).filter(User.email == "owner@carwash.com").first()
        if not owner:
            owner = create_user(db, "owner@carwash.com", "owner123", is_demo=False)
            owner.roles.append(superadmin_role)
            db.commit()
            print("Created owner@carwash.com (password: owner123)")
        else:
            if superadmin_role not in owner.roles:
                owner.roles.clear()
                owner.roles.append(superadmin_role)
                db.commit()
            print("owner@carwash.com already exists - updated to superadmin")
        
        print("\n" + "="*60)
        print("SUPERADMIN ACCOUNT CREATED")
        print("="*60)
        print("\nLogin Credentials:")
        print("Email: owner@carwash.com")
        print("Password: owner123")
        print("\nRole: superadmin")
        print("Access: Full system control, manages all users including admins")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_superadmin()
