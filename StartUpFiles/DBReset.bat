@echo off
start cmd /c "cd .. && call NAIPEnv\Scripts\activate.bat && cd PlateCheck && del db.sqlite3 && python manage.py migrate"
echo DB has been reset.
pause