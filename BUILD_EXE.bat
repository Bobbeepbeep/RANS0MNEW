@echo off
title Build RANSOM Safe Simulator
cd /d "%~dp0"
py -m pip install --upgrade pyinstaller pillow
py -m PyInstaller --noconfirm --clean --onefile --windowed --name "RANSOMTRIAGE" --add-data "assets;assets" RANSOM_SIM.py
echo.
echo Build finished. Your EXE is in the dist folder.
pause
