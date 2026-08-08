@echo off
cd /d "%~dp0"
:: Use pythonw to hide the console window so only the hologram shows
start "" pythonw gui_core.py
