import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_screener():

    response = requests.get(
        f"{BASE_URL}/screener"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_min_roe():

    response = requests.get(
        f"{BASE_URL}/screener?min_roe=20"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:

        assert company["return_on_equity_pct"] >= 20

def test_max_de():

    response = requests.get(
        f"{BASE_URL}/screener?max_de=1"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:

        if company["debt_to_equity"] is not None:

            assert company["debt_to_equity"] <= 1

def test_sector_filter():

    response = requests.get(
        f"{BASE_URL}/screener?sector=Financials"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:

        assert company["broad_sector"] == "Financials"

def test_pe_filter():

    response = requests.get(
        f"{BASE_URL}/screener?max_pe=30"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:

        if company["pe_ratio"] is not None:

            assert company["pe_ratio"] <= 30

def test_invalid_roe():

    response = requests.get(
        f"{BASE_URL}/screener?min_roe=-5"
    )

    assert response.status_code == 400
def test_invalid_datatype():

    response = requests.get(
        f"{BASE_URL}/screener?min_roe=abc"
    )

    assert response.status_code == 422