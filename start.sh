#!/bin/sh
set -e

echo "Running database migrations..."
python -c "from app.database import create_tables; create_tables()"
python commands/database/migrate_db.py || true
python commands/database/add_signup_columns.py || true
python commands/database/add_user_soft_delete_columns.py || true

# Run column migrations
python -c "
from sqlalchemy import text
from app.database import engine
c = engine.connect()
c.execute(text('ALTER TABLE settings_theme_selection ADD COLUMN IF NOT EXISTS for_client BOOLEAN DEFAULT FALSE'))
c.execute(text(\"ALTER TABLE role_sidebar_settings ADD COLUMN IF NOT EXISTS business_number VARCHAR DEFAULT '__global__'\"))
c.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE'))
c.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITHOUT TIME ZONE'))
c.execute(text('ALTER TABLE business_info ADD COLUMN IF NOT EXISTS business_sub_name VARCHAR'))
c.commit()
c.close()
print('Column migrations OK')
" || true

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
