import time
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/companies"

TICKERS = [
    "TCS",
    "INFY",
    "HDFCBANK",
    "RELIANCE",
    "ICICIBANK"
]


def test_dashboard_load_time():

    for ticker in TICKERS:

        start = time.perf_counter()

        response = requests.get(
            f"{BASE_URL}/{ticker}"
        )

        elapsed = time.perf_counter() - start

        print(f"{ticker}: {elapsed:.3f} seconds")

        assert response.status_code == 200

        assert elapsed < 3