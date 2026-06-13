@echo off

echo === Cleaning previous build artifacts ===

REM Clean PyInstaller output
if exist dist rmdir /S /Q dist
if exist build rmdir /S /Q build

REM Clean only Vite build output from backend static (preserves images and other assets)
if exist backend\app\static\assets rmdir /S /Q backend\app\static\assets
if exist backend\app\static\index.html del /Q backend\app\static\index.html

REM Clean frontend build output and cache
if exist frontend\dist rmdir /S /Q frontend\dist
if exist frontend\node_modules\.vite rmdir /S /Q frontend\node_modules\.vite

echo === Installing dependencies ===
pip install -r backend/requirements.txt
cd frontend
call npm install
call npm run build
cd ..

echo === Copying frontend build to backend ===
xcopy /Y /E "frontend\dist\*" "backend\app\static\"

echo === Building executable ===
pyinstaller backend/ssp_drift.spec --clean

echo === Done ===