from enum import Enum
from datetime import datetime
from typing import Optional
from src.models.database import db

class TicketType(Enum):
    GROUND_PASS_WEEK1 = "Ground Pass (Week 1)"
    GROUND_PASS_MIDDLE = "Ground Pass (Middle Weekend)"
    GROUND_PASS_WEEK2 = "Ground Pass (Week 2)"
    ROD_LAVER = "Rod Laver Arena"
    MARGARET_COURT = "Margaret Court Arena"
    JOHN_CAIN = "John Cain Arena"
    AO_LIVE = "AO Live"

class TicketCategory(Enum):
    ADULT = "Adult"
    CONCESSION = "Concession"
    YOUTH = "Youth"
    KIDS = "Kids"

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    concession_card = db.Column(db.String(50))
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationships
    session = db.relationship('Session', back_populates='tickets')
    user = db.relationship('User', back_populates='tickets')
    
    # Base prices for different ticket types
    PRICES = {
        TicketType.GROUND_PASS_WEEK1: {"ADULT": 49, "CONCESSION": 25, "YOUTH": 10, "KIDS": 25},
        TicketType.GROUND_PASS_MIDDLE: {"ADULT": 69, "CONCESSION": 30, "YOUTH": 10, "KIDS": 30},
        TicketType.GROUND_PASS_WEEK2: {"ADULT": 139, "CONCESSION": 70, "YOUTH": 5, "KIDS": 70},
        TicketType.ROD_LAVER: {"ADULT": 75, "CONCESSION": 37.5, "YOUTH": 37.5, "KIDS": 37.5},
        TicketType.MARGARET_COURT: {"ADULT": 65, "CONCESSION": 32.5, "YOUTH": 32.5, "KIDS": 32.5},
        TicketType.JOHN_CAIN: {"ADULT": 65, "CONCESSION": 32.5, "YOUTH": 32.5, "KIDS": 32.5},
        TicketType.AO_LIVE: {"ADULT": 20, "CONCESSION": 10, "YOUTH": 10, "KIDS": 10}
    }

    # Session capacity limits
    CAPACITY = {
        TicketType.ROD_LAVER: 50,
        TicketType.MARGARET_COURT: 50,
        TicketType.JOHN_CAIN: 50,
        TicketType.AO_LIVE: 10
    }

    def __init__(self, ticket_type, category, session_date, session_id, user_id, concession_card=None, quantity=1):
        self.ticket_type = ticket_type
        self.category = category
        self.session_date = session_date
        self.concession_card = concession_card
        self.session_id = session_id
        self.user_id = user_id
        self.quantity = quantity
        self._validate_ticket()

    def _validate_ticket(self):
        """Validate ticket parameters"""
        if self.category == TicketCategory.CONCESSION.value and not self.concession_card:
            raise ValueError("Concession card number is required for concession tickets")
        
        if self.category == TicketCategory.YOUTH.value:
            # Validate youth age (12-17)
            pass  # Implement age validation logic
        
        if self.quantity < 1 or self.quantity > 10:
            raise ValueError("Quantity must be between 1 and 10")

    def calculate_base_price(self):
        """Calculate the base price for a single ticket based on type"""
        base_prices = {
            TicketType.GROUND_PASS_WEEK1.value: 49,
            TicketType.GROUND_PASS_MIDDLE.value: 69,
            TicketType.GROUND_PASS_WEEK2.value: 139,
            TicketType.ROD_LAVER.value: 75,
            TicketType.MARGARET_COURT.value: 65,
            TicketType.JOHN_CAIN.value: 65,
            TicketType.AO_LIVE.value: 20
        }
        return base_prices.get(self.ticket_type, 0)
    
    def calculate_price(self):
        """Calculate the total price for all tickets based on type and category"""
        base_price = self.calculate_base_price()
        
        # Apply category discounts
        if self.category == TicketCategory.CONCESSION.value:
            price = base_price * 0.5  # 50% discount for concession
        elif self.category == TicketCategory.YOUTH.value:
            if self.ticket_type == TicketType.GROUND_PASS_WEEK1.value:
                price = 10
            elif self.ticket_type == TicketType.GROUND_PASS_MIDDLE.value:
                price = 10
            elif self.ticket_type == TicketType.GROUND_PASS_WEEK2.value:
                price = 5
            else:
                price = base_price * 0.5  # 50% discount for youth on other tickets
        elif self.category == TicketCategory.KIDS.value:
            price = base_price * 0.5  # 50% discount for kids
        else:
            price = base_price  # Adult price
        
        return price * self.quantity  # Multiply by quantity

    def calculate_total_price(self) -> float:
        """Calculate the total price for all tickets"""
        return self.calculate_price()

    def is_available(self, current_capacity: int) -> bool:
        """Check if ticket is available based on session capacity"""
        ticket_type = TicketType(self.ticket_type)
        if ticket_type in self.CAPACITY:
            return current_capacity + self.quantity <= self.CAPACITY[ticket_type]
        return True  # Ground passes have no capacity limit

    def __str__(self):
        return f"{self.ticket_type} - {self.category} - {self.quantity}x - ${self.calculate_total_price():.2f}"

    def __repr__(self):
        return f'<Ticket {self.id}: {self.ticket_type} - {self.category}>' 