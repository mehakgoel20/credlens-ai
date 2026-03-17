import json
import requests
import os
import time

API_BASE = "http://127.0.0.1:8002"
API_KEY = os.getenv("APP_API_KEY", "credlens-secret-key")

REQUEST_TIMEOUT = 30
RETRIES = 2
REQUEST_DELAY = 0.2


def check_server():
    try:
        requests.get(f"{API_BASE}/docs", timeout=3)
        return True
    except:
        return False


def call_api(payload, headers):
    for attempt in range(RETRIES + 1):
        try:
            res = requests.post(
                f"{API_BASE}/decision/",
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            return res
        except requests.exceptions.RequestException as e:
            if attempt == RETRIES:
                raise e
            time.sleep(1)


def main():

    if not check_server():
        print("❌ Backend server not running on port 8002")
        print("Start it with:")
        print("python3 -m uvicorn app.main:app --reload --port 8002")
        return

    with open("eval/real_test_cases.json") as f:
        cases = json.load(f)

    total = len(cases)
    passed = 0
    latencies = []

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    for c in cases:

        name = c["name"]
        payload = c["input"]
        expected = c["expected_decision"]

        start = time.time()

        try:
            res = call_api(payload, headers)
        except requests.exceptions.RequestException as e:
            print(f"\n{name}")
            print("❌ REQUEST FAILED:", e)
            continue

        latency = time.time() - start
        latencies.append(latency)

        if res.status_code != 200:
            print(f"\n{name}")
            print(f"❌ API ERROR {res.status_code}: {res.text}")
            continue

        out = res.json()

        if "decision_output" not in out:
            print(f"\n{name}")
            print("❌ Missing decision_output in response")
            print("Response:", out)
            continue

        got = out["decision_output"]["decision"]

        ok = (got == expected)

        print(f"\n{name}")
        print(f"Expected: {expected} | Got: {got} => {'✅ PASS' if ok else '❌ FAIL'}")

        if ok:
            passed += 1

        time.sleep(REQUEST_DELAY)

    accuracy = (passed / total) * 100
    avg_latency = sum(latencies) / len(latencies)

    print("\n==============================")
    print(f"RESULT: {passed}/{total} passed")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Avg latency: {avg_latency:.2f}s")
    print("==============================")


if __name__ == "__main__":
    main()