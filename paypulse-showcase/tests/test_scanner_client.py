import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from scanner.client import PayrollScanner
from scanner.utils import solve_challenge

@pytest.fixture
def mock_httpx_client():
    with patch('scanner.client.httpx.Client') as mock:
        yield mock

@pytest.fixture
def scanner(mock_httpx_client):
    return PayrollScanner("http://testserver")

def test_authenticate_success(scanner, mock_httpx_client):
    # Setup mocks
    mock_instance = mock_httpx_client.return_value

    # Mock GET / (login page)
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.text = '<html><input id="challenge" value="ABCD"></html>'

    # Mock POST /login
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = {"access_token": "fake_token"}

    mock_instance.get.return_value = mock_get_response
    mock_instance.post.return_value = mock_post_response

    # Run
    result = scanner.authenticate()

    # Verify
    assert result is True
    assert scanner.token == "fake_token"

    # Verify calls
    mock_instance.get.assert_called_with("/")

    # Calculate expected response for "ABCD"
    expected_response = solve_challenge("ABCD")
    mock_instance.post.assert_called_with(
        "/login",
        json={"challenge": "ABCD", "response": expected_response}
    )

def test_authenticate_no_challenge_found(scanner, mock_httpx_client):
    mock_instance = mock_httpx_client.return_value

    # Mock GET / without challenge input
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.text = '<html><body>No challenge here</body></html>'
    mock_instance.get.return_value = mock_get_response

    with pytest.raises(Exception, match="Could not find challenge input"):
        scanner.authenticate()

def test_authenticate_login_failure(scanner, mock_httpx_client):
    mock_instance = mock_httpx_client.return_value

    # Mock GET /
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.text = '<html><input id="challenge" value="ABCD"></html>'

    # Mock POST /login failure
    mock_post_response = MagicMock()
    mock_post_response.status_code = 401
    mock_post_response.text = "Unauthorized"

    mock_instance.get.return_value = mock_get_response
    mock_instance.post.return_value = mock_post_response

    result = scanner.authenticate()

    assert result is False
    assert scanner.token is None

def test_get_paystubs_success(scanner, mock_httpx_client):
    mock_instance = mock_httpx_client.return_value
    scanner.token = "valid_token"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "paystubs": [{"date": "2023-01-01", "net_pay": 1000}]
    }
    mock_instance.get.return_value = mock_response

    paystubs = scanner.get_paystubs()

    assert len(paystubs) == 1
    assert paystubs[0]["net_pay"] == 1000

    mock_instance.get.assert_called_with(
        "/api/paystubs",
        headers={"Authorization": "Bearer valid_token"}
    )

def test_get_paystubs_unauthenticated(scanner):
    scanner.token = None
    with pytest.raises(Exception, match="Not authenticated"):
        scanner.get_paystubs()

def test_to_dataframe(scanner, mock_httpx_client):
    mock_instance = mock_httpx_client.return_value
    scanner.token = "valid_token"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "paystubs": [
            {"date": "2023-01-01", "net_pay": 1000},
            {"date": "2023-02-01", "net_pay": 1100}
        ]
    }
    mock_instance.get.return_value = mock_response

    df = scanner.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]["net_pay"] == 1000
    assert df.iloc[1]["net_pay"] == 1100
