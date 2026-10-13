@echo off
title NutriGuide AI — Powered by IBM Granite
color 0A

echo.
echo  ============================================================
echo   NutriGuide AI - Personalized Nutrition Agentic Application
echo   Powered by IBM Granite LLM via IBM watsonx.ai
echo  ============================================================
echo.

:: ── Step 1: Check Python installation ──────────────────────────────────────
echo [1/5] Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please download Python 3.11+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
python --version
echo        Python found. OK.
echo.

:: ── Step 2: Check/Create virtual environment ───────────────────────────────
echo [2/5] Setting up virtual environment...
IF NOT EXIST "venv" (
    echo        Creating virtual environment...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo        Virtual environment created.
) ELSE (
    echo        Virtual environment already exists. Skipping.
)
echo.

:: ── Step 3: Activate venv & install dependencies ───────────────────────────
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Failed to install dependencies.
    echo  Please check your internet connection and try again.
    pause
    exit /b 1
)
echo        All dependencies installed successfully. OK.
echo.

:: ── Step 4: Check for .env file ────────────────────────────────────────────
echo [4/5] Checking environment configuration...
IF NOT EXIST ".env" (
    echo.
    echo  [NOTICE] .env file not found.
    echo  Copying .env.example to .env ...
    copy .env.example .env >nul
    echo.
    echo  ============================================================
    echo   ACTION REQUIRED — Configure your IBM watsonx.ai credentials
    echo  ============================================================
    echo.
    echo  1. Open the file: .env  (in the nutrition_ai folder)
    echo  2. Replace the following values with your IBM Cloud credentials:
    echo.
    echo     WATSONX_API_KEY=your_ibm_cloud_api_key_here
    echo     WATSONX_PROJECT_ID=your_project_id_here
    echo     WATSONX_URL=https://us-south.ml.cloud.ibm.com
    echo.
    echo  How to get credentials:
    echo    - Go to https://cloud.ibm.com/
    echo    - Create or open a watsonx.ai project
    echo    - Generate an API key from IAM
    echo.
    echo  NOTE: The app WILL run in demo mode without credentials.
    echo        Plans will be generated using built-in templates.
    echo.
    echo  Press any key to continue in DEMO MODE...
    pause >nul
) ELSE (
    echo        .env file found. OK.
)
echo.

:: ── Step 5: Create plans directory ────────────────────────────────────────
IF NOT EXIST "plans" mkdir plans

:: ── Step 6: Launch the application ────────────────────────────────────────
echo [5/5] Starting NutriGuide AI server...
echo.
echo  ============================================================
echo   Application is starting at: http://localhost:5000
echo  ============================================================
echo.
echo  Opening browser automatically in 3 seconds...
echo  (If browser does not open, navigate to http://localhost:5000)
echo.
echo  Press CTRL+C to stop the server.
echo.

:: Open browser after 3 second delay (background)
start /B cmd /C "timeout /T 3 /NOBREAK >nul && start http://localhost:5000"

:: Start Flask server
python app.py

echo.
echo  Server stopped.
pause
