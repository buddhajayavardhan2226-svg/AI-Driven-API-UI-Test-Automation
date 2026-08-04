from playwright.sync_api import Page , Playwright ,expect
import re
class FindTransations:
    def __init__(self,page):
        self.page = page
        self.FINDtransation_Page_LINK = page.get_by_role("link", name="Find Transactions")
        self.findBYtransationIDbox=page.locator("input[id='transactionId']")
        self.find_by_id_btn= page.get_by_role("button" , name= "Find Transactions").nth(0)
        self.Find_by_Date_box= page.locator("input[id='transactionDate']")
        self.find_by_date_btn= page.get_by_role("button" , name= "Find Transactions").nth(0)
        self.logout=page.get_by_role("link", name="Log Out")
        self.Details=page.get_by_role("link", name=re.compile(r"Transfer Sent", re.IGNORECASE))

    def click_FINDtransation_Page_LINK(self):
        self.FINDtransation_Page_LINK.click()

    def set_transaction_id(self , value):
        self.findBYtransationIDbox.fill(value)
    def click_Find_by_id_btn(self):
        self.find_by_id_btn.click()
    def set_transaction_date(self , value):
        self.Find_by_Date_box.fill(value)
    def click_Find_by_date_btn(self):
        self.find_by_date_btn.click()
    def click_logout(self):
        self.logout.click()
    def click_Details(self):
        self.Details.click()

