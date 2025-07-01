import requests
import json

def test_login():
    url = "http://localhost:8000/auth/login"
    data = {"username": "admin", "password": "admin", "grant_type": ""}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=data, headers=headers)
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    print("[PASS] login")
    return token

def test_quickscan(token):
    url = "http://localhost:8000/mcp/quickscan"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"domain": "example.com"}
    resp = requests.post(url, json=data, headers=headers)
    assert resp.status_code == 200, resp.text
    print("[PASS] quickscan")

def test_portscan(token):
    url = "http://localhost:8000/mcp/portscan"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"target": "example.com"}
    resp = requests.post(url, json=data, headers=headers)
    assert resp.status_code == 200, resp.text
    print("[PASS] portscan")

def test_vulnscan(token):
    url = "http://localhost:8000/mcp/vulnscan"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"target": "http://example.com"}
    resp = requests.post(url, json=data, headers=headers)
    assert resp.status_code == 200, resp.text
    print("[PASS] vulnscan")

def test_result_query(token):
    url = "http://localhost:8000/result/assets"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200, resp.text
    print("[PASS] result/assets query")

if __name__ == "__main__":
    token = test_login()
    test_quickscan(token)
    test_portscan(token)
    test_vulnscan(token)
    test_result_query(token)
    print("All API tests passed.")
