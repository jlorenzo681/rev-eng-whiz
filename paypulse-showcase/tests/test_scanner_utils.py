import base64
import pytest
from scanner.utils import solve_challenge

def test_solve_challenge_basic():
    """Test with a simple known input."""
    challenge = "ABCD"
    expected_str = "BDFH"
    expected_b64 = base64.b64encode(expected_str.encode()).decode()
    assert solve_challenge(challenge) == expected_b64

def test_solve_challenge_empty():
    """Test with empty string."""
    challenge = ""
    expected_b64 = base64.b64encode(b"").decode()
    assert solve_challenge(challenge) == expected_b64

def test_solve_challenge_special_chars():
    """Test with special characters."""
    challenge = "!@"
    expected_str = "\"B"
    expected_b64 = base64.b64encode(expected_str.encode()).decode()
    assert solve_challenge(challenge) == expected_b64

def test_solve_challenge_longer_string():
    """Test with a string longer than 4 chars to verify cycle."""
    challenge = "AAAAE"
    expected_str = "BCDEF"
    expected_b64 = base64.b64encode(expected_str.encode()).decode()
    assert solve_challenge(challenge) == expected_b64
