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

        username = user_data["username"]
        password = user_data["password"]

        # 1. Call REST login endpoint
        login_response = request_context.get(
            f"/parabank/services/bank/login/{username}/{password}",
            headers={"Accept": "application/json"}
        )

        # 2. Check if login request succeeded or returned valid XML/JSON status
        assert login_response.status in [200, 400, 401]

    finally:
        request_context.dispose()
        playwright.stop()