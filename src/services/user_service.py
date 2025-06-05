from src.models.database import db
from src.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def create_user(self, username: str, password: str, email: str, full_name: str, age: int, concession_card: str = None) -> User:
        """Create a new user"""
        user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            full_name=full_name,
            age=age,
            concession_card=concession_card
        )
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_username(self, username: str) -> User:
        """Get a user by username"""
        return User.query.filter_by(username=username).first()

    def get_user_by_email(self, email: str) -> User:
        """Get a user by email"""
        return User.query.filter_by(email=email).first()

    def verify_password(self, user: User, password: str) -> bool:
        """Verify a user's password"""
        return check_password_hash(user.password, password)

    def update_user(self, user: User, **kwargs) -> User:
        """Update user information"""
        for key, value in kwargs.items():
            if hasattr(user, key):
                if key == 'password':
                    value = generate_password_hash(value)
                setattr(user, key, value)
        db.session.commit()
        return user 