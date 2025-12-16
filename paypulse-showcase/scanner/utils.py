import base64

def solve_challenge(challenge: str) -> str:
    """
    Reverse engineered 'secureHash' algorithm from login.html
    Logic:
    1. Iterate through challenge string
    2. Shift char code by (index % 4) + 1
    3. Base64 encode the result
    """
    output_chars = []
    for i, char in enumerate(challenge):
        shift = (i % 4) + 1
        new_char = chr(ord(char) + shift)
        output_chars.append(new_char)
    
    output_str = "".join(output_chars)
    # Python's b64encode expects bytes and returns bytes
    encoded = base64.b64encode(output_str.encode("utf-8")).decode("utf-8")
    return encoded
