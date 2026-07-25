import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_all_sectors():

    response = requests.get(
    f"{BASE_URL}/sectors"
)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # Your database currently has 10 sectors
    assert len(data) == 10

def test_sector_fields():

    response = requests.get(
    f"{BASE_URL}/sectors"
)

    data = response.json()

    sector = data[0]

    assert "broad_sector" in sector
    assert "company_count" in sector

def test_financial_sector():
    response = requests.get(
    f"{BASE_URL}/sectors/Financials/companies"
)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_financial_sector_filter():

    response = requests.get(
    f"{BASE_URL}/sectors/Financials/companies"
)

    data = response.json()

    for company in data:

        assert company["broad_sector"] == "Financials"


def test_invalid_sector():

    response = requests.get(
        f"{BASE_URL}/sectors/INVALID"
    )

    assert response.status_code == 404

