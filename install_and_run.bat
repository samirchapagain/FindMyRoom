@echo off
cd /d "C:\myproject"
echo Installing Django and dependencies...
pip install Django>=4.2
pip install Pillow
pip install channels>=4.0.0
pip install channels-redis>=4.1.0
pip install redis>=4.5.0
pip install stripe>=5.0.0
echo.
echo Running migrations...
python manage.py migrate
echo.
echo Starting server...
python manage.py runserver