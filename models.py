from datetime import datetime
from config import db
from pydantic import BaseModel, ValidationError, validator

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    #notes = db.relationship("Note", backref="person", cascade="all, delete, delete-orphan", single_parent=True, order_by="desc(Note.timestamp)")
    notes = db.relationship('Note', backref='person', lazy=True)

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NoteSchema(BaseModel):
    id: int
    person_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode=True
        from_attributes = True

class PersonSchema(BaseModel):
    id: int
    lname: str
    fname: str
    timestamp: datetime
    notes: list[NoteSchema] = []

    @validator('lname')
    def lname_must_not_be_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Last name must not be empty")
        return value

    class Config:
        orm_mode=True
        from_attributes = True

