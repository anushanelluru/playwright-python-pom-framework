# Amazon Test Automation Framework (Playwright + Python + PyTest)

A modern, production-ready UI Test Automation project built with **Playwright for Python** and **PyTest**, structured around the **Page Object Model (POM)** architectural pattern.

---

## 🚀 Why Playwright?
* **Auto-Waiting:** Playwright automatically waits for elements to be visible, stable, and ready before performing actions—eliminating arbitrary sleeps and flaky waits.
* **Fast & Resilient:** Communicates directly with browser engines via DevTools protocol without intermediary WebDriver drivers.
* **Multi-Tab / New Window Isolation:** Seamless handling of multiple pages, popups, and permissions using Browser Contexts.
* **Built-in Tracing & Network Interception:** Retains step-by-step DOM snapshots, screenshots, and network logs upon failure.

---

## 📁 Project Architecture

```text
my_amazon_test_project/
├── base/
│   ├── __init__.py
│   └── base_page.py             # Playwright Page wrapper with auto-waiting and safe interactions
├── pages/
│   ├── __init__.py
│   ├── home_page.py             # Amazon Home Page: search bar, logo, popups
│   ├── search_results_page.py   # Search Results: card locators, count, tab-aware item click
│   └── product_page.py          # Product Details: title assertion, price, cart
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # PyTest fixtures: context sizing, timeouts, failure screenshots
│   └── test_amazon_search.py    # Playwright E2E and parameterized test suites
├── utils/
│   ├── __init__.py
│   └── config_reader.py         # Config parser resolving runtime parameters from config.ini
├── config/
│   └── config.ini               # Test configuration (base URL, browser, timeout)
├── reports/                     # Output directory for HTML reports, screenshots, and traces
├── pytest.ini                   # PyTest run configurations, Playwright flags, and logging
└── requirements.txt             # Framework dependencies
```

---

## 🛠️ Step-by-Step PyCharm Setup Guide

### 1. Open the Project in PyCharm
1. Launch **PyCharm**.
2. Select **File ➔ Open...** and choose `my_amazon_test_project`.
3. Click **Open**.

### 2. Configure Virtual Environment (.venv)
1. In PyCharm, go to **PyCharm ➔ Settings** (`Cmd + ,` on macOS, or `Ctrl + Alt + S` on Windows).
2. Navigate to **Project: my_amazon_test_project ➔ Python Interpreter**.
3. Click **Add Interpreter ➔ Add Local Interpreter...**
4. Select **Virtualenv Environment**:
   * **Location:** `./.venv`
   * **Base Python:** Python 3.10+
5. Click **OK**.

### 3. Install Playwright & Browser Binaries
Open the PyCharm terminal (`Alt + F12` or `View ➔ Tool Windows ➔ Terminal`) and run:
```bash
# Step A: Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Step B: Install Playwright browser binaries (Chromium, Firefox, WebKit)
playwright install
```

### 4. Enable PyTest Runner in PyCharm
1. In Settings, navigate to **Tools ➔ Python Integrated Tools**.
2. Under **Testing**, set **Default test runner** to **pytest**.
3. Click **Apply** and **OK**.

---

## 💻 Test Execution Guide

### 1. Run All Tests (Headless by default with HTML Report):
```bash
pytest
```
* View the HTML report at:
  👉 `reports/report.html`

### 2. Run with Headed Browser (Visible UI):
```bash
pytest --headed
```

### 3. Run Across Multiple Browsers:
```bash
# Chromium (Chrome)
pytest --browser chromium

# Firefox
pytest --browser firefox

# WebKit (Safari engine)
pytest --browser webkit
```

### 4. Run Filtered Tests by Marker:
```bash
# Run critical smoke tests
pytest -m smoke

# Run full regression suite
pytest -m regression
```

### 5. Parallel Execution (Accelerated multi-process):
```bash
pytest -n auto
```

### 6. Inspect Failure Traces with Playwright Inspector:
If a test fails, Playwright saves an execution trace in `reports/artifacts/`. Inspect it visually:
```bash
playwright show-trace reports/artifacts/<trace-file>.zip
```
*(Shows a timeline, console logs, DOM snapshots, and network calls for the failed test).*
