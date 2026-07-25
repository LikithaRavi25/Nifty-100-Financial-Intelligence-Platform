import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

data = requests.get("http://127.0.0.1:8000/api/v1/companies").json()

print("Count:", len(data))
print("Last 5 companies:", [c["id"] for c in data[-5:]])

def test_get_companies():

    response = requests.get(
        f"{BASE_URL}/companies"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 90

def test_company_profile():

    response = requests.get(
        f"{BASE_URL}/companies/TCS"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"

def test_company_pl():

    response = requests.get(
        f"{BASE_URL}/companies/TCS/pl"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_company_bs():

    response = requests.get(
        f"{BASE_URL}/companies/TCS/bs"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_company_cashflow():

    response = requests.get(
        f"{BASE_URL}/companies/TCS/cashflow"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_company_ratios():

    response = requests.get(
        f"{BASE_URL}/companies/TCS/ratios"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

def test_invalid_company():

    response = requests.get(
        f"{BASE_URL}/companies/INVALID"
    )

    assert response.status_code == 404

def test_tearsheet():

    response = requests.get(
        f"{BASE_URL}/companies/TCS/tearsheet"
    )

    assert response.status_code == 200

    assert response.headers["content-type"] == "application/pdf"