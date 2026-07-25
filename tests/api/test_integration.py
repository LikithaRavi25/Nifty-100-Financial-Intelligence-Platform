import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_health():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200


def test_companies():

    response = requests.get(
        f"{BASE_URL}/companies"
    )

    assert response.status_code == 200


def test_screener():

    response = requests.get(
        f"{BASE_URL}/screener"
    )

    assert response.status_code == 200


def test_sectors():

    response = requests.get(
        f"{BASE_URL}/sectors"
    )

    assert response.status_code == 200