@echo off
echo ========================================
echo E-Commerce Feature Setup
echo ========================================
echo.

echo Step 1: Creating database tables...
python add_ecommerce_tables.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create tables
    pause
    exit /b 1
)
echo.

echo Step 2: Updating roles and permissions...
python seed_data.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to update roles
    pause
    exit /b 1
)
echo.

echo Step 3: Creating test client user...
python create_client_user.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create client user
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Running verification...
python verify_ecommerce.py
echo.
echo You can now start the server with:
echo   start_server.bat
echo.
echo Test the features:
echo   Client: http://localhost:8000/shop.html
echo   Login: client@carwash.com / client123
echo.
pause
