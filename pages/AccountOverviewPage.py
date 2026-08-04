from playwright.sync_api import Page ,sync_playwright
import json
import re

# with sync_playwright() as p:
#     browser=p.chromium.launch(headless=False)
#     context=browser.new_context()
#     page=context.new_page()
#     res=page.goto("https://parabank.parasoft.com/parabank")
#     # data=res.text()
#     # print(data)
#     page.locator("input[name=\"username\"]").fill("demo")
#     page.locator("input[name=\"password\"]").fill("demo")
#     page.get_by_role("button" , name="LOG IN").click()
#     page.wait_for_timeout(5000)

class AccountOverview:
    def __init__(self, page: Page):
        self.page = page

        self.AccountOverviewPagelink =page.get_by_role("link", name="Accounts Overview")
        self.RecentTRANSATION=page.locator("#accountTable tbody tr:nth-child(1) td:nth-child(1) a")
        self.TransationDetails=page.get_by_role("link", name=re.compile(r"Transfer Sent", re.IGNORECASE))



    def click_AccountOverviewPagelink(self):
        self.AccountOverviewPagelink.click()

    def click_RecentTRANSACTION(self):
        self.RecentTRANSATION.click()
    def click_TransationDetails(self):
        self.TransationDetails.click()
