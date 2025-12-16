import httpx
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional, List, Dict, Any
from .utils import solve_challenge

class PayrollScanner:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)
        self.token: Optional[str] = None

    def authenticate(self) -> bool:
        """
        Performs the 'reverse engineered' authentication flow:
        1. Fetch login page to get the challenge
        2. Solve the challenge locally
        3. Submit the solution to /login
        """
        # Step 1: Get Challenge
        print(f"[*] Connecting to {self.base_url}...")
        r = self.client.get("/")
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        challenge_input = soup.find("input", {"id": "challenge"})
        if not challenge_input:
            raise Exception("Could not find challenge input on page")
        
        challenge = challenge_input.get("value")
        print(f"[*] Found challenge: {challenge}")

        # Step 2: Solve Challenge
        response_code = solve_challenge(challenge)
        print(f"[*] Computed response: {response_code}")

        # Step 3: Login
        login_data = {
            "challenge": challenge,
            "response": response_code
        }
        
        r = self.client.post("/login", json=login_data)
        if r.status_code == 200:
            data = r.json()
            self.token = data.get("access_token")
            print(f"[*] Login Successful! Token obtained.")
            return True
        else:
            print(f"[!] Login Failed: {r.text}")
            return False

    def get_paystubs(self) -> List[Dict[str, Any]]:
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        r = self.client.get("/api/paystubs", headers=headers)
        r.raise_for_status()
        
        return r.json().get("paystubs", [])

    def to_dataframe(self) -> pd.DataFrame:
        data = self.get_paystubs()
        return pd.DataFrame(data)
