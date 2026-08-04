from pages import transfer_page

from pages.transfer_page import TransferamountPage
from playwright.sync_api import Page , Playwright ,expect
from config import *
from pages.homepage import HomePage
from utilities.utility_data import RandomDataUtil
import pytest

def test_transation_page(page:Page):
    print("\n testing login is running")
    loginpage = HomePage(page)
    config = Config()

    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()

    random_data = RandomDataUtil()
    transfer_page = TransferamountPage(page)
    transfer_page.click_transfer_page_link()
    transfer_page.enter_amount(random_data.get_random_amount())
    transfer_page.select_fromAccount()
    transfer_page.select_toAccount()
    transfer_page.click_transfer()

    expect(transfer_page.msgg_after_transfer).to_be_visible()

    page.wait_for_timeout(5000)

