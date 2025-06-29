import json
import os
import ast
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Paths to your data files
UNANSWERED_QUESTIONS_FILE = "unanswered_questions.json"
ANSWERED_QUESTIONS_FILE = "answered_questions.json"
UNIVERSITY_DATA_FILE = "university_data.py"

def safe_json_load(file_path):
    """Safely loads a JSON file, returning an empty list if it's empty or invalid."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            if os.fstat(f.fileno()).st_size == 0:
                return []
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def get_university_data_dict():
    """Reads and safely evaluates the university_data.py file content."""
    with open(UNIVERSITY_DATA_FILE, "r") as f:
        content = f.read()
        dict_start = content.find('{')
        return ast.literal_eval(content[dict_start:])

def save_university_data_dict(data):
    """Saves the dictionary back to the university_data.py file."""
    new_content = "university_data = " + json.dumps(data, indent=4)
    with open(UNIVERSITY_DATA_FILE, "w") as f:
        f.write(new_content)

@app.route("/")
def index():
    """Renders the main web page."""
    return render_template("index.html")

@app.route("/get_questions", methods=["GET"])
def get_questions():
    """Returns the list of unanswered questions."""
    return jsonify({"unanswered": safe_json_load(UNANSWERED_QUESTIONS_FILE)})

@app.route("/get_answered_questions", methods=["GET"])
def get_answered_questions():
    """Returns the list of answered questions."""
    return jsonify({"answered": safe_json_load(ANSWERED_QUESTIONS_FILE)})

@app.route("/answer_question", methods=["POST"])
def answer_question():
    """Moves a question from unanswered to answered."""
    data = request.get_json()
    question_to_answer = data.get("question")
    answer = data.get("answer", "No answer provided.")

    unanswered = safe_json_load(UNANSWERED_QUESTIONS_FILE)
    updated_unanswered = [q for q in unanswered if q['question'] != question_to_answer]
    with open(UNANSWERED_QUESTIONS_FILE, "w") as f:
        json.dump(updated_unanswered, f, indent=4)

    answered = safe_json_load(ANSWERED_QUESTIONS_FILE)
    answered.append({"question": question_to_answer, "answer": answer})
    with open(ANSWERED_QUESTIONS_FILE, "w") as f:
        json.dump(answered, f, indent=4)

    return jsonify({"success": True})

@app.route("/get_university_data", methods=["GET"])
def get_university_data_route():
    try:
        return jsonify(get_university_data_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_section", methods=["POST"])
def update_section():
    """Updates a specific top-level section of the university data."""
    data = request.get_json()
    section_key = data.get("section")
    section_data_str = data.get("data")

    if not section_key or section_data_str is None:
        return jsonify({"success": False, "error": "Missing section key or data."})

    try:
        new_section_data = json.loads(section_data_str)
    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "Invalid JSON format in the provided data."})

    try:
        full_data = get_university_data_dict()
        full_data[section_key] = new_section_data
        save_university_data_dict(full_data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add_section", methods=["POST"])
def add_section():
    """Adds a new top-level section to the university data."""
    data = request.get_json()
    section_key = data.get("key")
    section_data_str = data.get("data")

    if not section_key or section_data_str is None:
        return jsonify({"success": False, "error": "Missing section key or data."})

    try:
        new_section_data = json.loads(section_data_str)
    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "Invalid JSON format in the provided data."})

    try:
        full_data = get_university_data_dict()
        if section_key in full_data:
            return jsonify({"success": False, "error": f"Section '{section_key}' already exists."})

        full_data[section_key] = new_section_data
        save_university_data_dict(full_data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)