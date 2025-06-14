<<<<<<< HEAD
# Example: merged version
Your local version of README.md
The version from the remote (origin/main)
=======
<<<<<<< HEAD
>>>>>>> 3fa1350 (Initial commit)
# Australian-online-Ticket-Management-System
Python-based ticket management system for the Australian Open 2026. Calculates ticket prices by type, age category, and quantity. Developed for the MN404 unit at Melbourne Institute of Technology as part of a Master's program project.
=======
# Australian Open Ticket Management System (AOTMS)

A Python-based ticket management system for the Australian Open 2026.

## Project Overview
The AOTMS is designed to manage ticket sales for the Australian Open 2026, held from January 18 to February 2, 2026, at Melbourne Park. The system handles various ticket categories, pricing, and session management.
![Screenshot 2025-06-01 091441](https://github.com/user-attachments/assets/d49fc4ce-41e6-4462-adef-d539017b6458)

![Screenshot 2025-06-01 091224](https://github.com/user-attachments/assets/77796a62-5126-4822-a6ee-a31e46ccdb6b)
![Screenshot 2025-06-01 091757](https://github.com/user-attachments/assets/f11e38a1-b4a0-4da8-9e42-eba16411d09b)
![Screenshot 2025-06-01 095329](https://github.com/user-attachments/assets/d7179f70-8cfa-474c-9ee8-2b31b1530821)

## Features
- User authentication and login system
- Ticket price calculation based on categories
- Session management for different venues
- Support for various ticket types (Ground Pass, Reserved Seating)
- Concession and youth pricing
- Session capacity management

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure
```
aotms/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── ticket.py
│   │   └── session.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── ticket_service.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_ticket.py
│   └── test_session.py
├── requirements.txt
└── README.md!'
