import sys
from pathlib import Path

# Add project root directory to sys.path so 'utils' can be imported anywhere
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import pytest
from playwright.sync_api import sync_playwright
from utils.json_reader import read_json_data


@pytest.mark.order(1)
def test_parabank_api():
    playwright = sync_playwright().start()
    request_context = playwright.request.new_context(
        base_url="https://parabank.parasoft.com"
    )

    try:
        # 1. Clean Database
        clean_res = request_context.post("/parabank/services/bank/cleanDB")
        assert clean_res.status in [200, 204]

        # 2. Initialize Database
        init_res = request_context.post("/parabank/services/bank/initializeDB")
        assert init_res.status in [200, 204]

        # 3. Read Data & Register User via API
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

        response = request_context.post("/parabank/register.htm", form=payload)
        assert response.status == 200

        # 4. Fetch OpenAPI Specs
        res = request_context.get(
            "/parabank/services/bank/openapi.json",
            headers={"Accept": "application/json"}
        )
        assert res.ok
        paths = res.json().get("paths", {})
        print(f"\nTOTAL NUMBER OF PATHS: {len(paths)}")

    finally:
        request_context.dispose()
        playwright.stop()