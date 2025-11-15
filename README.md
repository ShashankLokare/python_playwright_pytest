# Python Playwright pytest Automation Framework

End-to-end test automation for https://demoblaze.com/ using Playwright, pytest, and Allure reporting.

## Features

- **Page Object Model (POM)** - Clean separation of test logic and page interactions
- **Playwright** - Cross-browser automation (headless/headed modes)
- **pytest** - Powerful test framework with fixtures
- **Allure Reports** - Beautiful, interactive test reports with steps, screenshots, and metrics
- **Local Allure CLI** - Set up Allure in one command
- **GitHub Actions CI/CD** - Automated testing on every push with artifact uploads

## Project Structure

```
python_playwright_pytest/
├── app/
│   └── pages/
│       ├── __init__.py
│       ├── locators.py          # Centralized CSS/XPath selectors
│       ├── base_page.py         # Base class for all page objects
│       ├── home_page.py         # DemoBlaze homepage interactions
│       ├── product_page.py      # Product detail page interactions
│       └── cart_page.py         # Shopping cart and checkout
├── tests/
│   ├── conftest.py              # pytest hooks (automatic screenshots on failure)
│   ├── test_buy_nexus6.py       # Main e2e test: Nexus 6 purchase flow
│   └── test_example.py          # Simple sanity test
├── pytest.ini                    # pytest configuration (headed mode, Allure)
├── pyproject.toml               # Project metadata
├── requirements.txt             # Python dependencies
├── setup_allure.py              # Setup script for local Allure CLI
├── run_tests_report.py          # Test runner with report generation
├── README.md
├── .gitignore
└── .github/
    └── workflows/
        └── test.yml             # GitHub Actions CI/CD workflow
```

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ShashankLokare/python_playwright_pytest.git
cd python_playwright_pytest
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Set Up Allure (One-time)
```bash
python setup_allure.py
```

This downloads Allure 2.35.1 to `allure-2.35.1/` locally. Skip this if you have Allure installed globally.

### 4. Run Tests
```bash
# Run tests and generate HTML report
python run_tests_report.py

# Run tests headless mode
python run_tests_report.py --headless

# View existing report
python run_tests_report.py --view

# Serve report with live updates
python run_tests_report.py --serve
```

Or use pytest directly:
```bash
pytest tests/ -v --alluredir=allure-results --headed
allure serve allure-results
```

## Configuration

### pytest.ini
```ini
[pytest]
addopts = -q --headed --alluredir=allure-results
testpaths = tests
```

Flags:
- `--headed` - Run browser in headed mode (visible window)
- `--alluredir=allure-results` - Save Allure results to this directory

### Playwright Pytest Fixtures
The `page` fixture from `pytest-playwright` is available in all test functions:
```python
def test_example(page):
    page.goto("https://example.com")
    assert "Example" in page.title()
```

## Test Details

### test_buy_nexus6.py
End-to-end purchase flow for Nexus 6 phone:
1. Open DemoBlaze homepage
2. Select "Nexus 6" product
3. Verify product details
4. Add to cart
5. Open shopping cart
6. Place order
7. Fill order form (name, country, etc.)
8. Complete purchase
9. Verify confirmation message

**Allure Annotations:**
- Feature: Shopping
- Story: Purchase Product
- Severity: Critical
- 9 detailed steps with screenshots

**Run:**
```bash
pytest tests/test_buy_nexus6.py -v
allure serve allure-results
```

## Page Object Model

### BasePage
Base class for all page objects, handles navigation:
```python
from app.pages.base_page import BasePage

class HomePage(BasePage):
    def open(self):
        self.goto("/index.html")
```

### Locators
Centralized CSS/XPath selectors:
```python
from app.pages.locators import Locators

class HomePage(BasePage):
    def select_product(self, product_name: str):
        self.page.click(Locators.PRODUCT_LINK_BY_NAME(product_name))
```

### Example: Using Page Objects
```python
def test_buy_nexus6(page):
    home_page = HomePage(page, "https://demoblaze.com")
    home_page.open()
    home_page.select_product("Nexus 6")
    
    product_page = ProductPage(page, "https://demoblaze.com")
    product_page.add_to_cart()
    
    cart_page = CartPage(page, "https://demoblaze.com")
    cart_page.open()
    cart_page.place_order()
    # ... continue with checkout
```

## Allure Reporting

### Local Setup (Recommended)
```bash
python setup_allure.py
```

Installs Allure 2.35.1 to `allure-2.35.1/` (portable, no system installation needed).

### Generate Reports
```bash
# Method 1: Using run_tests_report.py (recommended)
python run_tests_report.py          # Run tests + generate + open HTML report
python run_tests_report.py --serve  # Run tests + live serve with Allure CLI

# Method 2: Using pytest + Allure CLI directly
pytest tests/ -v --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure serve allure-results
```

### Report Features
- **Test steps** - Each action captured as a step with screenshot
- **Screenshots** - Attached at each step and on test failure
- **Metadata** - Feature, story, severity, duration, timing
- **Attachments** - Text, images, logs
- **Trends** - Historical test results and success rates

## GitHub Actions CI/CD

Automatically runs tests on every push to main branch and PR.

### Features
- Windows runner with Python 3.12
- Playwright chromium browser installed
- Allure 2.35.1 CLI downloaded from official release
- Artifacts uploaded: `allure-results/` (JSON) and `allure-report/` (HTML)
- 30-day retention
- PR comments with report link

### Workflow File
`.github/workflows/test.yml`

### View Results
1. Go to: https://github.com/ShashankLokare/python_playwright_pytest/actions
2. Click on workflow run
3. Download artifacts or view summary

## Running Tests Locally

### All Tests
```bash
pytest tests/ -v
```

### Specific Test File
```bash
pytest tests/test_buy_nexus6.py -v
pytest tests/test_example.py -v
```

### Specific Test Function
```bash
pytest tests/test_buy_nexus6.py::test_buy_nexus6 -v
```

### With Reports
```bash
python run_tests_report.py
python run_tests_report.py --headless
```

## Troubleshooting

### Allure CLI Not Found
```bash
python setup_allure.py
```

### Browser Not Found
```bash
python -m playwright install chromium
```

### Tests Fail - Check Screenshots
Screenshots are automatically captured on test failure in:
- `allure-results/` (in Allure JSON)
- Visible in Allure report

### Port Already in Use (allure serve)
Allure CLI picks a random port. If it fails, check:
```bash
netstat -ano | findstr :4040  # Windows
lsof -i :4040                  # Mac/Linux
```

## Development

### Add New Test
```python
# tests/test_new_feature.py
import allure
from app.pages.home_page import HomePage

@allure.feature("Shopping")
@allure.story("New Feature")
@allure.title("Description")
def test_new_feature(page):
    home_page = HomePage(page, "https://demoblaze.com")
    home_page.open()
    # ... test actions
```

### Add New Page Object
```python
# app/pages/new_page.py
from app.pages.base_page import BasePage
from app.pages.locators import Locators

class NewPage(BasePage):
    def some_action(self):
        self.page.click(Locators.SOME_LOCATOR)
```

### Add New Selectors
```python
# app/pages/locators.py
class Locators:
    NEW_ELEMENT = "css=.my-element"
    # or
    NEW_ELEMENT = "xpath=//div[@class='my-element']"
```

## Requirements

- Python 3.8+
- Playwright
- pytest
- pytest-playwright
- allure-pytest
- allure-commandline (optional, can be set up locally with `python setup_allure.py`)

## Repository

- **GitHub**: https://github.com/ShashankLokare/python_playwright_pytest
- **Main Branch**: Latest code and CI/CD results
- **Actions**: https://github.com/ShashankLokare/python_playwright_pytest/actions

## License

MIT

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
