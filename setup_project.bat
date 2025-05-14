@echo off
REM Setup script for the ADA project, handling both backend and frontend installations on Windows

echo Setting up ADA project...

REM Create and activate virtual environment for backend
echo Creating and activating virtual environment for backend...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    exit /b 1
)

REM Install backend dependencies
echo Installing backend dependencies...
python install_dependencies.py

REM Install frontend dependencies
echo Moving to frontend directory for npm install...
cd client\ada-online
if exist package.json (
    echo Found package.json, running npm install...
    npm install
) else (
    echo Error: package.json not found in client\ada-online directory.
    exit /b 1
)

echo Frontend setup complete. Returning to root directory.
cd ..\..

echo Project setup complete. Backend and frontend dependencies installed.
echo Deactivating virtual environment...
call venv\Scripts\deactivate.bat