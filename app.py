from flask import Flask, request, jsonify, send_from_directory, session, redirect
import os, json
from datetime import datetime

app = Flask(__name__, static_folder=".")
app.secret_key = "telecompass_bhutan_2026"

ADMIN_USERNAME = "yang"
ADMIN_PASSWORD = "dream"
MESSAGES_FILE  = "messages.json"

# ── Use Supabase on Render, JSON locally ───────────
USE_SUPABASE = os.environ.get("RENDER") is not None

if USE_SUPABASE:
    from supabase import create_client
    SUPABASE_URL = "https://cdlimimarqcyvngnhuaw.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkbGltaW1hcnFjeXZuZ2hudWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwNTUwMTIsImV4cCI6MjA5MzYzMTAxMn0.EChGAPwRF28ecxUMLauTVtedcIE8JBeUwyMQIIopw6U"
    db = create_client(SUPABASE_URL, SUPABASE_KEY)

def is_logged_in():
    return session.get("logged_in") == True

# ── JSON helpers (local only) ──────────────────────
def read_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# ══════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/login")
def login_page():
    return send_from_directory(".", "login.html")

@app.route("/admin")
def admin_page():
    if not is_logged_in():
        return redirect("/login")
    return send_from_directory(".", "admin.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# ══════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════

@app.route("/auth/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Wrong username or password."}), 401

@app.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# ══════════════════════════════════════════════════
# MESSAGES
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

    if USE_SUPABASE:
        db.table("messages").insert({
            "name": name, "email": email,
            "topic": topic, "message": message
        }).execute()
    else:
        all_messages = read_messages()
        all_messages.append({
            "id":         int(datetime.now().timestamp() * 1000),
            "name":       name,
            "email":      email,
            "topic":      topic,
            "message":    message,
            "receivedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_messages(all_messages)

    return jsonify({
        "success": True,
        "message": "✅ Thank you! Your message has been received. We will reply within 2 business days."
    })

@app.route("/messages", methods=["GET"])
def get_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401
    if USE_SUPABASE:
        result = db.table("messages").select("*").order("id", desc=True).execute()
        return jsonify({"total": len(result.data), "messages": result.data})
    else:
        messages = read_messages()
        return jsonify({"total": len(messages), "messages": messages})

@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401
    if USE_SUPABASE:
        db.table("messages").delete().eq("id", msg_id).execute()
    else:
        messages = read_messages()
        save_messages([m for m in messages if m["id"] != msg_id])
    return jsonify({"success": True, "message": "Deleted."})

@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401
    if USE_SUPABASE:
        db.table("messages").delete().neq("id", 0).execute()
    else:
        save_messages([])
    return jsonify({"success": True, "message": "All messages cleared."})

# ══════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)