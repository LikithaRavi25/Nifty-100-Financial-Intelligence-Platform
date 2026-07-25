import threading
import time
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/screener"

results = []


def call_api():

    response = requests.get(BASE_URL)

    results.append(response.status_code)


def test_concurrent_screener():

    threads = []

    start = time.perf_counter()

    # Launch 10 concurrent requests
    for _ in range(10):

        t = threading.Thread(target=call_api)

        threads.append(t)

        t.start()

    # Wait for all requests to finish
    for t in threads:

        t.join()

    elapsed = time.perf_counter() - start

    print(f"\nCompleted in {elapsed:.2f} seconds")

    print("Status Codes:", results)

    # Verify all requests succeeded
    assert len(results) == 10

    assert all(code == 200 for code in results)

    # Performance target
    assert elapsed < 10