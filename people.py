from flask import abort, make_response
from config import db
from models import Person, PersonSchema, Note, NoteSchema
from pydantic import ValidationError, validator

def read_all():
    people = Person.query.all()
    people_list = []
    for person in people:
        person_dict = PersonSchema.from_orm(person).dict()
        person_dict['notes'] = [NoteSchema.from_orm(note).dict() for note in person.notes]
        people_list.append(person_dict)
    return people_list

def create(person_data):
    lname = person_data.get("lname")
    if lname is None or lname.strip() == "":
        abort(400, description="Last name is required and must not be empty")
    
    id = person_data.get("id")
    new_person = Person(
            lname=lname,
            id=id,
            fname=person_data.get("fname", "")
    )
    db.session.add(new_person)
    db.session.commit()
    person_dict = PersonSchema.from_orm(new_person).dict()
    person_dict['notes'] = [NoteSchema.from_orm(note).dict() for note in new_person.notes]
    return person_dict, 201

def read_one(person_id):
    person = Person.query.get(person_id)
    if person is not None:
        person_dict = PersonSchema.from_orm(person).dict()
        person_dict['notes'] = [NoteSchema.from_orm(note).dict() for note in person.notes]
        return person_dict
    else:
        abort(404, f"Person with ID {person_id} not found")

def update(person_id, person_data):
    existing_person = Person.query.get(person_id)

    if existing_person:
        existing_person.fname = person_data.get("fname", existing_person.fname)
        existing_person.lname = person_data.get("lname", existing_person.fname)
        db.session.commit()
        person_dict = PersonSchema.from_orm(existing_person).dict()
        person_dict['notes'] = [NoteSchema.from_orm(note).dict() for note in existing_person.notes]
        return person_dict, 200
    else:
        abort(404, f"Person with ID {person_id} not found")

def delete(person_id):
    existing_person = Person.query.get(person_id)
    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{person_id} successfully deleted", 204)
    else:
        abort(404, f"Person with ID {person_id} not found")
