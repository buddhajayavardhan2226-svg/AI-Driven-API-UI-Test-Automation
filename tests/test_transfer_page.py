import pytest
from playwright.sync_api import Page, expect
from config import Config
from pages.homepage import HomePage
from pages.transfer_page import TransferamountPage
from utilities.utility_data import RandomDataUtil


def test_transation_page(page: Page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    # Step 1: Login
    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()

    # Step 2: Navigate to Transfer page
    random_data = RandomDataUtil()
    transfer_page = TransferamountPage(page)
    transfer_page.click_transfer_page_link()

    # Wait for accounts to finish loading in dropdowns before interacting
    page.wait_for_selector("#fromAccountId option")

    # Step 3: Perform Transfer
    transfer_page.enter_amount(random_data.get_random_amount())
    transfer_page.select_fromAccount()
    transfer_page.select_toAccount()
    transfer_page.click_transfer()

    # Step 4: Verification
    expect(transfer_page.msgg_after_transfer).to_be_visible()