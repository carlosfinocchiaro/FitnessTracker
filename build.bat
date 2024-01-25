@echo off
cd /d %~dp0
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=./FitnessTracker.ico FitnessTracker.py
move .\dist\FitnessTracker.exe .\FitnessTracker.exe
rd /s /q .\build
rd /s /q .\dist
del /f .\FitnessTracker.spec