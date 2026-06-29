from uuid import uuid4
from datetime import datetime
from flask import Flask, request, jsonify
from llm_detector import llm_score
from audit import add_entry, get_entries
from scoring import compute_confidence, generate_label

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    result = compute_confidence(data["text"])

    raw_confidence = result["confidence"]
    display_confidence = round(raw_confidence, 2)

    # classification thresholds
    if raw_confidence >= 0.65:
        attribution = "likely_ai"
    elif raw_confidence < 0.4:
        attribution = "likely_human"
    else:
        attribution = "uncertain"

    content_id = str(uuid4())

    entry = {
        "content_id": content_id,
        "creator_id": data["creator_id"],
        "text": data["text"],
        "timestamp": datetime.utcnow().isoformat(),
        "attribution": attribution,
        "confidence": raw_confidence,
        "llm_score": result["llm_score"],
        "stylometric_score": result["stylometric_score"],
        "status": "classified"
    }

    add_entry(entry)

    return {
        "content_id": content_id,
        "attribution": attribution,
        "confidence": display_confidence,
        "llm_score": round(result["llm_score"], 2),
        "stylometric_score": round(result["stylometric_score"], 2),
        "label": generate_label(raw_confidence)
    }


@app.route("/log", methods=["GET"])
def log():

    return jsonify({
        "entries": get_entries()
    })


if __name__ == "__main__":
    app.run(debug=True)