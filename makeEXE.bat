pip install -r backend/requirements.txt
cd frontend
call npm install
call npm run build
cd ..
rm -r backend/app/static/*
cp -r frontend/dist/* backend/app/static/
pyinstaller backend/ssp_drift.spec