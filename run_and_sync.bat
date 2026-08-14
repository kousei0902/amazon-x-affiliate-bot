@echo off
cd /d "%~dp0"
git pull --quiet
python -m src.main >> logs\run.log 2>&1
git add products.csv logs\run.log
git commit -m "auto: posting run %date% %time%" --quiet
git push --quiet
