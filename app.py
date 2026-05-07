from flask import Flask, request, jsonify, send_from_directory, session, redirect
import json, os
from datetime import datetime

app = Flask(__name__, static_folder="public")

# ── Secret key for session ─────────────────────────
app.secret_key = "telecompass_bhutan_2026"

# ── Admin credentials (change these) ──────────────
ADMIN_USERNAME = "yang"
ADMIN_PASSWORD = "dream"

MESSAGES_FILE = "messages.json"

# ══════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════

def read_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def is_logged_in():
    return session.get("logged_in") == True

# ══════════════════════════════════════════════════
# PAGE ROUTES
# ══════════════════════════════════════════════════

@app.route("/")
def home():
    return send_from_directory("public", "index.html")

@app.route("/login")
def login_page():
    return send_from_directory("public", "login.html")

@app.route("/admin")
def admin_page():
    if not is_logged_in():
        return redirect("/login")
    return send_from_directory("public", "admin.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("public", filename)

# ══════════════════════════════════════════════════
# AUTH ROUTES
# ══════════════════════════════════════════════════

@app.route("/auth/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Wrong username or password."}), 401

@app.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route("/auth/check", methods=["GET"])
def check_auth():
    return jsonify({"logged_in": is_logged_in()})

# ══════════════════════════════════════════════════
# MESSAGE ROUTES
# ══════════════════════════════════════════════════

@app.route("/message", methods=["POST"])
def save_message():
    data    = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    topic   = data.get("topic", "General")
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Name, email and message are required."}), 400

    new_message = {
        "id":         int(datetime.now().timestamp() * 1000),
        "name":       name,
        "email":      email,
        "topic":      topic,
        "message":    message,
        "receivedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    all_messages = read_messages()
    all_messages.append(new_message)
    save_messages(all_messages)

    print(f"📬 Saved: {name} — {email}")

    return jsonify({
        "success": True,
        "message": "✅ Thank you! Your message has been received. We will reply within 2 business days."
    })

@app.route("/messages", methods=["GET"])
def get_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized. Please log in."}), 401
    messages = read_messages()
    return jsonify({"total": len(messages), "messages": messages})

@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401
    messages = read_messages()
    updated  = [m for m in messages if m["id"] != msg_id]
    if len(updated) == len(messages):
        return jsonify({"success": False, "error": "Message not found."}), 404
    save_messages(updated)
    return jsonify({"success": True, "message": "Deleted."})

@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401
    save_messages([])
    return jsonify({"success": True, "message": "All messages cleared."})

# ══════════════════════════════════════════════════
if __name__ == "__main__":
    app.run(debug=True)
