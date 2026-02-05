@echo off
title AI Data Analysis Dashboard
echo 🚀 Initializing Data Dashboard...

:: 1. Ensure the script runs from the project folder
cd /d "%~dp0"

:: 2. Check if the 'venv' folder exists
if not exist "venv" (
    echo ---------------------------------------------------
    echo 📦 Virtual environment not found. Creating one...
    echo ---------------------------------------------------
    
    :: Create venv
    python -m venv venv
    
    :: Activate venv
    call venv\Scripts\activate
    
    :: Install libraries
    echo ⬇️ Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    
    echo.
    echo ✅ Setup complete!
) else (
    :: If venv exists, just activate it
    call venv\Scripts\activate
)

:: 3. Run the main Python script
echo.
echo 📈 Starting Application...
echo ---------------------------------------------------
python src/main.py

:: 4. Pause at the end so you can see errors if it crashes
echo.
if errorlevel 1 (
    echo ❌ The application crashed. See error above.
)
pause