from flask import Flask, render_template, request, jsonify
from config import app, db
from people import read_all, create, read_one, update, delete
from models import Person, Note
from notes import read_one as read_one_note, create as create_note, update as update_note, delete as delete_note

# Swagger setup
from flask_swagger_ui import get_swaggerui_blueprint
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "People API"})

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

@app.route("/api/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        return jsonify(read_all())
    elif request.method == "POST":
        new_person, status_code = create(request.json)
        return jsonify(new_person), status_code

@app.route("/api/people/<lname>", methods=["GET", "PUT", "DELETE"])
def handle_person(lname):
    if request.method == "GET":
        return jsonify(read_one(lname))
    elif request.method == "PUT":
        updated_person, status_code = update(lname, request.json)
        return jsonify(updated_person), status_code
    elif request.method == "DELETE":
        return delete(lname)

@app.route("/api/notes", methods=["GET", "POST"])
def handle_notes():
    if request.method == "GET":
        return jsonify(read_all())
    elif request.method == "POST":
        new_note, status_code = create_note(request.json)
        return jsonify(new_note), status_code

@app.route("/api/notes/<note_id>", methods=["GET", "PUT", "DELETE"])
def handle_note(note_id):
    if request.method == "GET":
        return jsonify(read_one_note(note_id))
    elif request.method == "PUT":
        updated_note, status_code = update_note(note_id, request.json)
        return jsonify(updated_note), status_code
    elif request.method == "DELETE":
        return delete_note(note_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=True)
