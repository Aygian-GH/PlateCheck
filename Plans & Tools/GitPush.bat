@echo off
git add .
$commitName = Read-Host -Prompt "Enter Commit Text: "
git commit -m "$commitName"

git remote add origin https://github.com/Aygian-GH/PlateCheck.git
git branch -M main
git push -u origin main
pause