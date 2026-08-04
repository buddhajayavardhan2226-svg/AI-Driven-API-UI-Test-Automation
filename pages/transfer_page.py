from playwright.sync_api import Page , Playwright , expect



class TransferamountPage:

    def __init__(self , page:Page):
        self.page = page
        self.link_of_tranfor_page=page.get_by_role("link", name="Transfer Funds")
        self.amoutnENTERbox=page.locator("#amount")
        self.fromAccountIDbox=page.locator("#fromAccountId")
        self.toAccountIDbox=page.locator("#toAccountId")
        self.transfer_button=page.get_by_role("button", name="Transfer")
        self.msgg_after_transfer=page.get_by_role("heading", name="Transfer Complete!")

    def click_transfer_page_link(self):
        self.link_of_tranfor_page.click()
    def enter_amount(self,amount):
        self.amoutnENTERbox.fill(str(amount))

    def select_fromAccount(self):
        # Wait for options in 'fromAccountId' dropdown
        self.fromAccountIDbox.click()
        self.fromAccountIDbox.locator("option").first.wait_for(state="attached")
        self.fromAccountIDbox.select_option(index=0)

    def select_toAccount(self):
        # 1. Wait until the options inside #toAccountId exist in DOM
        self.toAccountIDbox.click()
        self.toAccountIDbox.locator("option").first.wait_for(state="attached")

        # 2. Wait for Playwright to ensure the element is stable before selecting
        self.page.wait_for_timeout(500)  # Short 500ms pause for JS re-rendering

        # 3. Perform selection
        self.toAccountIDbox.select_option(index=0)
    def click_transfer(self):
        self.transfer_button.click()
    def msg_after_transfer(self):
        pass
        return  self.msgg_after_transfer