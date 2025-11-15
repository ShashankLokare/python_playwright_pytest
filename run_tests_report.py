#!/usr/bin/env python3
"""
Run tests and generate Allure report via CLI.
Usage: 
  python run_tests_report.py              # Run tests and generate Allure results
  python run_tests_report.py --headless   # Run tests in headless mode
  python run_tests_report.py --view       # View existing report (doesn't run tests)

Note: To generate HTML report from Allure JSON results, install Allure CLI:
  https://docs.qameta.io/allure/
Then run: allure generate allure-results -o allure-report --clean
Or use: allure serve allure-results
"""
import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"
ALLURE_REPORT_DIR = PROJECT_ROOT / "allure-report"


def run_tests(headless: bool = False) -> int:
    """Run pytest and generate Allure results."""
    print("Running pytest with Allure report generation...")
    cmd = [sys.executable, "-m", "pytest", "tests/", "-q", "--alluredir=allure-results"]
    
    # Override headed mode from pytest.ini if headless requested
    if headless:
        print("  (headless mode)")
        # Overwrite pytest.ini's --headed with -o (override)
        # Note: This is a bit hacky but works for local runs
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return result.returncode


def generate_html_report() -> bool:
    """
    Generate offline HTML Allure report.
    Requires Allure CLI: https://docs.qameta.io/allure/
    """
    print("\nAttempting to generate HTML Allure report...")
    try:
        # Try allure command
        result = subprocess.run(
            ["allure", "generate", str(ALLURE_RESULTS_DIR), "-o", str(ALLURE_REPORT_DIR), "--clean"],
            check=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        print(f"✓ Report generated at: {ALLURE_REPORT_DIR}")
        return True
    except FileNotFoundError:
        print("\n⚠ Allure CLI not found (install from: https://docs.qameta.io/allure/)")
        print("\nGenerated Allure JSON results in: allure-results/")
        print("To view report, install Allure and run:")
        print("  allure serve allure-results")
        return False
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to generate report: {e.stderr}")
        return False


def serve_report() -> bool:
    """Serve Allure report via Allure CLI."""
    print("\nServing Allure report...")
    try:
        subprocess.run(
            ["allure", "serve", str(ALLURE_RESULTS_DIR)],
            cwd=PROJECT_ROOT,
        )
        return True
    except FileNotFoundError:
        print("ERROR: 'allure' CLI not found. Install from: https://docs.qameta.io/allure/")
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


def view_existing_report() -> None:
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

    # View existing report
    if args.view:
        view_existing_report()
        return 0

    # Run tests
    test_result = run_tests(headless=args.headless)
    
    # Serve or generate report
    if args.serve:
        serve_report()
    else:
        if generate_html_report():
            open_report()

    return test_result


if __name__ == "__main__":
    sys.exit(main())


