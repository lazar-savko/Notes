from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Task Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text
        }

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return "<h2>Welcome to the Notes server</h2>"

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes])

@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    if note:
        return jsonify(note.to_dict())
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    new_note = Note(text=data['text'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    if note:
        data = request.json
        note.text = data.get('text', note.text)
        db.session.commit()
        return jsonify(note.to_dict())
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/notes/<int:id>', methods=['PATCH'])
def patch_note(id):
    note = Note.query.get(id)
    if note:
        data = request.json
        if 'text' in data:
            note.text = data['text']
        db.session.commit()
        return jsonify(note.to_dict())
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted"}), 200
    else:
        return jsonify({"error": "Note not found"}), 404

if __name__ == "__main__":
    app.run(port=os.getenv('PORT'), debug=True, host="0.0.0.0")
