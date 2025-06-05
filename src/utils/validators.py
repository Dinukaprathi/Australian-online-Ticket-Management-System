from datetime import datetime
from typing import Optional
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength"""
    # At least 6 characters, 1 uppercase, 1 lowercase, 1 number
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$'
    return bool(re.match(pattern, password))

def validate_date(date_str: str) -> Optional[datetime]:
    """Validate and parse date string"""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # Check if date is within tournament period
        start_date = datetime(2026, 1, 18)
        end_date = datetime(2026, 2, 2)
        if start_date <= date <= end_date:
            return date
    except ValueError:
        pass
    return None

def validate_concession_card(card_number: str) -> bool:
    """Validate concession card number format"""
    # Basic format: 8 digits
    pattern = r'^\d{8}$'
    return bool(re.match(pattern, card_number))

def validate_age(age: int) -> bool:
    """Validate age is within reasonable range"""
    return 0 <= age <= 120

def validate_username(username: str) -> bool:
    """Validate username format"""
    # 3-20 characters, alphanumeric and underscore only
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))

def validate_full_name(name: str) -> bool:
    """Validate full name format"""
    # At least two words, only letters, spaces, and hyphens
    pattern = r'^[A-Za-z]+(?:[ -][A-Za-z]+)+$'
    return bool(re.match(pattern, name)) 