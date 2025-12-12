Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "LLM Safety Gateway - Installation Check" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

$errors = 0

# Check Python
Write-Host "`n[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    $errors++
}

# Check Node.js
Write-Host "`n[2/6] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found" -ForegroundColor Red
    $errors++
}

# Check npm
Write-Host "`n[3/6] Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm not found" -ForegroundColor Red
    $errors++
}

# Check virtual environment
Write-Host "`n[4/6] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "  ! Virtual environment not found - will be created on first run" -ForegroundColor Yellow
}

# Check requirements.txt
Write-Host "`n[5/6] Checking requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  ✓ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    $errors++
}

# Check frontend dependencies
Write-Host "`n[6/6] Checking frontend setup..." -ForegroundColor Yellow
if (Test-Path "frontend/package.json") {
    Write-Host "  ✓ package.json found" -ForegroundColor Green
    if (Test-Path "frontend/node_modules") {
        Write-Host "  ✓ node_modules installed" -ForegroundColor Green
    } else {
        Write-Host "  ! node_modules not found - run 'npm install' in frontend/" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ Frontend package.json not found" -ForegroundColor Red
    $errors++
}

# Check .env file
Write-Host "`n[Extra] Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  ! .env file not found - create one with your GEMINI_API_KEY" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Cyan
if ($errors -eq 0) {
    Write-Host "✓ Installation Check Complete - No critical errors!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor White
    Write-Host "  1. Install frontend dependencies: cd frontend && npm install" -ForegroundColor Gray
    Write-Host "  2. Create .env file with your GEMINI_API_KEY" -ForegroundColor Gray
    Write-Host "  3. Run: .\start.ps1" -ForegroundColor Gray
} else {
    Write-Host "✗ Installation Check Failed - $errors error(s) found" -ForegroundColor Red
    Write-Host "`nPlease fix the errors above before running the application." -ForegroundColor Yellow
}
Write-Host "=" * 60 -ForegroundColor Cyan

Read-Host "`nPress Enter to exit"
