from src.web_app import app, db
from src.models.ticket import Ticket
from src.models.session import Session
from src.models.user import User

def migrate_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database() 