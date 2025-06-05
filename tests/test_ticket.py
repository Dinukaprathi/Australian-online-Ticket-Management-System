import pytest
from datetime import datetime
from src.models.ticket import Ticket, TicketType, TicketCategory
from src.models.user import User
from src.models.session import Session

def test_ticket_creation():
    """Test ticket creation with valid parameters"""
    date = datetime(2026, 1, 20)
    ticket = Ticket(
        ticket_type=TicketType.GROUND_PASS_WEEK1,
        category=TicketCategory.ADULT,
        session_date=date
    )
    assert ticket.ticket_type == TicketType.GROUND_PASS_WEEK1
    assert ticket.category == TicketCategory.ADULT
    assert ticket.session_date == date
    assert ticket.calculate_price() == 49.0

def test_concession_ticket():
    """Test concession ticket creation and pricing"""
    date = datetime(2026, 1, 20)
    ticket = Ticket(
        ticket_type=TicketType.ROD_LAVER,
        category=TicketCategory.CONCESSION,
        session_date=date,
        concession_card="12345678"
    )
    assert ticket.calculate_price() == 37.5

def test_youth_ticket():
    """Test youth ticket pricing"""
    date = datetime(2026, 1, 20)
    ticket = Ticket(
        ticket_type=TicketType.GROUND_PASS_WEEK1,
        category=TicketCategory.YOUTH,
        session_date=date
    )
    assert ticket.calculate_price() == 10.0

def test_invalid_date():
    """Test ticket creation with invalid date"""
    date = datetime(2025, 12, 25)  # Before tournament
    with pytest.raises(ValueError):
        Session(
            session_date=date,
            venue=TicketType.ROD_LAVER
        )

def test_session_capacity():
    """Test session capacity management"""
    date = datetime(2026, 1, 20)
    session = Session(
        session_date=date,
        venue=TicketType.ROD_LAVER
    )
    assert session.get_available_capacity() == 50

    # Add tickets up to capacity
    for _ in range(50):
        ticket = Ticket(
            ticket_type=TicketType.ROD_LAVER,
            category=TicketCategory.ADULT,
            session_date=date
        )
        assert session.add_ticket(ticket)

    # Try to add one more ticket
    ticket = Ticket(
        ticket_type=TicketType.ROD_LAVER,
        category=TicketCategory.ADULT,
        session_date=date
    )
    assert not session.add_ticket(ticket)

def test_user_ticket_management():
    """Test user ticket management"""
    user = User(
        username="testuser",
        password="Test123",
        email="test@example.com",
        full_name="Test User",
        age=25
    )
    date = datetime(2026, 1, 20)
    ticket = Ticket(
        ticket_type=TicketType.GROUND_PASS_WEEK1,
        category=TicketCategory.ADULT,
        session_date=date
    )
    user.add_ticket(ticket)
    assert len(user.get_tickets()) == 1
    assert user.get_tickets()[0] == ticket

def test_concession_validation():
    """Test concession ticket validation"""
    date = datetime(2026, 1, 20)
    with pytest.raises(ValueError):
        Ticket(
            ticket_type=TicketType.ROD_LAVER,
            category=TicketCategory.CONCESSION,
            session_date=date
        )  # No concession card provided

def test_ground_pass_pricing():
    """Test ground pass pricing for different weeks"""
    date = datetime(2026, 1, 20)
    # Week 1
    ticket1 = Ticket(
        ticket_type=TicketType.GROUND_PASS_WEEK1,
        category=TicketCategory.ADULT,
        session_date=date
    )
    assert ticket1.calculate_price() == 49.0

    # Middle weekend
    ticket2 = Ticket(
        ticket_type=TicketType.GROUND_PASS_MIDDLE,
        category=TicketCategory.ADULT,
        session_date=date
    )
    assert ticket2.calculate_price() == 69.0

    # Week 2
    ticket3 = Ticket(
        ticket_type=TicketType.GROUND_PASS_WEEK2,
        category=TicketCategory.ADULT,
        session_date=date
    )
    assert ticket3.calculate_price() == 139.0 