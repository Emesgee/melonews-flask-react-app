from backend.app import app  # Import your Flask app
from backend.models import db  # Import the database instance and models

# Ensure the app context is active when creating tables
with app.app_context():
    db.create_all()  # This will create all tables defined in models.py
    print("All tables created successfully.")

    #db.drop_all()
    #print("All tables dropped!")