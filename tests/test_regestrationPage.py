import time
import uuid
import pytest
from playwright.sync_api import Page, expect
from pages.homepage import HomePage
from pages.regestration_page import Regestrationpage
from utilities.utility_data import RandomDataUtil


@pytest.mark.order(2)
def test_regestrationpage(page: Page):
    # Ensure active session from previous tests is cleared
    page.context.clear_cookies()

    homepage = HomePage(page)
    register = Regestrationpage(page)

    # Navigate to home and ensure logout if session persists
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    logout_link = page.locator("a", has_text="Log Out")
    if logout_link.is_visible():
        logout_link.click()

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

    # Guaranteed unique username using nanosecond precision + UUID hex
    unique_username = f"usr_{time.time_ns()}_{uuid.uuid4().hex[:6]}"
    unique_password = fakerdata.get_random_password()

    # Fill out registration form
    register.set_first_last_name(firstname, lastname)
    register.set_address_city_state_zipcode(address, city, state, zipcode)
    register.set_phone_ssn(phone, ssn)

    # Force clear username input box before filling in case browser auto-filled it
    username_field = page.locator("input[id='customer.username']")
    username_field.clear()
    username_field.fill(unique_username)

    register.set_password_conformpassword(unique_password)
    register.click_regestration()

    # Verification
    expect(register.msg_after_creation).to_be_visible()
    print("\n Registration completed successfully.")

    # Cleanup session state for subsequent tests
    register.click_logout()