import pytest
from pages.homepage import HomePage
from pages.regestration_page import Regestrationpage
from playwright.sync_api import expect
from utilities.utility_data import RandomDataUtil
from playwright.sync_api import Page , Playwright ,expect
import time


@pytest.mark.order(2)
def test_regestrationpage(page: Page):

    homepage = HomePage(page)
    register = Regestrationpage(page)
    homepage.clickregisterationurl()
    fakerdata = RandomDataUtil()
    firstname = fakerdata.get_first_name()
    lastname = fakerdata.get_last_name()
    address = fakerdata.get_address()
    city = fakerdata.get_city()
    state = fakerdata.get_state()
    zipcode = fakerdata.get_zipcode()
    phone = fakerdata.get_phone()
    ssn = fakerdata.get_ssn()
    global username0
    username0 =  f"{int(time.time())}_jayavara"
    global password0
    password0 = fakerdata.get_random_password()

    register.set_first_last_name(firstname , lastname)
    register.set_address_city_state_zipcode(address , city , state , zipcode)
    register.set_phone_ssn(phone , ssn)
    register.set_username(username0)
    register.set_password_conformpassword(password0)
    register.click_regestration()

    expect(register.msg_after_creation).to_be_visible()
    print("yes your login successful")