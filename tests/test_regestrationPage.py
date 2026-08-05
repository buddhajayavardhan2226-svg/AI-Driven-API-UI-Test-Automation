import time
import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.regestration_page import Regestrationpage
from utilities.utility_data import RandomDataUtil


@pytest.mark.order(2)
def test_regestrationpage(page: Page):
    homepage = HomePage(page)
    register = Regestrationpage(page)

    homepage.clickregisterationurl()

    # Generate fake user data
    fakerdata = RandomDataUtil()
    firstname = fakerdata.get_first_name()
    lastname = fakerdata.get_last_name()
    address = fakerdata.get_address()
    city = fakerdata.get_city()
    state = fakerdata.get_state()
    zipcode = fakerdata.get_zipcode()
    phone = fakerdata.get_phone()
    ssn = fakerdata.get_ssn()

    # Scope variables locally to prevent global state leaks across test executions
    username0 = f"{int(time.time())}_jayavara"
    password0 = fakerdata.get_random_password()

    # Fill out registration form
    register.set_first_last_name(firstname, lastname)
    register.set_address_city_state_zipcode(address, city, state, zipcode)
    register.set_phone_ssn(phone, ssn)
    register.set_username(username0)
    register.set_password_conformpassword(password0)
    register.click_regestration()

    # Verification
    expect(register.msg_after_creation).to_be_visible()
    print("\n Registration completed successfully.")