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
└── README.md
```

## Running Tests
```bash
pytest tests/
```

## License
MIT License 
>>>>>>> ef69cff (Initial commit)
