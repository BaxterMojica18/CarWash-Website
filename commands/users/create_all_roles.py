#!/usr/bin/env python3
"""
Create all roles and permissions for the Car Wash system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import get_db, User, Role, Permission, user_roles, role_permissions
from sqlalchemy.orm import Session

def create_permissions(db: Session):
    """Create all system permissions"""
    permissions = [
        ("manage_products", "Add, edit, delete products"),
        ("manage_locations", "Add, edit, delete washing bays"),
        ("view_locations", "View washing bays (read-only)"),
        ("manage_invoices", "Create, edit, delete invoices"),
        ("view_invoices", "View invoices (read-only)"),
        ("view_reports", "Access sales reports"),
        ("manage_settings", "Modify theme and settings"),
        ("manage_users", "Manage user permissions")
    ]
    
    created_permissions = {}
    for name, description in permissions:
        permission = db.query(Permission).filter(Permission.name == name).first()
        if not permission:
            permission = Permission(name=name, description=description)
            db.add(permission)
            print(f"✅ Created permission: {name}")
        else:
            print(f"⚠️  Permission already exists: {name}")
        created_permissions[name] = permission
    
    db.commit()
    return created_permissions

def create_roles(db: Session):
    """Create all system roles"""
    roles = [
        ("superadmin", "System owner with full access"),
        ("admin", "Administrator with management access"),
        ("user", "Staff member with limited access"),
        ("client", "Customer with basic access")
    ]
    
    created_roles = {}
    for name, description in roles:
        role = db.query(Role).filter(Role.name == name).first()
        if not role:
            role = Role(name=name, description=description)
            db.add(role)
            print(f"✅ Created role: {name}")
        else:
            print(f"⚠️  Role already exists: {name}")
        created_roles[name] = role
    
    db.commit()
    return created_roles

def assign_permissions_to_roles(db: Session, roles: dict, permissions: dict):
    """Assign permissions to roles based on the system matrix"""
    from sqlalchemy import delete
    
    role_permissions_data = {
        "superadmin": [
            "manage_products", "manage_locations", "view_locations",
            "manage_invoices", "view_invoices", "view_reports",
            "manage_settings", "manage_users"
        ],
        "admin": [
            "manage_products", "manage_locations", "view_locations",
            "manage_invoices", "view_invoices", "view_reports",
            "manage_settings"
        ],
        "user": [
            "view_locations", "manage_invoices", "view_invoices", "view_reports"
        ],
        "client": []
    }
    
    for role_name, permission_names in role_permissions_data.items():
        role = roles[role_name]
        
        # Clear existing permissions for this role
        db.execute(delete(role_permissions).where(role_permissions.c.role_id == role.id))
        
        # Assign new permissions
        for permission_name in permission_names:
            permission = permissions[permission_name]
            db.execute(role_permissions.insert().values(
                role_id=role.id,
                permission_id=permission.id
            ))
            print(f"✅ Assigned {permission_name} to {role_name}")
    
    db.commit()

def main():
    """Main function to create all roles and permissions"""
    print("🚀 Creating all roles and permissions for Car Wash system...")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Create permissions
        print("\n📋 Creating Permissions:")
        permissions = create_permissions(db)
        
        # Create roles
        print("\n👥 Creating Roles:")
        roles = create_roles(db)
        
        # Assign permissions to roles
        print("\n🔗 Assigning Permissions to Roles:")
        assign_permissions_to_roles(db, roles, permissions)
        
        print("\n" + "=" * 60)
        print("✅ Successfully created all roles and permissions!")
        print("\n📊 Summary:")
        print(f"   • Permissions: {len(permissions)}")
        print(f"   • Roles: {len(roles)}")
        print("\n🎯 Role Hierarchy:")
        print("   superadmin → admin → user → client")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return 1
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    exit(main())