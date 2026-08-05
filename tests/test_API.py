from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from utilities.to_read_json_data import read_json_data
from colorama import Fore, Style, init


init(autoreset=True)


@pytest.mark.order(1)
def test_parabank_api():
    with sync_playwright() as playwright:

        with playwright.request.new_context(
                base_url="https://parabank.parasoft.com"
        ) as request_context:


            clean_res = request_context.post("/parabank/services/bank/cleanDB")
            print(f"\n[Clean DB Status]: {clean_res.status}")
            assert clean_res.status == 204


            init_res = request_context.post(
                "/parabank/services/bank/initializeDB"
            )
            print(f"[Init DB Status]: {init_res.status}")
            assert init_res.status == 204


            request_context.get("/parabank/register.htm")


            BASE_DIR = Path(__file__).resolve().parent.parent
            DATA_PATH = BASE_DIR / "test_data" / "data.json"
            user_data = read_json_data(file_path=str(DATA_PATH))


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

            response = request_context.post(
                "/parabank/register.htm", form=payload
            )
            print(f"[Register Status]: {response.status}")

            if response.status != 200:
                print(f"[Error Response Snippet]:\n{response.text()[:500]}")


            assert (
                    response.status == 200
            ), f"Registration failed with status {response.status}"

            response_body = response.text()
            assert (
                    "Welcome" in response_body or "created successfully" in response_body
            ), "Registration response missing welcome message!"


            res = request_context.get(
                "/parabank/services/bank/openapi.json",
                headers={"Accept": "application/json"}
            )
            assert res.ok, f"Failed to fetch OpenAPI specs, status code: {res.status}"

            json_data = res.json()
            paths = json_data.get("paths", {})

            print(f"{Fore.GREEN}{Style.BRIGHT}\nTHESE ARE ALL THE PATHS EXTRACTED FROM PARABANK API:")
            for path in paths.keys():
                print(path)

            print(
                f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}"
                f"TOTAL NUMBER OF ALL POSSIBLE PATHS: {len(paths)}"
            )