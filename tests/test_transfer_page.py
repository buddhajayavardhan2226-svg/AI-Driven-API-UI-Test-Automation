import pytest
from playwright.sync_api import Page, expect
from config import Config
from pages.homepage import HomePage
from pages.transfer_page import TransferamountPage
from utilities.utility_data import RandomDataUtil


@pytest.mark.order(5)
def test_transation_page(page: Page):
    print("\n Testing transfer page...")
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

    # HTML <option> tags use 'attached' state rather than default 'visible'
    page.wait_for_selector("#fromAccountId optionuuuuvvvuuu", state="attached")

    # Step 3: Perform Transfer
    transfer_page.enter_amount(random_data.get_random_amount())
    transfer_page.select_fromAccount()
    transfer_page.select_toAccount()
    transfer_page.click_transfer()

    # Step 4: Verification
    expect(transfer_page.msgg_after_transfer).to_be_visible()
    print("\n Transfer funds test passed successfully.")