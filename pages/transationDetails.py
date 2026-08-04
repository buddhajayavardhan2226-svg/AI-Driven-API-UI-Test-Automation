from playwright.sync_api import Playwright , Page , expect

class TransationDetails:
    def __init__(self , page:Page):
        self.page =page
        self.TransactionID=page.locator("tr", has_text="Transaction ID:").locator("td").nth(1).inner_text().strip()
        self.date_value = page.locator("tr", has_text="Date:").locator("td").nth(1).inner_text().strip()
        self.description = page.locator("tr", has_text="Description:").locator("td").nth(1).inner_text().strip()
        self.type_value = page.locator("tr", has_text="Type:").locator("td").nth(1).inner_text().strip()
        self.amount_value = page.locator("tr", has_text="Amount:").locator("td").nth(1).inner_text().strip()
