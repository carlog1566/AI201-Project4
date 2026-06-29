from uuid import uuid4
from datetime import datetime
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from llm_detector import llm_score
from audit import add_entry, get_entries
from scoring import compute_confidence, generate_label

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
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

@app.route("/appeal", methods=["POST"])
def appeal():
    data = request.get_json()

    content_id = data["content_id"]
    reason = data["creator_reasoning"]

    entries = get_entries()

    updated = None

    for entry in entries:
        if entry["content_id"] == content_id:
            entry["status"] = "under_review"
            entry["appeal_reasoning"] = reason
            updated = entry
            break

    if not updated:
        return jsonify({"error": "content_id not found"}), 404

    add_entry({
        "type": "appeal",
        "content_id": content_id,
        "creator_reasoning": reason,
        "timestamp": datetime.utcnow().isoformat()
    })

    return jsonify({
        "message": "Appeal received",
        "content_id": content_id,
        "status": "under_review"
    })


if __name__ == "__main__":
    app.run(debug=True)