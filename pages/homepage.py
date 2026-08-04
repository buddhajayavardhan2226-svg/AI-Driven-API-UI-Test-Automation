from playwright.sync_api import Page

class HomePage:
    def __init__(self , page : Page):
        self.page = page
        self.regestrationurl=page.get_by_role("link", name="Register")
        self.usernamebox=page.locator("input[name=\"username\"]")
        self.passwordbox=page.locator("input[name=\"password\"]")
        self.loginbutton=page.get_by_role("button", name="Log In")

    def homepagetitle(self):
        title = self.page.title()
        return title

    def fillusernamebox(self,username):
        self.usernamebox.fill(username)

    def fillpasswordbox(self,password):
        self.passwordbox.fill(password)

    def clickloginbutton(self):
        self.loginbutton.click()

    def clickregisterationurl(self):
        self.regestrationurl.click()