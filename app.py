# app.py - backend to receive text - python flask
# import and app setup 
# request → gets data from user (like form input)
# redirect → sends user to another page
from flask import Flask, request, jsonify, send_from_directory, session, redirect
# os - works with files and folders
import os
import json
# for timestamp
from datetime import datetime, timezone, timedelta

# Start website + enable login memory
# {app = Flask(_name_)} === Flask, use this file as the starting point of the project.
app = Flask(__name__, static_folder=".")
app.secret_key = "telecompass_bhutan_2026"

# password and username for admin login
ADMIN_USERNAME = "yang"
ADMIN_PASSWORD = "dream"
# Use the file called messages.json to store contact form messages.
MESSAGES_FILE = "messages.json"

# check login status of admin
def is_logged_in():
    return session.get("logged_in") == True   # yes, logged in so session remembers to keep it logged_in   #FALSE - no

# read message from JSON files
def read_messages():
    """
    Read all messages from messages.json.

    If the file does not exist, return an empty list.
    """
    if not os.path.exists(MESSAGES_FILE):
        return []

    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

# save messages to JSON file
def save_messages(messages):
    """
    Save the given list of messages to messages.json.

    indent=2 makes the JSON file nicely formatted and readable.
    """
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# fronend page route
# hoempage
@app.route("/")
def home():
    """
    Serve the main homepage.
    URL: /
    Returns: index.html
    """
    return send_from_directory(".", "index.html")

# login page
@app.route("/login")
def login_page():
    """
    Serve the admin login page.
    URL: /login
    Returns: login.html
    """
    return send_from_directory(".", "login.html")

# admin dashboard
@app.route("/admin")
def admin_page():
    """
    Serve the admin dashboard.

    Only accessible if the admin is logged in.
    Otherwise redirects to /login.
    """
    if not is_logged_in():
        return redirect("/login")

    return send_from_directory(".", "admin.html")

# Static file serving (CSS JS images)
@app.route("/<path:filename>")
def static_files(filename):
    """
    Serve static files such as:
    - CSS files
    - JavaScript files
    - Images
    - Other HTML pages

    Example:
    /styles.css
    /script.js
    /img3.png
    """
    return send_from_directory(".", filename)

# Authentication system
# login
@app.route("/auth/login", methods=["POST"])
def login():
    """
    Handle admin login.

    Expects JSON:
    {
        "username": "...",
        "password": "..."
    }

    If credentials match:
        session["logged_in"] = True

    Returns:
        {"success": True}
    or
        {"success": False, "error": "..."}
    """
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

# logout
@app.route("/auth/logout", methods=["POST"])
def logout():
    """
    Log out the admin user.

    session.clear() removes all session data.
    """
    session.clear()
    return jsonify({"success": True})

# Contact form message system
# save new messages
@app.route("/message", methods=["POST"])
def save_message():
    """
    Save a new message submitted from the contact form.

    Expected JSON:
    {
        "name": "...",
        "email": "...",
        "topic": "...",
        "message": "..."
    }

    Stores the message in messages.json.
    """
    try:
        # Get JSON data sent through frontend
        data = request.get_json()

        # Extract and clean values
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        topic = data.get("topic", "General")
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Name, email and message are required."
            }), 400

        # Load existing messages
        all_messages = read_messages()

        # Create a unique message ID using current timestamp
        message_id = int(datetime.now().timestamp() * 1000)

        # Bhutan Standard Time 
        bhutan_time = datetime.now(
            timezone(timedelta(hours=6))
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Add new message to list
        all_messages.append({
            "id": message_id,
            "name": name,
            "email": email,
            "topic": topic,
            "message": message,
            "receivedAt": bhutan_time
        })

        # Save updated list 
        save_messages(all_messages)

        return jsonify({
            "success": True,
            "message": (
                "✅ Thank you! Your message has been received. "
                "We will reply within 2 business days."
            )
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Admin message APIs
# Get all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    """
    Return all saved messages.

    Only accessible to logged-in admin.
    """
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    messages = read_messages()

    return jsonify({
        "total": len(messages),
        "messages": messages
    })


# Delete single message
@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    """
    Delete a single message by ID.

    Example:
    DELETE /messages/123456789
    """
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    updated_messages = [
        m for m in read_messages()
        if m["id"] != msg_id
    ]

    save_messages(updated_messages)

    return jsonify({"success": True})

# delete all message
@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():
    """
    Delete all messages.

    Used by the 'Clear All Messages' button.
    """
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    save_messages([])

    return jsonify({"success": True})


# @app.errorhandler(404)
# def not_found(e):
#     """
#     Show custom 404 page when a route is not found.
#     """
#     return send_from_directory(".", "404.html"), 404


# @app.errorhandler(500)
# def server_error(e):
#     """
#     Show custom 500 page for internal server errors.
#     """
#     return send_from_directory(".", "500.html"), 500

# run server
if __name__ == "__main__":
    """
    Start the Flask development server.

    Render automatically provides a PORT environment variable.
    If PORT is not set, default to 5000.
    """
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )