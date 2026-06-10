@echo off
set /p commitName="Enter Commit Text: "

git add .
git commit -m "%commitName%"
git push

pause