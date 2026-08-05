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

    # Web-first assertion handles waiting automatically
    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    print("\n Login test passed successfully.")


@pytest.mark.order(4)
def test_login_INvalidDetails(page: Page):
    print("\n Testing login with invalid details...")
    loginpage = HomePage(page)
    config = Config()

    # Pass invalid username and invalid password to verify error handling
    loginpage.fillusernamebox(config.invalid_username)
    loginpage.fillpasswordbox(config.invalid_password)
    loginpage.clickloginbutton()

    # Target error message element explicitly
    expect(
        page.locator("p.error")
    ).to_contain_text("The username and password could not be verified.")

    print("\n Invalid login test passed as expected.")