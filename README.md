# python_playwright_pytest

Minimal Playwright + pytest setup with Page Object Model, Allure reports, uv package manager, and GitHub Actions CI/CD.

**Repository:** https://github.com/ShashankLokare/python_playwright_pytest

**GitHub Actions Status:** Tests run automatically on every push to `main`, `develop`, or `master` branches.

Prerequisites (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Install Playwright browsers

```powershell
python -m playwright install
```

Run tests

```powershell
pytest -q
```

Notes

- Tests use `pytest-playwright` fixtures (e.g., `page`).
- To run a single test file:

```powershell
pytest tests/test_example.py -q
```

Install the `uv` package from PyPI

The project includes the PyPI package `uv` in `requirements.txt`. To install it specifically (or if you add it later), run:

```powershell
pip install uv
```

Note: `uv` is a PyPI package — consult its PyPI/GitHub page for usage examples and documentation.

Allure Reports

Tests are configured to generate Allure reports by default (via `pytest.ini`). JSON report data is stored in `allure-results/`.

### Quick Start (No Extra Setup)

Run tests and view raw results:

```powershell
python -m pytest tests/ -q --alluredir=allure-results
```

Generated JSON reports are in `allure-results/`.

### Generate & View HTML Report (Requires Allure CLI)

To generate an HTML report, install Allure CLI and use the provided script:

```powershell
# Option 1: Install Allure via Chocolatey (Windows)
choco install allure

# Option 2: Install Allure via NPM
npm install -g allure-commandline

# Option 3: Install Allure via Scoop
scoop install allure
```

Then run:

```powershell
python run_tests_report.py
```

Or manually:

```powershell
python -m pytest tests/ -q --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure serve allure-results
```

### Script Options

```powershell
python run_tests_report.py              # Run tests and generate HTML report
python run_tests_report.py --headless   # Run tests in headless mode
python run_tests_report.py --serve      # Serve report with Allure CLI
python run_tests_report.py --view       # View existing report
```

### CI/CD

GitHub Actions automatically:
1. Runs tests with Allure report generation
2. Generates HTML report from results
3. Uploads both JSON and HTML artifacts
4. Comments on PRs with report link

Download artifacts from the Actions tab and open `index.html` in a browser to view the detailed report.
