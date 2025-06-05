from datetime import datetime, date
from typing import List, Dict
from src.models.ticket import Ticket, TicketType
from src.models.database import db

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_capacity = db.Column(db.Integer, default=0)
    tickets = db.relationship('Ticket', back_populates='session')

    def __init__(self, 
                 session_date: datetime,
                 venue: TicketType,
                 capacity: int = None):
        # Convert date to datetime if needed
        if isinstance(session_date, date) and not isinstance(session_date, datetime):
            session_date = datetime.combine(session_date, datetime.min.time())
        
        self.session_date = session_date
        self.venue = venue.value
        self.capacity = capacity or Ticket.CAPACITY.get(venue, float('inf'))
        self._validate_session()

    def _validate_session(self):
        """Validate session parameters"""
        # All ticket types are valid venues
        valid_venues = [t.value for t in TicketType]
        if self.venue not in valid_venues:
            raise ValueError(f"Invalid venue for session. Must be one of: {', '.join(valid_venues)}")

        # Validate date range (Jan 18 - Feb 2, 2026)
        start_date = datetime(2026, 1, 18)
        end_date = datetime(2026, 2, 2)
        if not start_date <= self.session_date <= end_date:
            raise ValueError("Session date must be between Jan 18 and Feb 2, 2026")

    def is_available(self, quantity: int = 1) -> bool:
        """Check if there's enough capacity for the requested quantity of tickets"""
        return self.current_capacity + quantity <= self.capacity

    def add_ticket(self, ticket: Ticket) -> bool:
        """Add a ticket to the session if capacity allows"""
        if self.is_available(ticket.quantity):
            self.tickets.append(ticket)
            self.current_capacity += ticket.quantity
            return True
        return False

    def get_available_capacity(self) -> int:
        """Get remaining capacity for the session"""
        return self.capacity - self.current_capacity

    def get_ticket_count_by_category(self) -> Dict[str, int]:
        """Get count of tickets by category"""
        counts = {}
        for ticket in self.tickets:
            category = ticket.category
            counts[category] = counts.get(category, 0) + ticket.quantity
        return counts

    def __str__(self):
        return (f"Session at {self.venue} on {self.session_date.strftime('%Y-%m-%d')} - "
                f"Capacity: {self.current_capacity}/{self.capacity}")

    @classmethod
    def get_or_create(cls, session_date: datetime, venue: TicketType, capacity: int = None) -> 'Session':
        """Get an existing session or create a new one"""
        # Convert date to datetime if needed
        if isinstance(session_date, date) and not isinstance(session_date, datetime):
            session_date = datetime.combine(session_date, datetime.min.time())
            
        session = cls.query.filter_by(
            session_date=session_date,
            venue=venue.value
        ).first()
        
        if not session:
            session = cls(session_date=session_date, venue=venue, capacity=capacity)
            db.session.add(session)
            db.session.commit()
        
        return session 