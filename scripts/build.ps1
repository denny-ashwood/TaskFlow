# TaskFlow Windows Build Script
# Creates standalone executable using PyInstaller

param(
    [switch]$Clean,
    [switch]$Dev
)

Write-Host "TaskFlow Build Script" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

# Configuration
$AppName = "TaskFlow"
$Version = "1.0.0"
$MainScript = "main.py"
$OutputDir = "dist"
$BuildDir = "build"
$SpecFile = "taskflow.spec"

# Create assets if they don't exist
Write-Host "Checking assets..." -ForegroundColor Yellow
if (-not (Test-Path "assets/icons")) {
    Write-Host "Generating placeholder icons..." -ForegroundColor Yellow
    python scripts/create_icons.py
}

# Clean previous builds
if ($Clean) {
    Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
    Remove-Item -Path $OutputDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $SpecFile -Force -ErrorAction SilentlyContinue
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Build command
if ($Dev) {
    Write-Host "Creating development build..." -ForegroundColor Yellow
    pyinstaller `
        --name $AppName `
        --windowed `
        --onefile `
        --icon "assets/icons/app_icon.png" `
        --add-data "assets/icons;assets/icons" `
        --add-data "assets/images;assets/images" `
        --hidden-import "sqlalchemy.sql.default_comparator" `
        --hidden-import "apscheduler.triggers.date" `
        --hidden-import "apscheduler.triggers.interval" `
        --hidden-import "apscheduler.triggers.cron" `
        $MainScript
} else {
    Write-Host "Creating production build..." -ForegroundColor Yellow
    pyinstaller `
        --name $AppName `
        --windowed `
        --onefile `
        --icon "assets/icons/app_icon.png" `
        --add-data "assets/icons;assets/icons" `
        --add-data "assets/images;assets/images" `
        --hidden-import "sqlalchemy.sql.default_comparator" `
        --hidden-import "apscheduler.triggers.date" `
        --hidden-import "apscheduler.triggers.interval" `
        --hidden-import "apscheduler.triggers.cron" `
        --clean `
        --noconfirm `
        $MainScript
}

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "Executable located at: $OutputDir\$AppName.exe" -ForegroundColor Green