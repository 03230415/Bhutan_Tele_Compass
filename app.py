# overall backend code for the website - python flask framework
# app.py - backend to receive text - python flask
# import and app setup 
# request → gets data from user (like form input)
# redirect → sends user to another page
from flask import Flask, request, jsonify, send_from_directory, session, redirect
# os - works with files and folders
import os
# for timestamp
from datetime import datetime, timezone, timedelta
# supabase - cloud database to store messages
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder=".")
app.secret_key = "telecompass_bhutan_2026"

ADMIN_USERNAME = "yang"
ADMIN_PASSWORD = "dream"

# -----------------------------
# SUPABASE SETUP
# -----------------------------
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Safety check - prints warning if env variables are missing
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️  WARNING: SUPABASE_URL or SUPABASE_KEY is missing from .env file!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def is_logged_in():
    return session.get("logged_in") == True

# -----------------------------
# FRONTEND ROUTES
# -----------------------------
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

# -----------------------------
# AUTHENTICATION
# -----------------------------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if (
        data.get("username") == ADMIN_USERNAME
        and data.get("password") == ADMIN_PASSWORD
    ):
        session["logged_in"] = True
        return jsonify({"success": True})

    return jsonify({
        "success": False,
        "error": "Wrong username or password."
    }), 401

@app.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# -----------------------------
# CONTACT FORM
# -----------------------------
@app.route("/message", methods=["POST"])
def save_message():
    try:
        data = request.get_json()
        print("📩 Received data:", data)  # shows in terminal when form is submitted

        name    = data.get("name", "").strip()
        email   = data.get("email", "").strip()
        topic   = data.get("topic", "General")
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Name, email and message are required."
            }), 400

        message_id = int(datetime.now().timestamp() * 1000)

        bhutan_time = datetime.now(
            timezone(timedelta(hours=6))
        ).strftime("%Y-%m-%d %H:%M:%S")

        new_message = {
            "id":          message_id,
            "name":        name,
            "email":       email,
            "topic":       topic,
            "message":     message,
            "received_at": bhutan_time
        }

        print("💾 Saving to Supabase:", new_message)  # shows in terminal before saving
        result = supabase.table("messages").insert(new_message).execute()
        print("✅ Supabase result:", result)           # shows in terminal after saving

        return jsonify({
            "success": True,
            "message": (
                "✅ Thank you! Your message has been received. "
                "We will reply within 2 business days."
            )
        })

    except Exception as e:
        print("❌ Error saving message:", e)  # shows exact error in terminal
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------
# ADMIN MESSAGE APIs
# -----------------------------
@app.route("/messages", methods=["GET"])
def get_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    result = supabase.table("messages").select("*").order("id", desc=True).execute()
    return jsonify({
        "total":    len(result.data),
        "messages": result.data
    })

@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    supabase.table("messages").delete().eq("id", msg_id).execute()
    return jsonify({"success": True})

@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    supabase.table("messages").delete().neq("id", 0).execute()
    return jsonify({"success": True})

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )