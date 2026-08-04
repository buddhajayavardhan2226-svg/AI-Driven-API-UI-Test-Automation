from playwright.sync_api import Page , Playwright ,expect


class Regestrationpage:

    def __init__(self , page : Page):
        self.page = page

        self.firstname=page.locator("[id=\"customer.firstName\"]")
        self.lastname=page.locator("[id=\"customer.lastName\"]")
        self.address=page.locator("[id=\"customer.address.street\"]")
        self.city=page.locator("[id=\"customer.address.city\"]")
        self.state=page.locator("[id=\"customer.address.state\"]")
        self.zipcode=page.locator("[id=\"customer.address.zipCode\"]")
        self.phone=page.locator("[id=\"customer.phoneNumber\"]")
        self.ssn=page.locator("[id=\"customer.ssn\"]")
        self.username=page.locator("[id=\"customer.username\"]")
        self.password=page.locator("[id=\"customer.password\"]")
        self.conformpassword=page.locator("[id=\"repeatedPassword\"]")
        self.regesterbutton=page.get_by_role("button", name="Register")
        self.msg_after_creation=page.get_by_text("Your account was created")
        self.logout = page.get_by_role("link", name="Log Out")

    def set_first_last_name(self, first_name : str, last_name : str):
        self.firstname.fill(first_name)
        self.lastname.fill(last_name)
    def set_address_city_state_zipcode(self,address : str , city : str, state : str, zipcode : str):
        self.address.fill(address)
        self.city.fill(city)
        self.state.fill(state)
        self.zipcode.fill(zipcode)

    def set_phone_ssn(self, number : int , ssn : str):
        self.phone.fill(number)
        self.ssn.fill(ssn)

    def set_username(self, username : str ):
        self.username.fill(username)

    def set_password_conformpassword(self, password : str):
        self.password.fill(password)
        self.conformpassword.fill(password)

    def click_regestration(self):
        self.regesterbutton.click()

    def complete_regestration(self , user_data : dict):
        self.set_first_last_name(user_data["firstname"],user_data["lastname"])
        self.set_address_city_state_zipcode(user_data["address"],user_data["city"],user_data["state"],user_data["zipcode"])
        self.set_phone_ssn(user_data["phone"],user_data["ssn"])
        self.set_username(user_data["username"])
        self.set_password_conformpassword(user_data["password"])
        self.click_regestration()

        return self.msg_after_creation
    def click_logout(self):
        self.logout.click()