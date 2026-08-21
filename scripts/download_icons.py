#!/usr/bin/env python3
"""
Download Material Icons font for TaskFlow.
"""

import sys
import urllib.request
from pathlib import Path

def download_file(url: str, destination: Path) -> bool:
    """Download file from URL."""
    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, destination)
        print(f"Saved to {destination}")
        return True
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

def main():
    """Download Material Icons fonts."""
    assets_dir = Path(__file__).parent.parent / 'assets'
    fonts_dir = assets_dir / 'fonts'
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Material Icons fonts
    fonts = [
        (
            "Material Icons Regular",
            "https://github.com/google/material-design-icons/raw/master/font/MaterialIcons-Regular.ttf",
            fonts_dir / "MaterialIcons-Regular.ttf",
        ),
        (
            "Material Icons Outlined",
            "https://github.com/google/material-design-icons/raw/master/font/MaterialIconsOutlined-Regular.otf",
            fonts_dir / "MaterialIconsOutlined-Regular.otf",
        ),
        (
            "Material Icons Round",
            "https://github.com/google/material-design-icons/raw/master/font/MaterialIconsRound-Regular.otf",
            fonts_dir / "MaterialIconsRound-Regular.otf",
        ),
    ]

    success = True
    for name, url, destination in fonts:
        print(f"\n{'='*50}")
        print(f"Processing: {name}")
        print(f"{'='*50}")

        if destination.exists():
            print(f"Already exists: {destination}")
            continue

        if not download_file(url, destination):
            success = False

    if success:
        print("\n* Material Icons downloaded successfully!")
        print(f"Location: {fonts_dir}")
    else:
        print("\n* Some downloads failed. Please check the URLs and try again.")
        print("You can also manually download from:")
        print("https://github.com/google/material-design-icons/tree/master/font")

if __name__ == '__main__':
    main()