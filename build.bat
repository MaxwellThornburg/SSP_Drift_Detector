@echo off
setlocal EnableDelayedExpansion

:: Configuration
set "BACKEND_DIR=backend"
set "FRONTEND_DIR=frontend"
set "APP_NAME=SSP_Drift_Detector"

:: Colors for output (requires Windows 10+)
set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "RESET=[0m"

:: Parse arguments
set "CLEAN=0"
set "DEV=0"
set "SKIP_PYTHON=0"
set "SKIP_FRONTEND=0"

:parse_args
if "%~1"=="" goto :done_parsing
if /I "%~1"=="-c" set "CLEAN=1" & shift & goto :parse_args
if /I "%~1"=="--clean" set "CLEAN=1" & shift & goto :parse_args
if /I "%~1"=="-d" set "DEV=1" & shift & goto :parse_args
if /I "%~1"=="--dev" set "DEV=1" & shift & goto :parse_args
if /I "%~1"=="--skip-python" set "SKIP_PYTHON=1" & shift & goto :parse_args
if /I "%~1"=="--skip-frontend" set "SKIP_FRONTEND=1" & shift & goto :parse_args
if /I "%~1"=="-h" goto :show_help
if /I "%~1"=="--help" goto :show_help
shift & goto :parse_args
:done_parsing

:: Show banner
echo %GREEN%========================================%RESET%
echo %GREEN%   SSP Drift Detector Build Script     %RESET%
echo %GREEN%========================================%RESET%
echo.

:: Check prerequisites
echo %BLUE%[INFO]%RESET% Checking prerequisites...

where python >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%RESET% Python not found in PATH
    exit /b 1
)

where npm >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%RESET% npm not found in PATH
    exit /b 1
)

:: Clean previous builds
if "%CLEAN%"=="1" (
    echo %YELLOW%[WARN]%RESET% Cleaning previous build artifacts...
    
    if exist "%FRONTEND_DIR%\dist" (
        echo   - Removing %FRONTEND_DIR%\dist...
        rmdir /S /Q "%FRONTEND_DIR%\dist"
    )
    
    if exist "%FRONTEND_DIR%\node_modules\.vite" (
        echo   - Removing %FRONTEND_DIR%\node_modules\.vite...
        rmdir /S /Q "%FRONTEND_DIR%\node_modules\.vite"
    )
    
    if exist "%BACKEND_DIR%\dist" (
        echo   - Removing %BACKEND_DIR%\dist...
        rmdir /S /Q "%BACKEND_DIR%\dist"
    )
    
    if exist "%BACKEND_DIR%\build" (
        echo   - Removing %BACKEND_DIR%\build...
        rmdir /S /Q "%BACKEND_DIR%\build"
    )

    if exist "%APP_NAME%.exe" (
        echo   - Removing old %APP_NAME%.exe...
        del /Q "%APP_NAME%.exe"
    )
    
    echo %GREEN%[INFO]%RESET% Clean complete.
    echo.
)

:: Install dependencies
if "%SKIP_PYTHON%"=="0" (
    echo %BLUE%[INFO]%RESET% Installing Python dependencies...
    cd "%BACKEND_DIR%"
    python -m pip install -r requirements.txt
    if !ERRORLEVEL! neq 0 (
        echo %RED%[ERROR]%RESET% Failed to install Python dependencies
        exit /b 1
    )
    cd ..
    echo.
)

if "%SKIP_FRONTEND%"=="0" (
    echo %BLUE%[INFO]%RESET% Installing Node dependencies...
    cd "%FRONTEND_DIR%"
    call npm install
    if !ERRORLEVEL! neq 0 (
        echo %RED%[ERROR]%RESET% Failed to install npm dependencies
        exit /b 1
    )
    
    echo %BLUE%[INFO]%RESET% Building frontend...
    call npm run build
    if !ERRORLEVEL! neq 0 (
        echo %RED%[ERROR]%RESET% Failed to build frontend
        exit /b 1
    )
    cd ..
    echo.
)

:: Dev mode
if "%DEV%"=="1" (
    echo %BLUE%[INFO]%RESET% Starting in development mode...
    start "Frontend Dev Server" cmd /c "cd %FRONTEND_DIR% && npm run dev"
    timeout /t 3 /nobreak >nul
    cd "%BACKEND_DIR%"
    python run_desktop.py
    exit /b 0
)

:: Build Python application with PyInstaller
if "%SKIP_PYTHON%"=="0" (
    echo %BLUE%[INFO]%RESET% Building Python application with PyInstaller...
    cd "%BACKEND_DIR%"
    
    :: Ensure frontend dist exists before bundling
    if not exist "..\%FRONTEND_DIR%\dist" (
        echo %RED%[ERROR]%RESET% Frontend dist folder not found. Please build the frontend first.
        exit /b 1
    )

    :: Build single executable, bundling the frontend dist folder
    python -m PyInstaller --onefile --windowed --name %APP_NAME% --clean --add-data "..\%FRONTEND_DIR%\dist;static" run_desktop.py
    
    if !ERRORLEVEL! neq 0 (
        echo %RED%[ERROR]%RESET% Failed to build Python application
        exit /b 1
    )
    cd ..
    echo.
    
    :: Copy to root
    echo %BLUE%[INFO]%RESET% Copying executable to project root...
    
    copy /Y "%BACKEND_DIR%\dist\%APP_NAME%.exe" "%APP_NAME%.exe" >nul
    if !ERRORLEVEL! neq 0 (
        echo %RED%[ERROR]%RESET% Failed to copy executable
        exit /b 1
    )
    
    echo.
    echo %GREEN%========================================%RESET%
    echo %GREEN%   Build Complete!                    %RESET%
    echo %GREEN%========================================%RESET%
    echo.
    echo Portable executable:
    echo   - %APP_NAME%.exe
    echo.
)

echo.
echo %GREEN%[INFO]%RESET% Done.
exit /b 0

:show_help
echo Usage: build.bat [options]
echo.
echo Options:
echo   -c, --clean          Clean previous builds before building
echo   -d, --dev            Run in development mode
echo   --skip-python        Skip Python build
echo   --skip-frontend      Skip npm install and frontend build
echo   -h, --help           Show this help message
echo.
echo Examples:
echo   build.bat                    Normal build
echo   build.bat -c                 Clean rebuild
echo   build.bat -d                 Run in dev mode
echo   build.bat --skip-python      Skip Python, build frontend only
exit /b 0