from datetime import datetime
from src.services.auth_service import AuthService
from src.services.ticket_service import TicketService
from src.models.ticket import TicketType
from src.utils.validators import (
    validate_email, validate_password, validate_date,
    validate_concession_card, validate_age, validate_username,
    validate_full_name
)

class AOTMS:
    def __init__(self):
        self.auth_service = AuthService()
        self.ticket_service = TicketService()
        self.current_user = None

    def register(self):
        """Register a new user"""
        print("\n=== Register New User ===")
        
        username = input("Username: ")
        if not validate_username(username):
            print("Invalid username format")
            return

        password = input("Password: ")
        if not validate_password(password):
            print("Password must be at least 6 characters with 1 uppercase, 1 lowercase, and 1 number")
            return

        email = input("Email: ")
        if not validate_email(email):
            print("Invalid email format")
            return

        full_name = input("Full Name: ")
        if not validate_full_name(full_name):
            print("Invalid name format")
            return

        try:
            age = int(input("Age: "))
            if not validate_age(age):
                print("Invalid age")
                return
        except ValueError:
            print("Age must be a number")
            return

        concession_card = None
        if age >= 18:
            has_concession = input("Do you have a concession card? (y/n): ").lower() == 'y'
            if has_concession:
                concession_card = input("Concession Card Number: ")
                if not validate_concession_card(concession_card):
                    print("Invalid concession card format")
                    return

        try:
            user = self.auth_service.register_user(
                username=username,
                password=password,
                email=email,
                full_name=full_name,
                age=age,
                concession_card=concession_card
            )
            print(f"Registration successful! Welcome {user.full_name}")
        except ValueError as e:
            print(f"Registration failed: {str(e)}")

    def login(self):
        """Login user"""
        print("\n=== Login ===")
        username = input("Username: ")
        password = input("Password: ")

        user = self.auth_service.login(username, password)
        if user:
            self.current_user = user
            print(f"Welcome back, {user.full_name}!")
        else:
            print("Invalid username or password")

    def purchase_ticket(self):
        """Purchase a ticket"""
        if not self.current_user:
            print("Please login first")
            return

        print("\n=== Purchase Ticket ===")
        print("Available Ticket Types:")
        for i, ticket_type in enumerate(TicketType, 1):
            print(f"{i}. {ticket_type.value}")

        try:
            choice = int(input("\nSelect ticket type (number): "))
            if not 1 <= choice <= len(TicketType):
                print("Invalid choice")
                return
            ticket_type = list(TicketType)[choice - 1]
        except ValueError:
            print("Invalid input")
            return

        date_str = input("Enter date (YYYY-MM-DD): ")
        date = validate_date(date_str)
        if not date:
            print("Invalid date or date outside tournament period")
            return

        try:
            ticket = self.ticket_service.purchase_ticket(
                user=self.current_user,
                ticket_type=ticket_type,
                session_date=date
            )
            if ticket:
                print(f"Ticket purchased successfully! {ticket}")
            else:
                print("Failed to purchase ticket - session may be full")
        except ValueError as e:
            print(f"Error: {str(e)}")

    def view_tickets(self):
        """View user's tickets"""
        if not self.current_user:
            print("Please login first")
            return

        print("\n=== Your Tickets ===")
        tickets = self.ticket_service.get_user_tickets(self.current_user)
        if not tickets:
            print("You have no tickets")
            return

        for i, ticket in enumerate(tickets, 1):
            print(f"{i}. {ticket}")

    def run(self):
        """Run the main application loop"""
        while True:
            print("\n=== Australian Open Ticket Management System ===")
            print("1. Register")
            print("2. Login")
            print("3. Purchase Ticket")
            print("4. View Tickets")
            print("5. Exit")

            choice = input("\nSelect an option: ")

            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.purchase_ticket()
            elif choice == '4':
                self.view_tickets()
            elif choice == '5':
                print("Thank you for using AOTMS!")
                break
            else:
                print("Invalid option")

if __name__ == "__main__":
    app = AOTMS()
    app.run() 