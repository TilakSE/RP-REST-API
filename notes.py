from datetime import datetime
from flask import abort, make_response
from config import db
from models import Person, Note, NoteSchema
from pydantic import ValidationError

def create(note_data):
    person_id = note_data.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_note = Note(
            content=note_data.get("content"),
            person_id=person_id,
            timestamp=note_data.get("timestamp", datetime.utcnow())
        )
        db.session.add(new_note)
        db.session.commit()
        return NoteSchema.from_orm(new_note).dict(), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")

def read_one(note_id):
    note = Note.query.get(note_id)

    if note is not None:
        return NoteSchema.from_orm(note).dict()
    else:
        abort(404, f"Note with ID {note_id} not found")

def update(note_id, note):
    existing_note = Note.query.get(note_id)

    if existing_note:
        existing_note.content = note.get("content", existing_note.content)
        db.session.commit()
        return NoteSchema.from_orm(existing_note).dict(), 200
    else:
        abort(404, f"Note with ID {note_id} not found")

def delete(note_id):
    existing_note = Note.query.get(note_id)

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(f"{note_id} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {note_id} not found")
