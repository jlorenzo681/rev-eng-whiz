from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import base64
import uvicorn
import random
import string

app = FastAPI(title="OmniPay Provider")
templates = Jinja2Templates(directory="paypulse-showcase/server/templates")
security = HTTPBearer()

# In-memory session store (simplify for demo)
SESSIONS = {}
TOKENS = set()

def generate_challenge(length=12):
    return ''.join(random.choices(string.ascii_letters, k=length))

def validate_response(challenge: str, response: str) -> bool:
    """
    Validation Logic (The 'Secret' format):
    1. Each char in challenge is shifted by (index % 4 + 1)
    2. Result is Base64 encoded
    """
    try:
        decoded = base64.b64decode(response).decode()
        expected = ""
        for i, char in enumerate(challenge):
            shift = (i % 4) + 1
            expected += chr(ord(char) + shift)
        return decoded == expected
    except:
        return False

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    challenge = generate_challenge()
    # Store challenge in a simple way. ensuring a session or cookie would be better but keeping it simple.
    # For this demo, we'll just put it in a global map keyed by a hidden ID or similar?
    # Actually, let's just make the client send back both challenge and response for statelessness in this simple demo, 
    # BUT in a real app, the server would remember the challenge. 
    # Let's use a hidden form field for the challenge string itself to keep it stateless.
    return templates.TemplateResponse(request=request, name="login.html", context={"challenge": challenge})

@app.post("/login")
async def login(data: dict):
    challenge = data.get("challenge")
    response = data.get("response")
    
    if not challenge or not response:
        raise HTTPException(status_code=400, detail="Missing data")
        
    if validate_response(challenge, response):
        token = secrets.token_hex(16)
        TOKENS.add(token)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials or bot detected")

@app.get("/api/paystubs")
async def get_paystubs(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials not in TOKENS:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
        
    return {
        "employee": "John Doe",
        "paystubs": [
            {"date": "2023-11-30", "net_pay": 2500.00, "currency": "USD"},
            {"date": "2023-11-15", "net_pay": 2500.00, "currency": "USD"},
            {"date": "2023-10-31", "net_pay": 2400.00, "currency": "USD"},
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
