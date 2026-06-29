from uuid import uuid4
from datetime import datetime
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from audit import add_entry, get_entries, save_log
from scoring import compute_confidence, generate_label

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

@app.route("/submit", methods=["POST"])
@limiter.limit("20 per minute;200 per day")
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
    label = generate_label(raw_confidence)

    entry = {
        "content_id": content_id,
        "creator_id": data["creator_id"],
        "text": data["text"],
        "timestamp": datetime.utcnow().isoformat(),
        "attribution": attribution,
        "confidence": raw_confidence,
        "llm_score": result["llm_score"],
        "stylometric_score": result["stylometric_score"],
        "label": label,
        "status": "classified",
        "appealed": False
    }

    add_entry(entry)

    return {
        "content_id": content_id,
        "attribution": attribution,
        "confidence": display_confidence,
        "llm_score": round(result["llm_score"], 2),
        "stylometric_score": round(result["stylometric_score"], 2),
        "label": label
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

    found = False

    for entry in entries:
        if entry["content_id"] == content_id:
            entry["status"] = "under_review"
            entry["appealed"] = True
            entry["appeal_reasoning"] = reason
            found = True
            break

    if not found:
        return jsonify({"error": "content_id not found"}), 404

    save_log(entries)

    return jsonify({
        "message": "Appeal received",
        "content_id": content_id,
        "status": "under_review"
    })


if __name__ == "__main__":
    app.run(debug=True)