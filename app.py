import uuid
from datetime import datetime

from flask import Flask, request, jsonify

from llm_detector import detect_with_llm
from audit import add_entry, get_entries

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    if "text" not in data or "creator_id" not in data:
        return jsonify({"error": "creator_id and text required"}), 400

    content_id = str(uuid.uuid4())

    result = detect_with_llm(data["text"])

    entry = {
        "content_id": content_id,
        "creator_id": data["creator_id"],
        "timestamp": datetime.utcnow().isoformat(),

        "attribution": result["attribution"],

        "confidence": result["score"],

        "llm_score": result["score"],

        "status": "classified"
    }

    add_entry(entry)

    return jsonify({
        "content_id": content_id,

        "attribution": result["attribution"],

        "confidence": result["score"],

        "label": "Placeholder label (Milestone 4)"
    })


@app.route("/log", methods=["GET"])
def log():

    return jsonify({
        "entries": get_entries()
    })


if __name__ == "__main__":
    app.run(debug=True)