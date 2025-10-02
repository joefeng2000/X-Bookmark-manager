@echo off
echo Starting X Bookmark Manager Development Environment...

start cmd /k "cd backend && .\\venv\\Scripts\\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start cmd /k "cd frontend && npm run dev"

echo Development servers starting...
echo Backend: <http://localhost:8000>
echo Frontend: <http://localhost:3000>
echo API Docs: <http://localhost:8000/docs>
