from app.database import SessionLocal, Role
from app import crud

db = SessionLocal()

# Create client user
client_user = crud.get_user_by_email(db, "client@carwash.com")
if not client_user:
    client_user = crud.create_user(db, "client@carwash.com", "client123", is_demo=False)
    print("✓ Client user created")
else:
    print("✓ Client user already exists")

# Assign client role
client_role = db.query(Role).filter(Role.name == "client").first()
if client_role and client_role not in client_user.roles:
    client_user.roles.append(client_role)
    db.commit()
    print("✓ Client role assigned")

print("\nClient Login:")
print("  Email: client@carwash.com")
print("  Password: client123")

db.close()
