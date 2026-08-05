from markdown_it.parser_inline import RuleFuncInlineType
from playwright.sync_api import sync_playwright, Page, Playwright, expect
from pages.regestration_page import Regestrationpage
from pages.homepage import HomePage
from pages.transfer_page import TransferamountPage
from pages.AccountOverviewPage import AccountOverview
from pages.transationDetails import TransationDetails
from pages.findTransationsPage import FindTransations
from utilities.utility_data import RandomDataUtil
from config import *
import time
import uuid

from utilities.to_read_json_data import read_json_data
from colorama import Fore , init , Style
import pytest
init(autoreset=True)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n STEPS FROM STARTING TO ENDING :-")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + " =============================")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "   1-USER REGISTRATION ")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "   2-LOGIN WITH USER DETAILS AFTER REGESTRATION")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "   3-TRANSFER AMOUNTS ")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "   4-GO TO TRANSTAION DETAILS AND CHECK AMOUNT DEBETS THORUGHT TRANSATION ID AND DATE")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "   5-FINALLY LOGOUT")
# def test_regestrationpage(page: Page):
#     homepage = HomePage(page)
#     register = Regestrationpage(page)
#     homepage.clickregisterationurl()
#     fakerdata = RandomDataUtil()
#     firstname = fakerdata.get_first_name()
#     lastname = fakerdata.get_last_name()
#     address = fakerdata.get_address()
#     city = fakerdata.get_city()
#     state = fakerdata.get_state()
#     zipcode = fakerdata.get_zipcode()
#     phone = fakerdata.get_phone()
#     ssn = fakerdata.get_ssn()
#     global username0
#     username0 = fakerdata.get_username()
#     global password0
#     password0 = fakerdata.get_random_password()
#     register.set_first_last_name(firstname , lastname)
#     register.set_address_city_state_zipcode(address , city , state , zipcode)
#     register.set_phone_ssn(phone , ssn)
#     register.set_username(username0)
#     register.set_password_conformpassword(password0)
#     register.click_regestration()
#     expect(register.msg_after_creation).to_be_visible()
#     print("yes your login successful")
# def test_login(page):
#     print("\n testing login is running")
#     loginpage = HomePage(page)
#     config = Config()
#     loginpage.fillusernamebox(config.username)
#     loginpage.fillpasswordbox(config.password)
#     loginpage.clickloginbutton()
#     page.wait_for_timeout(3000)
#     expect(
#         page.get_by_role("heading", name="Accounts Overview")
#     ).to_be_visible()
#     print("\n testing login is successful")
# def test_transation_page(page:Page):
#     print("\n testing transation is running")
#     loginpage = HomePage(page)
#     config = Config()
#
#     loginpage.fillusernamebox(config.username)
#     loginpage.fillpasswordbox(config.password)
#     loginpage.clickloginbutton()
#
#     random_data = RandomDataUtil()
#     transfer_page = TransferamountPage(page)
#     transfer_page.click_transfer_page_link()
#     transfer_page.enter_amount(random_data.get_random_amount())
#     transfer_page.select_fromAccount()
#     transfer_page.select_toAccount()
#     transfer_page.click_transfer()
#     expect(transfer_page.msgg_after_transfer).to_be_visible()
#     page.wait_for_timeout(3000)

def test_E2E(page:Page):
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"REGESTRATION IN PROCESS..............")
    homepage = HomePage(page)
    register = Regestrationpage(page)
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
    global username0
    username0 = f"user_{uuid.uuid4().hex[:8]}"
    global password0
    password0 = fakerdata.get_random_password()
    register.set_first_last_name(firstname, lastname)
    register.set_address_city_state_zipcode(address, city, state, zipcode)
    register.set_phone_ssn(phone, ssn)
    register.set_username(username0)
    register.set_password_conformpassword(password0)
    register.click_regestration()
    expect(register.msg_after_creation).to_be_visible()
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"REGISTRATION CREATED SUCCESSFULLY!!!")
    register.click_logout()


    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"\nLOGIN IS IN PROCESS..............")
    loginpage = HomePage(page)
    config = Config()
    loginpage.fillusernamebox(config.username)
    loginpage.fillpasswordbox(config.password)
    loginpage.clickloginbutton()
    page.wait_for_timeout(1000)
    expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"\nLOGIN SUCCESSFUL!!!")

    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"\nTRANSACTION IS PROCESSING..............")

    random_data = RandomDataUtil()
    transfer_page = TransferamountPage(page)
    transfer_page.click_transfer_page_link()
    transfer_page.enter_amount(random_data.get_random_amount())
    transfer_page.select_fromAccount()
    transfer_page.select_toAccount()
    transfer_page.click_transfer()
    expect(transfer_page.msgg_after_transfer).to_be_visible()
    page.wait_for_timeout(1000)



    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"\nCHECKING TRANSACTION HISTORY..............")
    accountoverview_page=AccountOverview(page)

    accountoverview_page.click_AccountOverviewPagelink()
    accountoverview_page.click_RecentTRANSACTION()
    accountoverview_page.click_TransationDetails()
    transationDETAILS_page=TransationDetails(page)

    transation_ID=transationDETAILS_page.TransactionID
    DATE=transationDETAILS_page.date_value
    Payment_Type=transationDETAILS_page.type_value          #Debit
    assert Payment_Type== "Debit"
    FINDtransation_page = FindTransations(page)
    FINDtransation_page.click_FINDtransation_Page_LINK()
    FINDtransation_page.set_transaction_id(transation_ID)
    FINDtransation_page.click_Find_by_id_btn()
    expect(page.get_by_role("heading", name="Transaction Results")).to_be_visible()
    FINDtransation_page.click_Details()
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"TRANSACTION HISTORY IS VERIFIED!!!")
    page.wait_for_timeout(4000)
    FINDtransation_page.click_logout()
    page.wait_for_timeout(2000)
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"YOU LOGOUT FROM YOUR ACCOUNT 😔")

    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"THIS IS THE PROCESS OF TESTING USER CAN SUCCESSFULLY DO PAYMENTS WITH VALID DETAILS")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"logging OUT AFTER COMPLETION WHOLE PROCESS")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"THIS GENERATE ALLURE REPORTS , HTML REPORTS AND CAPTURES FAILURE SCREENSHOTS AND VIDEOS , TRACING")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"ALLURE & HTML REPORTS SUCCESSFULLY GENERATED")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"DUE TO NO FAILURES(MEANS ALL WE EXPECTED) ✨ NO VIDEO OR SCREEN SHOTS CAPTURED EVEN TRACING")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"FLAKY CONDITION MAY OCCURE DUE TO USERNAME ALREADY EXIST")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"MINIMUN RERUN 2 WILL SOLVE FLAKY CONDITION ")
    print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"THROUGHT API I POSTED DATA WHICH EASILY HELPS US TO SOLVE PROBLEM "+Fore.LIGHTRED_EX+Style.BRIGHT+ "( IT WILL ERASE OUR DATA FOR EVERY 5 MINUTES )"+Fore.LIGHTGREEN_EX+Style.BRIGHT+" OCCURE BY PARABANK SITE ")
