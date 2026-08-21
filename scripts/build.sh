#!/bin/bash

# TaskFlow Build Script
# Creates standalone executable using PyInstaller

set -e

echo "TaskFlow Build Script"
echo "====================="

# Configuration
APP_NAME="TaskFlow"
VERSION="1.0.0"
MAIN_SCRIPT="main.py"
OUTPUT_DIR="dist"
BUILD_DIR="build"

# Parse arguments
CLEAN=false
DEV=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --dev)
            DEV=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create assets if they don't exist
echo "Checking assets..."
if [ ! -d "assets/icons" ] || [ ! -f "assets/icons/app_icon.png" ]; then
    echo "Generating placeholder icons..."
    python scripts/create_icons.py
fi

# Clean previous builds
if [ "$CLEAN" = true ]; then
    echo "Cleaning previous builds..."
    rm -rf "$OUTPUT_DIR" "$BUILD_DIR" *.spec
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build command
if [ "$DEV" = true ]; then
    echo "Creating development build..."
    pyinstaller \
        --name "$APP_NAME" \
        --windowed \
        --onefile \
        --icon "assets/icons/app_icon.png" \
        --add-data "assets/icons:assets/icons" \
        --add-data "assets/images:assets/images" \
        --hidden-import "sqlalchemy.sql.default_comparator" \
        --hidden-import "apscheduler.triggers.date" \
        --hidden-import "apscheduler.triggers.interval" \
        --hidden-import "apscheduler.triggers.cron" \
        "$MAIN_SCRIPT"
else
    echo "Creating production build..."
    pyinstaller \
        --name "$APP_NAME" \
        --windowed \
        --onefile \
        --icon "assets/icons/app_icon.png" \
        --add-data "assets/icons:assets/icons" \
        --add-data "assets/images:assets/images" \
        --hidden-import "sqlalchemy.sql.default_comparator" \
        --hidden-import "apscheduler.triggers.date" \
        --hidden-import "apscheduler.triggers.interval" \
        --hidden-import "apscheduler.triggers.cron" \
        --clean \
        --noconfirm \
        "$MAIN_SCRIPT"
fi

echo ""
echo "Build complete!"
echo "Executable located at: $OUTPUT_DIR/$APP_NAME"