#!/usr/bin/env python3
"""
Setup Allure CLI for local development.
Downloads Allure 2.35.1 if not already installed.

Requirements:
  - Java 8+ (Allure needs Java to run)
  - PowerShell or cmd (for ZIP extraction)

Usage:
  python setup_allure.py
  
Troubleshooting:
  If you get "JAVA_HOME is not set" error:
    1. Install Java: https://www.oracle.com/java/technologies/downloads/
    2. Set JAVA_HOME in environment variables to your Java installation
    3. Or install via package manager:
       - Windows: choco install openjdk11 (if Chocolatey installed)
       - Or use a conda environment: conda install openjdk
"""
import os
import sys
import zipfile
import subprocess
from pathlib import Path
from urllib.request import urlretrieve

PROJECT_ROOT = Path(__file__).parent
ALLURE_DIR = PROJECT_ROOT / "allure-2.35.1"
ALLURE_BIN = ALLURE_DIR / "bin" / ("allure.bat" if sys.platform == "win32" else "allure")
ALLURE_URL = "https://github.com/allure-framework/allure2/releases/download/2.35.1/allure-2.35.1.zip"


def check_java():
    """Check if Java is available."""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False


def download_allure():
    """Download Allure 2.35.1 if not already present."""
    if ALLURE_BIN.exists():
        print(f"✓ Allure already installed at: {ALLURE_DIR}")
        return True

    print(f"Downloading Allure 2.35.1 from GitHub...")
    try:
        zip_path = PROJECT_ROOT / "allure-2.35.1.zip"
        print(f"  URL: {ALLURE_URL}")
        urlretrieve(ALLURE_URL, zip_path)
        print(f"✓ Downloaded ({zip_path.stat().st_size / (1024*1024):.1f} MB)")
        
        print(f"Extracting to {ALLURE_DIR}...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(PROJECT_ROOT)
        zip_path.unlink()
        print(f"✓ Allure extracted successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to download/install Allure: {e}")
        return False


def verify_allure():
    """Verify Allure CLI is available."""
    try:
        result = subprocess.run(
            [str(ALLURE_BIN), "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✓ Allure verified: {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"✗ Failed to verify Allure: {e}")
    return False


def main():
    """Main setup flow."""
    print("\n=== Allure CLI Setup ===")
    
    # Check Java
    print("\nChecking Java...")
    if not check_java():
        print("✗ Java not found (required by Allure)")
        print("\nTo install Java:")
        print("  Windows:")
        print("    1. Download: https://www.oracle.com/java/technologies/downloads/")
        print("    2. Or use: choco install openjdk11 (requires Chocolatey)")
        print("    3. Or use: conda install openjdk")
        print("  macOS:")
        print("    brew install openjdk@11")
        print("  Linux:")
        print("    sudo apt-get install openjdk-11-jdk")
        return 1
    print("✓ Java found")
    
    if not download_allure():
        return 1
    
    # Skip verification if Java not available, but continue
    if verify_allure():
        print("\n✓ Allure setup complete!")
        print(f"\nTo use Allure locally, run:")
        print(f"  python run_tests_report.py              # Run tests and generate report")
        print(f"  python run_tests_report.py --view       # View existing report")
        print(f"  python run_tests_report.py --serve      # Serve live report")
        return 0
    else:
        print("\n✗ Allure verification failed (Java might not be properly installed)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
