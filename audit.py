import json
import os

LOG_FILE = "audit_log.json"


def load_log():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        return json.load(f)


def save_log(entries):

    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def add_entry(entry):

    entries = load_log()
    entries.append(entry)
    save_log(entries)


def get_entries():

    return load_log()