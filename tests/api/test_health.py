import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_health_status():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    assert response.status_code == 200

def test_health_ok():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    data = response.json()

    assert data["status"] == "ok"

def test_version_exists():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    data = response.json()

    assert "version" in data

def test_uptime():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    data = response.json()

    assert "uptime_seconds" in data

def test_db_counts():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    data = response.json()

    assert "db_row_counts" in data

def test_tables_present():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    tables = response.json()["db_row_counts"]

    required = [

        "companies",

        "balancesheet",

        "cashflow",

        "profitandloss",

        "financial_ratios",

        "market_cap",

        "analysis",

        "documents",

        "peer_groups",

        "sectors"

    ]

    for table in required:

        assert table in tables