import os
import sys
import requests
from pathlib import Path

# Add project root directory to sys.path FIRST before any local module imports
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import allure
import pytest
from playwright.sync_api import sync_playwright

# Direct import from root config.py
from config import Config

# n8n Webhook Configuration (Can be overridden via ENV variable in CI)
N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://jayava.app.n8n.cloud/webhook/playwright-failure"
)

# Global list to aggregate ALL failed test cases during a test run session
SUITE_FAILURES_LIST = []

for folder in ["reports/videos", "reports/screenshots", "reports/traces"]:
    Path(folder).mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    """Registers custom CLI flags and INI options safely without duplicate errors."""

    def safe_addoption(*args, **kwargs):
        try:
            parser.addoption(*args, **kwargs)
        except ValueError:
            pass  # Avoid collision if added by external plugins like pytest-base-url

    safe_addoption("--browser", action="store", default="chromium", help="Browser options: chromium, firefox, webkit")
    safe_addoption("--headed", action="store_true", default=False, help="Run tests in headed mode")
    safe_addoption("--base-url", action="store", default="https://parabank.parasoft.com/parabank", help="Base URL")
    safe_addoption("--video", action="store", default="retain-on-failure", help="Video recording mode")
    safe_addoption("--screenshot", action="store", default="only-on-failure", help="Screenshot capture mode")
    safe_addoption("--tracing", action="store", default="retain-on-failure", help="Playwright trace capture mode")

    # Register pytest.ini options
    for ini_opt in ["browser", "headed", "base_url", "video", "screenshot", "tracing"]:
        try:
            parser.addini(ini_opt, help=f"Default {ini_opt}")
        except ValueError:
            pass


def get_config_value(config, option_name):
    """Reads configuration values from CLI flags or fallback to pytest.ini."""
    for opt_format in [f"--{option_name}", option_name]:
        try:
            val = config.getoption(opt_format, None)
            if val is not None and val != False:
                return val
        except (ValueError, AttributeError):
            pass

    try:
        ini_value = config.getini(option_name)
        if ini_value:
            if option_name == "headed":
                return str(ini_value).lower() == "true"
            return ini_value
    except Exception:
        pass

    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures test failure details and appends them to the global session list."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Capture details for EVERY failed test during the execution call phase
    if report.when == "call" and report.failed:
        error_details = str(report.longrepr)

        # Store structured failure data in our session list
        SUITE_FAILURES_LIST.append({
            "test_name": item.name,
            "file_path": str(item.fspath),
            "failure_stage": report.when,
            "stacktrace": error_details
        })


def pytest_sessionfinish(session, exitstatus):
    """Hooks into session completion to send ALL aggregated failed tests to n8n in a single request."""
    if SUITE_FAILURES_LIST:
        print(f"\n[TestOps Engine] Suite Execution Complete. Total Failures Captured: {len(SUITE_FAILURES_LIST)}")

        # Build consolidated text prompt for n8n AI Agent
        formatted_failures_text = ""
        for idx, failure in enumerate(SUITE_FAILURES_LIST, 1):
            formatted_failures_text += (
                f"\n--- FAILED TEST #{idx} ---\n"
                f"Test Name: {failure['test_name']}\n"
                f"File Path: {failure['file_path']}\n"
                f"Failure Stage: {failure['failure_stage']}\n"
                f"--- STACKTRACE START ---\n"
                f"{failure['stacktrace']}\n"
                f"--- STACKTRACE END ---\n"
            )

        payload = {
            "total_failures_count": len(SUITE_FAILURES_LIST),
            "chatInput": (
                f"--- COMPLETE TEST SUITE FAILURE REPORT ---\n"
                f"Total Failed Tests: {len(SUITE_FAILURES_LIST)}\n"
                f"{formatted_failures_text}"
            ),
            "raw_failures": SUITE_FAILURES_LIST
        }

        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(N8N_WEBHOOK_URL, json=payload, headers=headers, timeout=15)
            print(
                f"[TestOps Engine] Successfully dispatched consolidated report for all {len(SUITE_FAILURES_LIST)} failures to n8n | Status: {response.status_code}")
        except Exception as e:
            print(f"[TestOps Engine Warning] n8n Webhook dispatch skipped/failed: {e}")


@pytest.fixture(scope="session", autouse=True)
def setup_registered_user():
    """Ensures the static user in Config() is registered in ParaBank before running tests."""
    config = Config()
    base_url = "https://parabank.parasoft.com/parabank"

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto(f"{base_url}/register.htm")
        page.locator("[name='customer.firstName']").fill("Test")
        page.locator("[name='customer.lastName']").fill("User")
        page.locator("[name='customer.address.street']").fill("123 Main St")
        page.locator("[name='customer.address.city']").fill("City")
        page.locator("[name='customer.address.state']").fill("State")
        page.locator("[name='customer.address.zipCode']").fill("12345")
        page.locator("[name='customer.phoneNumber']").fill("1234567890")
        page.locator("[name='customer.ssn']").fill("000-00-0000")
        page.locator("[name='customer.username']").fill(config.username)
        page.locator("[name='customer.password']").fill(config.password)
        page.locator("[name='repeatedPassword']").fill(config.password)
        page.get_by_role("button", name="Register").click()
    except Exception:
        pass  # If user already exists, ParaBank handles it gracefully
    finally:
        context.close()
        browser.close()
        playwright.stop()


@pytest.fixture(scope="function")
def browser_context(request):
    """Creates and manages Playwright browser context, forcing headless in CI."""
    browser_name = get_config_value(request.config, "browser") or "chromium"
    headed_flag = get_config_value(request.config, "headed") or False
    video_option = get_config_value(request.config, "video") or "retain-on-failure"

    is_ci = os.getenv("CI") == "true"
    run_headless = True if is_ci else not headed_flag

    print(f"[OK] Starting browser: {browser_name}")
    print(f"[OK] Headless mode: {run_headless} (CI={is_ci})")

    playwright = sync_playwright().start()

    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    browser_type = str(browser_name).lower()
    if browser_type == "chromium":
        browser = playwright.chromium.launch(headless=run_headless)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(headless=run_headless)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(headless=run_headless)
    else:
        playwright.stop()
        raise ValueError(f"[FAIL] Unsupported browser: {browser_name}")

    if video_option in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()

    yield context

    print("[CLEANUP] Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(request, browser_context):
    """Creates browser page, handles tracing, screenshots, and Allure reporting."""
    base_url = get_config_value(request.config, "base_url") or "https://parabank.parasoft.com/parabank"
    screenshot_option = get_config_value(request.config, "screenshot") or "only-on-failure"
    tracing_option = get_config_value(request.config, "tracing") or "retain-on-failure"
    video_option = get_config_value(request.config, "video") or "retain-on-failure"

    if tracing_option in ["on", "retain-on-failure"]:
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = browser_context.new_page()
    page.goto(base_url)

    yield page

    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        browser_context.tracing.stop(path=trace_path if test_failed or tracing_option == "on" else None)

    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)

        allure.attach.file(
            screenshot_path,
            name=f"{test_name}_screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    if test_failed and video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None
        if video_path and Path(video_path).exists():
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.WEBM
            )