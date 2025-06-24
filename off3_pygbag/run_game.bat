@echo off
cd /d "d:\buet classes\CSE 318 AI Lab\off3_pygbag"
echo Starting Chain Reaction Game Server...
python -m pygbag --serve --port 8000 --width 800 --height 600 main.py
pause
