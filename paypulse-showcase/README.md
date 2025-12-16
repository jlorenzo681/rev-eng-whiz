# PayPulse Showcase

A "Mock Payroll Scanner" project demonstrating skills in Python, Reverse Engineering, and API Integration.

## Project Overview

This project simulates a real-world scenario where a developer needs to build an API integration (= scanner) for a payroll provider ("OmniPay") that does not offer a public API and uses client-side obfuscation to prevent automation.

### Components

1.  **The Target (OmniPay)**: A FastAPI server mocking a payroll provider. It protects its login with a custom JS-based challenge-response mechanism.
2.  **The Scanner**: A Python library that:
    -   Connects to the target.
    -   Extracts the challenge.
    -   Solves the obfuscated algorithm locally (Reverse Engineering).
    -   Authenticates and retrieves payroll data.

## Getting Started

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the demo:
    ```bash
    python run_demo.py
    ```

3.  Run tests:
    ```bash
    pytest
    ```

## Real-Time Use Case Scenarios

This type of "scanner" architecture is critical for real-time applications such as:

1.  **Instant Loan Approvals**:
    -   A user applies for a loan at 2 AM.
    -   Instead of uploading PDFs and waiting 2 days for manual review, they login to their payroll provider via the app.
    -   The scanner instantly verifies income history.
    -   The loan is approved and funded in seconds.

2.  **Gig Economy Onboarding**:
    -   A driver signs up for a delivery app.
    -   The app scans their history from other platforms to verify experience and rating.
    -   Onboarding is completed instantly based on verified reputation data.

3.  **Dynamic Earned Wage Access (EWA)**:
    -   A worker checks out from their shift.
    -   The scanner detects the new shift data immediately.
    -   The worker can withdraw their earned wages for that day instantly, before payday.

## Tech Stack

-   **Server**: FastAPI, Jinja2
-   **Client**: httpx, BeautifulSoup4, pandas
-   **Concepts**: Reverse Engineering, Cookie/Session Management, Bot Protection Bypass.
