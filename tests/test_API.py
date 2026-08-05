import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from utilities.to_read_json_data import read_json_data

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

@pytest.mark.order(1)
def test_parabank_api():
    playwright = sync_playwright().start()
    request_context = playwright.request.new_context(
        base_url="https://parabank.parasoft.com"
    )

    try:
        data_path = BASE_DIR / "test_data" / "data.json"
        user_data = read_json_data(file_path=str(data_path))

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

        # Send request with explicit headers
        response = request_context.post(
            "/parabank/register.htm",
            form=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        # Allow 200 (Success/User Exists) and handle standard server behavior
        assert response.status in [200, 302], f"Registration returned status {response.status}"

    finally:
        request_context.dispose()
        playwright.stop()