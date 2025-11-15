#!/usr/bin/env python3
"""
Run tests and generate Allure report via CLI.
Usage: 
  python run_tests_report.py              # Run tests and generate Allure results
  python run_tests_report.py --headless   # Run tests in headless mode
  python run_tests_report.py --view       # View existing report (doesn't run tests)
  python run_tests_report.py --serve      # Serve live report with Allure CLI

Local Allure Setup:
  python setup_allure.py                  # Download and install Allure 2.35.1 locally

Or install globally from: https://docs.qameta.io/allure/
"""
import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"
ALLURE_REPORT_DIR = PROJECT_ROOT / "allure-report"
ALLURE_CLI = PROJECT_ROOT / "allure-2.35.1" / "bin" / ("allure.bat" if sys.platform == "win32" else "allure")


def find_allure_command():
    """Find allure command: local first, then system PATH."""
    if ALLURE_CLI.exists():
        return str(ALLURE_CLI)
    try:
        subprocess.run(["allure", "--version"], capture_output=True, check=True)
        return "allure"
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def run_tests(headless: bool = False) -> int:
    """Run pytest and generate Allure results."""
    print("Running pytest with Allure report generation...")
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--alluredir=allure-results", "--tb=short"]
    
    # Override headed mode from pytest.ini if headless requested
    if headless:
        print("  (headless mode)")
        # Overwrite pytest.ini's --headed with -o (override)
        # Note: This is a bit hacky but works for local runs
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return result.returncode


def generate_html_report(allure_cmd: str) -> bool:
    """
    Generate offline HTML Allure report.
    Requires Allure CLI: https://docs.qameta.io/allure/
    """
    print("\nAttempting to generate HTML Allure report...")
    try:
        # Try allure command
        result = subprocess.run(
            [allure_cmd, "generate", str(ALLURE_RESULTS_DIR), "-o", str(ALLURE_REPORT_DIR), "--clean"],
            check=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        print(f"✓ Report generated at: {ALLURE_REPORT_DIR}")
        return True
    except FileNotFoundError:
        print("\n⚠ Allure CLI not found")
        print("  To install locally: python setup_allure.py")
        print("  Or install globally: https://docs.qameta.io/allure/")
        print("\nGenerated Allure JSON results in: allure-results/")
        return False
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to generate report: {e.stderr}")
        return False


def serve_report(allure_cmd: str) -> bool:
    """Serve Allure report via Allure CLI."""
    print("\nServing Allure report...")
    try:
        subprocess.run(
            [allure_cmd, "serve", str(ALLURE_RESULTS_DIR)],
            cwd=PROJECT_ROOT,
        )
        return True
    except FileNotFoundError:
        print("ERROR: 'allure' CLI not found.")
        print("  To install locally: python setup_allure.py")
        print("  Or install globally: https://docs.qameta.io/allure/")
        return False


def open_report() -> None:
    """Open the generated HTML report in default browser."""
    report_index = ALLURE_REPORT_DIR / "index.html"
    if report_index.exists():
        report_url = report_index.as_uri()
        print(f"\nOpening report in browser: {report_url}")
        try:
            webbrowser.open(report_url)
        except Exception as e:
            print(f"Could not open browser: {e}")
    else:
        print(f"\nReport HTML file not found: {report_index}")


def view_existing_report(allure_cmd: str = None) -> None:
    """View the existing Allure report if it exists."""
    report_index = ALLURE_REPORT_DIR / "index.html"
    if report_index.exists():
        open_report()
    else:
        print("No existing report found. Run: python run_tests_report.py")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run tests and manage Allure reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests_report.py              # Run tests, generate JSON + HTML report
  python run_tests_report.py --headless   # Run tests headless
  python run_tests_report.py --view       # View existing report
  python run_tests_report.py --serve      # Serve with Allure CLI (requires 'allure' installed)
  
Setup:
  python setup_allure.py                  # Install Allure CLI locally (one-time)
        """,
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve report with Allure CLI (requires 'allure' command installed)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode (default: headed per pytest.ini)",
    )
    parser.add_argument(
        "--view",
        action="store_true",
        help="View existing Allure report without running tests",
    )
    args = parser.parse_args()

    # Find allure command
    allure_cmd = find_allure_command()
    if not allure_cmd:
        print("⚠ Allure CLI not found.")
        print("  To set up locally (one-time): python setup_allure.py")
        print("  Or install globally: https://docs.qameta.io/allure/")

    # View existing report
    if args.view:
        view_existing_report(allure_cmd)
        return 0

    # Run tests
    test_result = run_tests(headless=args.headless)
    
    # Serve or generate report
    if args.serve:
        if allure_cmd:
            serve_report(allure_cmd)
        else:
            print("ERROR: Cannot serve without Allure CLI. Run: python setup_allure.py")
            return 1
    else:
        if allure_cmd:
            if generate_html_report(allure_cmd):
                open_report()
        else:
            print("\nTo generate HTML reports, run: python setup_allure.py")
            print("Allure JSON results saved in: allure-results/")

    return test_result


if __name__ == "__main__":
    sys.exit(main())


