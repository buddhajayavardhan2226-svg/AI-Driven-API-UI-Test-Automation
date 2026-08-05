import os
import sys
from pathlib import Path

# Add project root directory to sys.path so 'utils' and other modules import cleanly
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import allure
import pytest
from playwright.sync_api import sync_playwright

# Ensure required artifact folders exist before tests execute
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
    """Captures test failure status for post-test artifact handling."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


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