import os
from pathlib import Path
import allure
import pytest
from playwright.sync_api import sync_playwright

# Ensure required artifact folders exist
for folder in ["reports/videos", "reports/screenshots", "reports/traces"]:
    Path(folder).mkdir(parents=True, exist_ok=True)


def get_config_value(config, option_name):
    """
    Reads configuration values. Fallback order:
    1. Command line option
    2. pytest.ini setting
    """
    cmd_value = config.getoption(option_name, None)
    if cmd_value is not None:
        return cmd_value

    if option_name == "headed":
        ini_value = config.getini(option_name)
        return ini_value.lower() == "true" if isinstance(ini_value, str) else bool(ini_value)
    else:
        return config.getini(option_name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures test failure status for post-test artifact handling."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="function")
def browser_context(request):
    """
    Creates and manages the Playwright browser context.
    - Forces headless execution in CI environments automatically.
    - Cleans up Playwright instances safely.
    """
    browser_name = get_config_value(request.config, "browser")
    headed_flag = get_config_value(request.config, "headed")
    video_option = get_config_value(request.config, "video")

    # Enforce headless mode in CI environments regardless of local ini config
    is_ci = os.getenv("CI") == "true"
    run_headless = True if is_ci else not headed_flag

    print(f"[OK] Starting browser: {browser_name}")
    print(f"[OK] Headless mode: {run_headless} (CI={is_ci})")

    playwright = sync_playwright().start()

    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    browser_type = browser_name.lower()
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
    """
    Creates a new browser page, handles tracing, screenshots, and Allure reporting.
    """
    base_url = get_config_value(request.config, "base_url")
    screenshot_option = get_config_value(request.config, "screenshot")
    tracing_option = get_config_value(request.config, "tracing")
    video_option = get_config_value(request.config, "video")

    print(f"[INFO] Navigating to: {base_url}")

    if tracing_option in ["on", "retain-on-failure"]:
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = browser_context.new_page()
    page.goto(base_url)

    yield page

    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    print(f"[RESULT] Test '{test_name}' result: {'[FAIL]' if test_failed else '[PASS]'}")

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