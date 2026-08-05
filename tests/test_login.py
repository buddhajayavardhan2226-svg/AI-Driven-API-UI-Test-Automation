import pytest
from playwright.sync_api import Page, expect
from config import Config
from pages.homepage import HomePage


@pytest.mark.order(3)
def test_login_validDetails(page: Page):
    print("\n Testing login with valid details...")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()

    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    print("\n Login test passed successfully.")


@pytest.mark.order(4)
def test_login_INvalidDetails(page: Page):
    print("\n Testing login with invalid details...")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.invalid_username)
    loginpage.fillpasswordbox(config.invalid_password)
    loginpage.clickloginbutton()

    # Checks for visibility of the error paragraph regardless of exact string variant
    expect(page.locator("p.error")).to_be_visible()

    print("\n Invalid login test passed as expected.")