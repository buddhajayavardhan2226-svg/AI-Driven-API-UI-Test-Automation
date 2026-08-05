import uuid
from playwright.sync_api import Page, Locator


class Regestrationpage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("input[id='customer.firstName']")
        self.last_name_input = page.locator("input[id='customer.lastName']")
        self.address_input = page.locator("input[id='customer.address.street']")
        self.city_input = page.locator("input[id='customer.address.city']")
        self.state_input = page.locator("input[id='customer.address.state']")
        self.zip_code_input = page.locator("input[id='customer.address.zipCode']")
        self.phone_input = page.locator("input[id='customer.phoneNumber']")
        self.ssn_input = page.locator("input[id='customer.ssn']")
        self.username_input = page.locator("input[id='customer.username']")
        self.password_input = page.locator("input[id='customer.password']")
        self.confirm_password_input = page.locator("input[id='repeatedPassword']")
        self.register_button = page.locator("input[value='Register']")

        # ParaBank renders this specific text upon successful creation
        self.msg_after_creation = page.get_by_text("Your account was created successfully.")

    def set_first_last_name(self, first_name: str, last_name: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)

    def set_address_city_state_zipcode(self, address: str, city: str, state: str, zipcode: str):
        self.address_input.fill(address)
        self.city_input.fill(city)
        self.state_input.fill(state)
        self.zip_code_input.fill(zipcode)

    def set_phone_ssn(self, phone: str, ssn: str):
        self.phone_input.fill(phone)
        self.ssn_input.fill(ssn)

    def set_username(self, username: str):
        self.username_input.clear()
        self.username_input.fill(username)
        # Blur the input so ParaBank's live validator finishes before form submit
        self.username_input.blur()

    def set_password_conformpassword(self, password: str):
        self.password_input.clear()
        self.password_input.fill(password)
        self.confirm_password_input.clear()
        self.confirm_password_input.fill(password)

    def click_regestration(self):
        # Ensure submit button is clicked cleanly without double trigger
        self.register_button.click()

    def click_logout(self):
        logout_btn = self.page.locator("a", has_text="Log Out")
        if logout_btn.is_visible():
            logout_btn.click()