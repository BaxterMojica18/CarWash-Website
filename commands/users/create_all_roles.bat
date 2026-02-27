@echo off
echo Creating all roles and permissions...
echo.

REM Copy the script to the container (in case it was updated)
docker cp "commands/users/create_all_roles.py" carwashwebsite-web-1:/app/commands/users/create_all_roles.py

REM Run the script inside the container
docker-compose exec web python /app/commands/users/create_all_roles.py

echo.
echo Script completed!
pause