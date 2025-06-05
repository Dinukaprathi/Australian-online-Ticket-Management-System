from typing import Optional, Dict
from src.models.user import User

class AuthService:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def register_user(self, 
                     username: str,
                     password: str,
                     email: str,
                     full_name: str,
                     age: int,
                     concession_card: Optional[str] = None) -> User:
        """Register a new user"""
        if username in self.users:
            raise ValueError("Username already exists")

        user = User(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            age=age,
            concession_card=concession_card
        )
        self.users[username] = user
        return user

    def login(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = self.users.get(username)
        if user and user.verify_password(password):
            return user
        return None

    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)

    def update_user(self, username: str, **kwargs) -> Optional[User]:
        """Update user information"""
        user = self.users.get(username)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            return user
        return None

    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        if username in self.users:
            del self.users[username]
            return True
        return False 