import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from utilities.to_read_json_data import read_json_data
from colorama import Fore, Style

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


@pytest.mark.order(1)
def test_parabank_api():
    with sync_playwright() as playwright:
        request_context = playwright.request.new_context(
            base_url="https://parabank.parasoft.com"
        )

        try:
            # 1. Clean Database
            clean_res = request_context.post("/parabank/services/bank/cleanDB")
            print(f"\n[Clean DB Status]: {clean_res.status}")
            assert clean_res.status == 204, f"Clean DB failed with status {clean_res.status}"

            # 2. Initialize Database
            init_res = request_context.post("/parabank/services/bank/initializeDB")
            print(f"[Init DB Status]: {init_res.status}")
            assert init_res.status == 204, f"Initialize DB failed with status {init_res.status}"

            # 3. Establish Session (GET register page)
            request_context.get("/parabank/register.htm")

            # 4. Read Test Data using dynamic BASE_DIR path
            data_path = BASE_DIR / "test_data" / "data.json"
            user_data = read_json_data(file_path=str(data_path))

            # 5. Build Registration Payload
            payload = {
                "customer.firstName": str(user_data["firstName"]),
                "customer.lastName": str(user_data["lastName"]),
                "customer.address.street": str(user_data["address"]),
                "customer.address.city": str(user_data["city"]),
                "customer.address.state": str(user_data["state"]),
                "customer.address.zipCode": str(user_data["zipCode"]),
                "customer.phoneNumber": str(user_data["phoneNumber"]),
                "customer.ssn": str(user_data["ssn"]),
                "customer.username": str(user_data["username"]),
                "customer.password": str(user_data["password"]),
                "repeatedPassword": str(user_data["confirm"]),
            }

            # 6. Post Registration using form=
            response = request_context.post("/parabank/register.htm", form=payload)
            print(f"[Register Status]: {response.status}")

            if response.status != 200:
                print(f"[Error Response Snippet]:\n{response.text()[:500]}")

            # 7. Assertions for Registration
            assert response.status == 200, f"Registration failed with status {response.status}"
            assert (
                "Welcome" in response.text() or "created successfully" in response.text()
            ), "Registration response missing welcome message!"

            # 8. Extract & Print OpenAPI Endpoints
            res = request_context.get(
                "/parabank/services/bank/openapi.json",
                headers={"Accept": "application/json"}
            )
            json_data = res.json()
            paths = json_data.get("paths", {})

            print(
                Fore.GREEN
                + Style.BRIGHT
                + "\nTHESE ARE THE ALL PATHS WHICH WE GET OUT FROM API REQUEST"
            )
            for path in paths.keys():
                print(path)

            print(
                Fore.LIGHTGREEN_EX
                + Style.BRIGHT
                + "TOTAL NUMBER OF ALL POSSIBLE PATHS EXTRACTED FROM API REQUEST OF PARABANK: ",
                len(paths),
            )

        finally:
            request_context.dispose()