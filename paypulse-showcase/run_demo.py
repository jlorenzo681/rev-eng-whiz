import uvicorn
import threading
import time
import sys
from server.app import app
from scanner.client import PayrollScanner

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def main():
    print("--- PayPulse Showcase Demo ---")
    print("[*] Starting OmniPay Server on port 8000...")
    
    # Run server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give it a moment to start
    time.sleep(2)
    
    try:
        print("\n[*] Initializing Scanner...")
        scanner = PayrollScanner("http://127.0.0.1:8000")
        
        print("[*] Attempting Authentication...")
        if scanner.authenticate():
            print("\n[*] Fetching Paystubs...")
            df = scanner.to_dataframe()
            print("\n[SUCCESS] Retrieved Payroll Data:")
            print(df.to_string())
        else:
            print("[FAIL] Authentication failed.")
            
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print("\n[*] Demo Complete. Exiting.")
        # Thread is daemon, will die with main thread

if __name__ == "__main__":
    main()
