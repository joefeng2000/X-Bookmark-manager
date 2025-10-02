# 启动开发环境

Write-Host "Starting X Bookmark Manager Development Environment..." -ForegroundColor Green

# 启动后端
Write-Host "`nStarting Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\\venv\\Scripts\\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# 等待2秒
Start-Sleep -Seconds 2

# 启动前端
Write-Host "`nStarting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`nDevelopment servers starting..." -ForegroundColor Green
Write-Host "Backend: <http://localhost:8000>" -ForegroundColor Cyan
Write-Host "Frontend: <http://localhost:3000>" -ForegroundColor Cyan
Write-Host "API Docs: <http://localhost:8000/docs>" -ForegroundColor Cyan
