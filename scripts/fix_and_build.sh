#!/bin/bash

# Quick fix and build script
# Generates assets and rebuilds the application

set -e

echo "TaskFlow Quick Fix and Build"
echo "============================"

# Navigate to project root
cd "$(dirname "$0")/.."

# Create assets directories
echo "Creating asset directories..."
mkdir -p assets/icons assets/images

# Generate icons
echo "Generating placeholder icons..."
python scripts/create_icons.py

# Clean previous build
echo "Cleaning previous build..."
rm -rf dist build *.spec

# Run build
echo "Building application..."
python -m PyInstaller \
    --name TaskFlow \
    --windowed \
    --onefile \
    --icon assets/icons/app_icon.png \
    --add-data "assets/icons:assets/icons" \
    --add-data "assets/images:assets/images" \
    --hidden-import "sqlalchemy.sql.default_comparator" \
    --hidden-import "apscheduler.triggers.date" \
    --hidden-import "apscheduler.triggers.interval" \
    --hidden-import "apscheduler.triggers.cron" \
    --clean \
    --noconfirm \
    main.py

echo ""
echo "Build complete!"
echo "Executable: dist/TaskFlow"