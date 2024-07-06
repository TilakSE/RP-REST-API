from datetime import datetime
from config import app, db
from models import Person, Note
from sqlalchemy import text
import logging

PEOPLE_NOTES = [
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "lname": "Bunny",
        "fname": "Easter",
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]

def truncate_tables():
    try:
        with db.engine.connect() as connection:
            # Begin a transaction
            transaction = connection.begin()
            try:
                # List all tables you want to truncate
                tables = ["note", "person"]
                for table in tables:
                    connection.execute(text(f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;'))
                # Commit the transaction if no exceptions
                transaction.commit()
                logging.info("Tables truncated successfully.")
            except Exception as e:
                # Rollback the transaction in case of error
                transaction.rollback()
                logging.error(f"Error truncating tables: {e}")
    except Exception as e:
        logging.error(f"Connection error: {e}")

def add_people_notes():
    for data in PEOPLE_NOTES:
        # Create a new Person instance
            person = Person(
                fname=data["fname"],
                lname=data["lname"],
                timestamp=datetime.utcnow()
            )
            db.session.add(person)
            db.session.flush()  # Flush to get the person ID before adding notes
            
            # Create Note instances for the person
            for note_content,timestamp in data["notes"]:
                note = Note(
                    content=note_content,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    person_id=person.id
                )
                db.session.add(note)
        
    # Commit the session after adding all entries
    db.session.commit()
    print("People and notes added successfully.")
    
with app.app_context():
    #db.drop_all()
    #db.create_all()
    truncate_tables()
    add_people_notes()
