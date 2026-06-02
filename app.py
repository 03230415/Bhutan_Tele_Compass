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
# create_client - creates a connection to supabase
# Client - the type of connection
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

# Start website + enable login memory
# {app = Flask(_name_)} === Flask, use this file as the starting point of the project.
app = Flask(__name__, static_folder=".")
app.secret_key = "telecompass_bhutan_2026"

# password and username for admin login
ADMIN_USERNAME = "yang"
ADMIN_PASSWORD = "dream"

# -----------------------------
# SUPABASE SETUP
# -----------------------------
# SUPABASE_URL - the address of your supabase project
# SUPABASE_KEY - the secret key to access your supabase project
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Safety check - prints warning if env variables are missing
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️  WARNING: SUPABASE_URL or SUPABASE_KEY is missing from .env file!")

# create a connection to supabase using the URL and KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# check login status of admin
def is_logged_in():
    return session.get("logged_in") == True   # yes, logged in so session remembers to keep it logged_in   #FALSE - no

# -----------------------------
# FRONTEND ROUTES
# -----------------------------
# homepage - when user goes to the website, show them the homepage (index.html)
@app.route("/")
def home():
    # send_from_directory - send a file from this folder to the user
    return send_from_directory(".", "index.html")

# login page
@app.route("/login")
def login_page():
    return send_from_directory(".", "login.html")

# admin dashboard
@app.route("/admin")
def admin_page():
    if not is_logged_in():
        return redirect("/login")
    return send_from_directory(".", "admin.html")

# Static file serving (CSS JS images)
# If someone asks for any file (CSS, JS, image, etc.), send it from my project folder.
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# -----------------------------
# AUTHENTICATION
# -----------------------------
# login door for the backend - when user tries to login, this function will check if the username and password are correct.
# @ - decorator - a way to connect or modify a function without changing its inside code.
# POST - when user submits the login form, it sends a POST request to the server with the username and password.
# methods=["POST"] - This route ONLY accepts data being sent to it, not just opened in a browser.
@app.route("/auth/login", methods=["POST"])
def login():
    # extract JSON data from request
    data = request.get_json()

    if (
        data.get("username") == ADMIN_USERNAME
        and data.get("password") == ADMIN_PASSWORD
    ):
        session["logged_in"] = True
        # jsonify - convert Python data into JSON format to send back to the frontend
        return jsonify({"success": True})

    return jsonify({
        "success": False,
        "error": "Wrong username or password."
    }), 401
    # 401 - unauthorized error code, means do not have the correct credentials.

# logout function
@app.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# -----------------------------
# CONTACT FORM
# -----------------------------
# Contact form message system
# save new messages
@app.route("/message", methods=["POST"])
def save_message():
    try:
        # Get JSON data sent through frontend
        data = request.get_json()
        print("📩 Received data:", data)  # shows in terminal when form is submitted

        # Extract and clean values
        # If name does NOT exist, use empty string  #strip - remove extra spaces before and after the text
        name    = data.get("name", "").strip()
        email   = data.get("email", "").strip()
        topic   = data.get("topic", "General")
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Name, email and message are required."
            }), 400

        # Create a unique message ID using current timestamp
        # converts seconds into milliseconds
        # int - integer
        message_id = int(datetime.now().timestamp() * 1000)

        # Bhutan Standard Time
        bhutan_time = datetime.now(
            # Bhutan is UTC +6
            timezone(timedelta(hours=6))
            # .strftime - format the date and time in a specific way
            # %y - year, %m - month, %d - day, %H - hour, %M - minute, %S - second
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Build the new message as a dictionary
        new_message = {
            "id":          message_id,
            "name":        name,
            "email":       email,
            "topic":       topic,
            "message":     message,
            # received_at - matches the column name in supabase table
            "received_at": bhutan_time
        }

        print("💾 Saving to Supabase:", new_message)  # shows in terminal before saving
        # Save message directly to supabase cloud database
        # .table("messages") - which table to save to
        # .insert(new_message) - add the new message
        # .execute() - run the command
        result = supabase.table("messages").insert(new_message).execute()
        print("✅ Supabase result:", result)           # shows in terminal after saving

        return jsonify({
            "success": True,
            "message": (
                "✅ Thank you! Your message has been received. "
                "We will reply within 2 business days."
            )
        })

    # exception - any python error
    # store the error in variable e
    except Exception as e:
        print("❌ Error saving message:", e)  # shows exact error in terminal
        return jsonify({
            "success": False,
            # str - string
            "error": str(e)
        }), 500


# -----------------------------
# ADMIN MESSAGE APIs
# -----------------------------
# Get all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    # Fetch all messages from supabase
    # .select("*") - get all columns
    # .order("id", desc=True) - newest message first
    result = supabase.table("messages").select("*").order("id", desc=True).execute()

    return jsonify({
        # len - how many items
        "total":    len(result.data),
        "messages": result.data
    })

# Delete single message
@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    # Delete the message from supabase where id matches
    # .eq("id", msg_id) - find the row where id equals msg_id
    supabase.table("messages").delete().eq("id", msg_id).execute()
    return jsonify({"success": True})

# delete all messages
@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    # Delete all messages from supabase
    # .neq("id", 0) - delete everything where id is not 0 (which is all rows)
    supabase.table("messages").delete().neq("id", 0).execute()
    return jsonify({"success": True})

# -----------------------------
# RUN SERVER
# -----------------------------
# his line makes sure the Flask server only starts when I run this file directly
if __name__ == "__main__":
    # Choose which port (door number) the website runs on
    # If server gives a port → use it Otherwise → use 5000
    port = int(os.environ.get("PORT", 5000))
    # system settings - environment variables - PORT

    # Start the web server so people can access your app.
    app.run(
        # Allow access from anywhere
        host="0.0.0.0",
        # This decides the address number of your website
        port=port,
        # Normal mode, not developer testing mode
        debug=False
    )