import config
from pages.homepage import HomePage
from playwright.sync_api import Playwright ,Page ,expect
import pytest
from config import Config
@pytest.mark.order(3)
def test_login_validDetails(page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()
    page.wait_for_timeout(3000)

    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()
    print("\n testing login is successful")

def test_login_INvalidDetails(page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.invalid_username)
    loginpage.clickloginbutton()
    page.wait_for_timeout(3000)

    expect(
        page.get_by_text("The username and password could not be verified.")
    ).to_be_visible()
    print("\n testing login details is invalid")



