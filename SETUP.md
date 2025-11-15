# Allure CLI Setup & Usage Guide

This document explains how to set up and use Allure 2.35.1 with the Playwright pytest framework.

## What is Allure?

Allure is a flexible, lightweight, open-source test reporting tool. It provides:
- Beautiful interactive reports with test history
- Detailed test steps with screenshots and attachments
- Test metrics and trends
- Live serving capabilities

## Prerequisites

### Required
- Python 3.8+
- Playwright browsers installed
- pytest and pytest-playwright

### For Allure CLI (Report Generation & Serving)
- **Java 8 or higher** (Allure is Java-based)

## Setup Options

### Option 1: Local Installation (Recommended) ⭐

Use the provided `setup_allure.py` script for a portable, one-time setup.

#### Step 1: Install Java

Choose your operating system:

**Windows:**
```powershell
# Option A: Via Chocolatey (if installed)
choco install openjdk11

# Option B: Via Conda
conda install openjdk

# Option C: Manual download
# https://www.oracle.com/java/technologies/downloads/
```

**macOS:**
```bash
brew install openjdk@11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install openjdk-11-jdk
```

#### Step 2: Run Setup Script

```powershell
python setup_allure.py
```

This will:
- Check if Java is installed
- Download Allure 2.35.1 (~24 MB)
- Extract to `allure-2.35.1/` directory
- Verify the installation

**Output:**
```
=== Allure CLI Setup ===

Checking Java...
✓ Java found
Downloading Allure 2.35.1 from GitHub...
  URL: https://github.com/allure-framework/allure2/releases/download/2.35.1/allure-2.35.1.zip
✓ Downloaded (23.8 MB)
Extracting to C:\Users\HP\python_git\python_playwright_pytest\allure-2.35.1...
✓ Allure extracted successfully

✓ Allure setup complete!

To use Allure locally, run:
  python run_tests_report.py              # Run tests and generate report
  python run_tests_report.py --view       # View existing report
  python run_tests_report.py --serve      # Serve live report
```

### Option 2: Global Installation

Install Allure globally via package manager or download.

**Windows (via Chocolatey):**
```powershell
choco install allure
```

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Manual Download:**
https://docs.qameta.io/allure/ → Downloads section

### Option 3: Docker

If you have Docker installed:

```bash
docker run --rm -v $(pwd)/allure-results:/app/results \
  frankescobar/allure-docker-service
```

## Running Tests & Generating Reports

### Method 1: Using run_tests_report.py (Easiest)

```powershell
# Run tests and generate HTML report
python run_tests_report.py

# Run tests in headless mode
python run_tests_report.py --headless

# View existing report (without running tests)
python run_tests_report.py --view

# Serve live report with Allure CLI
python run_tests_report.py --serve
```

This script automatically detects:
1. Local Allure installation at `allure-2.35.1/`
2. Global `allure` command in PATH

### Method 2: Using pytest + Allure CLI Directly

```powershell
# Step 1: Run tests and generate Allure JSON results
pytest tests/ -v --alluredir=allure-results --headed

# Step 2: Generate HTML report
allure generate allure-results -o allure-report --clean

# Step 3: View report (choose one)

# Option A: Serve with live updates
allure serve allure-results

# Option B: Open offline HTML report
start allure-report/index.html  # Windows
open allure-report/index.html   # macOS
```

## Understanding the Reports

### Report Locations

After running tests, you'll find:

```
python_playwright_pytest/
├── allure-results/           # JSON test results (for CI/CD)
│   ├── *.json               # Individual test data
│   ├── categories.json      # Test categories
│   ├── environment.json     # Environment info
│   └── ...
├── allure-report/           # Generated HTML report (offline browsable)
│   ├── index.html          # Main report page
│   ├── css/
│   ├── js/
│   └── data/
└── allure-2.35.1/          # Allure CLI binary (if using local setup)
```

### Report Sections

1. **Overview**
   - Pass/fail statistics
   - Test duration
   - Severity breakdown

2. **Test Details**
   - Test name and status
   - Execution time
   - Steps with screenshots
   - Attachments (logs, text, images)

3. **Behaviors**
   - Organized by Feature → Story → Test
   - Examples:
     - Shopping
       - Purchase Product
         - Buy Nexus 6 from DemoBlaze
         - Buy iPhone from DemoBlaze

4. **Timeline**
   - Execution order
   - Parallel execution info

5. **History**
   - Previous test runs
   - Trend analysis

## Viewing Reports

### Offline HTML Report

```powershell
# Windows
start allure-report/index.html

# PowerShell
Invoke-Item allure-report/index.html

# Or using Python
python -m webbrowser file://$(Get-Location)/allure-report/index.html
```

### Live Report Serving

```powershell
# Auto-opens in browser
python run_tests_report.py --serve

# Or directly with Allure
allure serve allure-results
```

Allure CLI will:
- Start a web server (usually port 4040)
- Auto-open your browser
- Reload on new test results
- Keep history of all runs

## Customizing Tests with Allure Annotations

Allure provides decorators to enhance your test reports:

```python
import allure
from app.pages.home_page import HomePage

@allure.feature("Shopping")
@allure.story("Purchase Product")
@allure.title("Buy Nexus 6 from DemoBlaze")
@allure.description("Complete end-to-end purchase workflow")
@allure.severity(allure.severity_level.CRITICAL)
def test_buy_nexus6(page):
    with allure.step("Open homepage"):
        home = HomePage(page, "https://demoblaze.com")
        home.open()
    
    with allure.step("Select Nexus 6 product"):
        home.select_product("Nexus 6")
    
    with allure.step("Add to cart"):
        # ... test code ...
        pass
```

### Common Annotations

| Annotation | Purpose | Example |
|-----------|---------|---------|
| `@allure.feature()` | High-level functionality | "Shopping", "Authentication" |
| `@allure.story()` | User story or scenario | "Purchase Product", "Login" |
| `@allure.title()` | Test display name | "Buy Nexus 6 from DemoBlaze" |
| `@allure.description()` | Detailed description | "Complete checkout flow" |
| `@allure.severity()` | Test priority | CRITICAL, MAJOR, MINOR, TRIVIAL |
| `allure.step()` | Test action step | "Click add to cart button" |
| `allure.attach()` | Attach file/text | Screenshots, logs |

### Attaching Data

```python
import allure

def test_example(page):
    # Attach text
    allure.attach("Login successful", "Status", allure.attachment_type.TEXT)
    
    # Attach screenshot
    screenshot = page.screenshot()
    allure.attach(screenshot, "page_state", allure.attachment_type.PNG)
    
    # Attach JSON
    allure.attach(json.dumps(data), "response", allure.attachment_type.JSON)
```

## Troubleshooting

### Java Not Found

**Error:** `JAVA_HOME is not set and no 'java' command could be found`

**Solution:**

1. Check Java installation:
```powershell
java -version
```

2. If not installed, install Java:
```powershell
# Conda (recommended)
conda install openjdk

# Or download from https://www.oracle.com/java/technologies/downloads/
```

3. Set JAVA_HOME (if needed):
```powershell
# Windows
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\path\to\java", "User")

# Linux/macOS
export JAVA_HOME=/usr/libexec/java_home
```

### Allure CLI Not Found

**Error:** `⚠ Allure CLI not found`

**Solution:**

```powershell
# Option 1: Use local setup (easiest)
python setup_allure.py

# Option 2: Install globally
# Windows: choco install allure
# macOS: brew install allure
# Linux: sudo apt-get install allure

# Option 3: Install via pip
pip install allure-commandline
```

### Port Already in Use

**Error:** `allure serve` fails with port conflict

**Solution:**

```powershell
# Check what's using the port (Windows)
netstat -ano | findstr :4040

# Kill the process
taskkill /PID <PID> /F

# Or let Allure pick another port
allure serve allure-results --port 5000
```

### Report Not Generating

**Error:** Report directory is empty

**Solution:**

1. Check if tests ran:
```powershell
ls allure-results/
```

2. Run tests with verbose output:
```powershell
pytest tests/ -v --alluredir=allure-results
```

3. Check for test failures:
```powershell
pytest tests/ -v
```

## CI/CD Integration

The project's GitHub Actions workflow automatically:
1. Runs all tests
2. Generates Allure JSON results
3. Generates HTML report
4. Uploads artifacts (30-day retention)

View results at: https://github.com/ShashankLokare/python_playwright_pytest/actions

## Best Practices

1. **Name your tests clearly**
   ```python
   # Good
   def test_buy_nexus6_from_demoblaze(page):
       pass
   
   # Avoid
   def test_1(page):
       pass
   ```

2. **Use feature/story/severity annotations**
   - Helps organize reports
   - Makes filtering easier
   - Provides business context

3. **Add steps for each logical action**
   ```python
   with allure.step("Open homepage"):
       # action
   
   with allure.step("Select product"):
       # action
   ```

4. **Attach screenshots at key points**
   - Helps debug failures
   - Provides visual documentation
   - Use in conftest.py for auto-capture on failure

5. **Keep allure-results/ and allure-report/ out of git**
   - These are generated (see .gitignore)
   - Use for CI/CD artifacts instead

6. **Archive old reports**
   - Allure keeps history in browser
   - Consider external backup for compliance

## Advanced Usage

### Clearing Old Results

```powershell
# Remove all existing results
rm -r allure-results
rm -r allure-report

# Then run tests again
python run_tests_report.py
```

### Comparing Test Runs

Allure automatically tracks history:
1. Open live report: `python run_tests_report.py --serve`
2. Go to "History" tab
3. View trend of passes/failures over time

### Integrating with CI/CD

See `.github/workflows/test.yml` for GitHub Actions setup:
- Downloads Allure 2.35.1
- Runs tests
- Generates report
- Uploads as artifact

Similar patterns work for:
- GitLab CI
- Jenkins
- CircleCI
- Azure DevOps

## Additional Resources

- **Allure Documentation**: https://docs.qameta.io/allure/
- **Allure Pytest Plugin**: https://docs.qameta.io/allure-pytest/
- **GitHub Releases**: https://github.com/allure-framework/allure2/releases
- **Community**: https://gitter.im/allure-framework/community

## Summary

| Task | Command |
|------|---------|
| First-time setup | `python setup_allure.py` |
| Run tests + generate report | `python run_tests_report.py` |
| Headless mode | `python run_tests_report.py --headless` |
| View report | `python run_tests_report.py --view` |
| Live server | `python run_tests_report.py --serve` |
| Check Java | `java -version` |
| Check Allure | `allure --version` |

---

For questions or issues, check the main README.md or GitHub Issues: https://github.com/ShashankLokare/python_playwright_pytest/issues
