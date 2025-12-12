# Start Script for LLM Safety Gateway

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Starting LLM Safety Gateway" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if requirements are installed
Write-Host "Checking backend dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Start backend in a new window
Write-Host "`nStarting FastAPI backend on http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.\venv\Scripts\Activate.ps1'; uvicorn main:app --reload"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "`nStarting React frontend on http://localhost:3000" -ForegroundColor Green
Write-Host "If this is your first time, run 'npm install' in the frontend directory first." -ForegroundColor Yellow
Start-Sleep -Seconds 2

Set-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start"

Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Services Starting!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "`nBackend: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop this script (services will keep running)" -ForegroundColor Yellow
Write-Host "Close the PowerShell windows to stop the services" -ForegroundColor Yellow

# Keep this window open
Read-Host "`nPress Enter to exit"
