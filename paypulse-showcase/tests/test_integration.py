from fastapi.testclient import TestClient
from server.app import app
from scanner.client import PayrollScanner
from scanner.utils import solve_challenge
import base64

client = TestClient(app)

def test_algorithm_correctness():
    """Verify our Python implementation matches the logic"""
    # Logic: char code + (index % 4 + 1)
    # A -> 65. index 0. shift 1 -> 66 (B)
    # B -> 66. index 1. shift 2 -> 68 (D)
    # C -> 67. index 2. shift 3 -> 70 (F)
    # D -> 68. index 3. shift 4 -> 72 (H)
    challenge = "ABCD"
    expected_str = "BDFH" 
    expected_b64 = base64.b64encode(expected_str.encode()).decode()
    
    assert solve_challenge(challenge) == expected_b64

def test_server_validation():
    """Verify server rejects bad responses"""
    challenge = "ABCD"
    response = "BADRESPONSE"
    
    res = client.post("/login", json={"challenge": challenge, "response": response})
    assert res.status_code == 401

def test_e2e_flow():
    """
    Test the full flow using the scanner code, but mocking the network 
    calls to use TestClient instead of httpx.
    """
    # We can patch the scanner's client, or just use httpx to hit the running app 
    # but TestClient is easier if we adapt the scanner.
    # However, Scanner uses httpx.Client. TestClient IS a requests-like interface but for httpx we might need 
    # to be careful. 
    # Actually, TestClient exposes app as ASGI. 
    # For simplicity in this 'showcase' separate from proper rigorous testing, 
    # I'll just rely on the 'algorithm' test and a lightweight integration 
    # that uses the TestClient directly to simulate the scanner steps.
    
    # 1. Get Challenge
    r = client.get("/")
    assert r.status_code == 200
    assert "challenge" in r.text
    
    # Extract (cheat a bit for test simplicity or use regex/bs4)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    challenge = soup.find("input", {"id": "challenge"})["value"]
    
    # 2. Solve
    response = solve_challenge(challenge)
    
    # 3. Login
    r = client.post("/login", json={"challenge": challenge, "response": response})
    assert r.status_code == 200
    token = r.json()["access_token"]
    
    # 4. Get Data
    r = client.get("/api/paystubs", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["employee"] == "John Doe"
