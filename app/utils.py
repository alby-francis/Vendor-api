import re

def valid_password(password):
    # Check length
    if len(password) < 8 or len(password) > 12:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'\d', password):
        return False

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*()-_+=]', password):
        return False
    return True

def valid_first_name(name):
    # Check if name contains only alphabets
    if re.match(r'^[A-Za-z]+$', name):
        return True
    else:
        return False

def valid_last_name(name):
    # Check if name contains only alphabets, one single quote, and one dot
    if re.match(r"^[A-Za-z']+\.?$", name):
        return True
    else:
        return False