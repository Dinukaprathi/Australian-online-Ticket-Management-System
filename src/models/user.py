from typing import List, Optional
from datetime import datetime
from src.models.ticket import Ticket
from src.models.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    concession_card = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tickets = db.relationship('Ticket', back_populates='user')

    def __init__(self, username, email, password, full_name, age, concession_card=None):
        self.username = username
        self.email = email
        self.set_password(password)  # Hash the password
        self.full_name = full_name
        self.age = age
        self.concession_card = concession_card
        self._validate_user()

    def _validate_user(self):
        """Validate user parameters"""
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email address")
        
        if self.age < 0 or self.age > 120:
            raise ValueError("Invalid age")

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password"""
        return check_password_hash(self.password, password)

    def add_ticket(self, ticket: Ticket):
        """Add a ticket to user's collection"""
        self.tickets.append(ticket)

    def get_tickets(self) -> List[Ticket]:
        """Get all tickets owned by the user"""
        return self.tickets

    def is_eligible_for_concession(self) -> bool:
        """Check if user is eligible for concession tickets"""
        return bool(self.concession_card)

    def is_youth(self) -> bool:
        """Check if user is in youth category (12-17)"""
        return 12 <= self.age <= 17

    def is_kids(self) -> bool:
        """Check if user is in kids category (3-11)"""
        return 3 <= self.age <= 11

    def __str__(self):
        return f"{self.username} ({self.full_name})" 