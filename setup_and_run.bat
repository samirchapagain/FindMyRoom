@echo off
echo Setting up and running LuxeRooms Django Project
echo ================================================

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser (optional - will prompt)
echo.
echo To create an admin user, run: python manage.py createsuperuser
echo.

REM Start the development server
echo Starting Django development server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo ================================================
python manage.py runserver

pause