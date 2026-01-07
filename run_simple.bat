@echo off
cd /d "C:\myproject"
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver