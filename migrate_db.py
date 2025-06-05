from src.web_app import app
from src.models.database import db
import os

def migrate_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database migration completed successfully!")

if __name__ == '__main__':
    # Delete the existing database file if it exists
    db_file = 'aotms.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database file: {db_file}")
    
    # Run the migration
    migrate_database() 