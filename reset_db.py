import os
from app import app, db

DB_FILE = "food.db"

with app.app_context():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Old database files have been deleted: {DB_FILE}")
    else:
        print(f"Database file not found {DB_FILE}，this might be the first run.")

    db.create_all()
    print("The database has been rebuilt, and the table structure is up to date models.py keep consistent")
