import uuid
import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.regestration_page import Regestrationpage
from utilities.utility_data import RandomDataUtil


@pytest.mark.order(2)
def test_regestrationpage(page: Page):
    # Navigate & reset session state
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    homepage = HomePage(page)
    register = Regestrationpage(page)

    register.click_logout()
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

    # Fresh unique username for this attempt
    unique_username = f"reg_{uuid.uuid4().hex[:10]}"
    unique_password = fakerdata.get_random_password()

    # Fill out registration form cleanly via POM
    register.set_first_last_name(firstname, lastname)
    register.set_address_city_state_zipcode(address, city, state, zipcode)
    register.set_phone_ssn(phone, ssn)
    register.set_username(unique_username)
    register.set_password_conformpassword(unique_password)

    # Wait briefly for ParaBank DOM validation to settle before clicking register
    page.wait_for_timeout(500)
    register.click_regestration()

    # Verification
    expect(register.msg_after_creation).to_be_visible(timeout=10000)
    print("\n Registration completed successfully.")

    register.click_logout()