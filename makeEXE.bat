pip install -r backend/requirements.txt
cd frontend
call npm install
call npm run build
cd ..
xcopy /Y /E "frontend\dist\*" "backend\app\static"
pyinstaller backend/ssp_drift.spec