import uuid
import pytest
from colorama import Fore, Style, init
from playwright.sync_api import Page, expect

from pages.regestration_page import Regestrationpage
from pages.homepage import HomePage
from pages.transfer_page import TransferamountPage
from pages.AccountOverviewPage import AccountOverview
from pages.transationDetails import TransationDetails
from pages.findTransationsPage import FindTransations
from utilities.utility_data import RandomDataUtil

init(autoreset=True)


def test_E2E(page: Page):
    # Navigate & reset page state
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    homepage = HomePage(page)
    register = Regestrationpage(page)

    register.click_logout()

    # -------------------------------------------------------------
    # Step 1: User Registration
    # -------------------------------------------------------------
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nREGISTRATION IN PROCESS..............")
    homepage.clickregisterationurl()

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
    unique_username = f"e2e_{uuid.uuid4().hex[:10]}"
    unique_password = fakerdata.get_random_password()

    register.set_first_last_name(firstname, lastname)
    register.set_address_city_state_zipcode(address, city, state, zipcode)
    register.set_phone_ssn(phone, ssn)
    register.set_username(unique_username)
    register.set_password_conformpassword(unique_password)

    # Wait briefly for ParaBank DOM validation to settle
    page.wait_for_timeout(500)
    register.click_regestration()

    expect(register.msg_after_creation).to_be_visible(timeout=10000)
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "REGISTRATION CREATED SUCCESSFULLY!!!")
    register.click_logout()

    # -------------------------------------------------------------
    # Step 2: Login using the newly created credentials
    # -------------------------------------------------------------
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nLOGIN IS IN PROCESS..............")
    loginpage = HomePage(page)

    loginpage.fillusernamebox(unique_username)
    loginpage.fillpasswordbox(unique_password)
    loginpage.clickloginbutton()

    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "LOGIN SUCCESSFUL!!!")

    # -------------------------------------------------------------
    # Step 3: Transfer Funds
    # -------------------------------------------------------------
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nTRANSACTION IS PROCESSING..............")
    random_data = RandomDataUtil()
    transfer_page = TransferamountPage(page)
    transfer_page.click_transfer_page_link()

    page.wait_for_selector("#fromAccountId option", state="attached")

    transfer_page.enter_amount(random_data.get_random_amount())
    transfer_page.select_fromAccount()
    transfer_page.select_toAccount()
    transfer_page.click_transfer()

    expect(transfer_page.msgg_after_transfer).to_be_visible()

    # -------------------------------------------------------------
    # Step 4: Verify Transaction History
    # -------------------------------------------------------------
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nCHECKING TRANSACTION HISTORY..............")
    accountoverview_page = AccountOverview(page)
    accountoverview_page.click_AccountOverviewPagelink()
    accountoverview_page.click_RecentTRANSACTION()
    accountoverview_page.click_TransationDetails()

    transationDETAILS_page = TransationDetails(page)
    transation_ID = transationDETAILS_page.TransactionID
    Payment_Type = transationDETAILS_page.type_value

    assert Payment_Type == "Debit"

    FINDtransation_page = FindTransations(page)
    FINDtransation_page.click_FINDtransation_Page_LINK()
    FINDtransation_page.set_transaction_id(transation_ID)
    FINDtransation_page.click_Find_by_id_btn()

    expect(page.get_by_role("heading", name="Transaction Results")).to_be_visible()
    FINDtransation_page.click_Details()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "TRANSACTION HISTORY IS VERIFIED!!!")

    # -------------------------------------------------------------
    # Step 5: Logout
    # -------------------------------------------------------------
    FINDtransation_page.click_logout()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "YOU LOGGED OUT FROM YOUR ACCOUNT 😔")