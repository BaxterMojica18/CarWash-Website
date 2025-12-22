@echo off
echo ========================================
echo PERMISSION SYSTEM SETUP
echo ========================================
echo.

echo Step 1: Creating permission tables...
python add_permissions.py
echo.

echo Step 2: Assigning roles to users...
python assign_user_roles.py
echo.

echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Now you can test the permissions:
echo   python test_permissions.py
echo.
pause
