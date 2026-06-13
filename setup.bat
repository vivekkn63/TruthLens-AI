@echo off
REM Setup script for TruthLens AI on Windows

echo.
echo 🚀 TruthLens AI Setup Script
echo ==============================
echo.

REM Check Python
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo.
echo ⚙️  Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file from template
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your API keys:
    echo    - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys
    echo    - TAVILY_API_KEY: Get from https://tavily.com
) else (
    echo ✓ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo    1. Edit .env and add your API keys
echo    2. Run: python main.py
echo.
pause
