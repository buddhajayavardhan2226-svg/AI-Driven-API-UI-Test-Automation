import pytest
from playwright.sync_api import Page, expect
from config import Config
from pages.homepage import HomePage


@pytest.mark.order(3)
def test_login_validDetails(page: Page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()

    # Web-first assertion handles waiting automatically
    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    print("\n testing login is successful")


def test_login_INvalidDetails(page: Page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    # Pass invalid credentials to trigger failure response
    loginpage.fillusernamebox(config.invalid_username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()

    # Web-first assertion handles waiting automatically
    expect(
        page.get_by_text("The username and password could not be verified.")
    ).to_be_visible()

    print("\n testing login details is invalid")