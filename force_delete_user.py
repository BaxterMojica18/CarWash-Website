from app.database import SessionLocal, User, UserProfile
from sqlalchemy import text

db = SessionLocal()
email = 'baxterdavid.mojica@gmail.com'
user = db.query(User).filter(User.email == email).first()

if user:
    # Use raw SQL to force delete across all related tables natively to avoid fetching all relationships manually
    db.execute(text(f"DELETE FROM role_permissions WHERE role_id IN (SELECT role_id FROM user_roles WHERE user_id = {user.id})")) # In case they own roles (rare)
    db.execute(text(f"DELETE FROM user_roles WHERE user_id = {user.id}"))
    db.execute(text(f"DELETE FROM user_profiles WHERE user_id = {user.id}"))
    db.execute(text(f"DELETE FROM user_preferences WHERE user_id = {user.id}"))
    db.execute(text(f"DELETE FROM password_reset_tokens WHERE user_id = {user.id}"))
    db.execute(text(f"DELETE FROM orders WHERE client_id = {user.id}"))
    db.execute(text(f"DELETE FROM reservations WHERE client_id = {user.id}"))
    db.execute(text(f"DELETE FROM cart_items WHERE client_id = {user.id}"))
    db.execute(text(f"DELETE FROM users WHERE id = {user.id}"))
    db.commit()
    print("User and all related records deleted cleanly.")
else:
    print("User not found.")
