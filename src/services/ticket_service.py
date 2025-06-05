from typing import List, Dict, Optional
from datetime import datetime
from src.models.ticket import Ticket, TicketType, TicketCategory
from src.models.session import Session
from src.models.user import User
from src.models.database import db

class TicketService:
    def __init__(self):
        pass

    def create_session(self, 
                      session_date: datetime,
                      venue: TicketType,
                      capacity: Optional[int] = None) -> Session:
        """Create a new session"""
        return Session.get_or_create(session_date=session_date, venue=venue, capacity=capacity)

    @staticmethod
    def purchase_ticket(
        user: User,
        ticket_type: str,
        category: str,
        session_date: datetime,
        quantity: int = 1,
        concession_card: Optional[str] = None
    ) -> Ticket:
        """Purchase a ticket for a user"""
        # Validate ticket type
        try:
            ticket_type_enum = TicketType(ticket_type)
        except ValueError:
            raise ValueError(f"Invalid ticket type: {ticket_type}")

        # Validate category
        try:
            category_enum = TicketCategory(category)
        except ValueError:
            raise ValueError(f"Invalid category: {category}")

        # Get or create session
        session = Session.get_or_create(session_date, ticket_type_enum)

        # Check if session has capacity
        if not session.is_available(quantity):
            raise ValueError("Session is full")

        # Create ticket
        ticket = Ticket(
            ticket_type=ticket_type,
            category=category,
            session_date=session_date,
            session_id=session.id,
            user_id=user.id,
            concession_card=concession_card,
            quantity=quantity
        )

        # Add ticket to database
        db.session.add(ticket)
        db.session.commit()

        return ticket

    def get_available_sessions(self, date: Optional[datetime] = None) -> List[Session]:
        """Get available sessions for a specific date or all dates"""
        query = Session.query
        if date:
            query = query.filter(db.func.date(Session.session_date) == date.date())
        return [s for s in query.all() if s.get_available_capacity() > 0]

    def get_session_capacity(self, session_key: str) -> Optional[int]:
        """Get remaining capacity for a session"""
        venue, date_str = session_key.split('_')
        session_date = datetime.strptime(date_str, '%Y%m%d')
        session = Session.query.filter_by(
            venue=venue,
            session_date=session_date
        ).first()
        return session.get_available_capacity() if session else None

    @staticmethod
    def get_user_tickets(user: User) -> list[Ticket]:
        """Get all tickets for a user"""
        return user.tickets

    @staticmethod
    def update_ticket(ticket: Ticket, quantity: int, concession_card: Optional[str] = None) -> Ticket:
        """Update a ticket's details"""
        if quantity < 1 or quantity > 10:
            raise ValueError("Quantity must be between 1 and 10")

        # Check if new quantity is available
        if not ticket.session.is_available(quantity - ticket.quantity):
            raise ValueError("Session does not have enough capacity")

        ticket.quantity = quantity
        if concession_card:
            ticket.concession_card = concession_card

        db.session.commit()
        return ticket

    @staticmethod
    def delete_ticket(ticket: Ticket) -> None:
        """Delete a ticket"""
        db.session.delete(ticket)
        db.session.commit()

    def cancel_ticket(self, user: User, ticket: Ticket) -> bool:
        """Cancel a ticket"""
        if ticket in user.tickets and ticket.session:
            user.tickets.remove(ticket)
            ticket.session.tickets.remove(ticket)
            db.session.delete(ticket)
            db.session.commit()
            return True
        return False 