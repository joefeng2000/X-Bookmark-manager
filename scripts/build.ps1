# 构建完整应用

Write-Host "Building X Bookmark Manager..." -ForegroundColor Green

# 构建前端
Write-Host "`nBuilding Frontend..." -ForegroundColor Yellow
cd frontend
npm run build
cd ..

# 构建Docker镜像
Write-Host "`nBuilding Docker Image..." -ForegroundColor Yellow
docker build -t x-bookmark-manager:latest .

Write-Host "`nBuild completed successfully!" -ForegroundColor Green
