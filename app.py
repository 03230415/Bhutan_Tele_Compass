# overall backend code for the website - python flask framework
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
    # Does the file messages.json exist on the computer?
    if not os.path.exists(MESSAGES_FILE):
        # Return an empty list instead of crashing
        return []

    # r - read mode #opens messages.json
    # f - file you just opened
    with open(MESSAGES_FILE, "r") as f:
    # If file doesn’t exist → ❌ error
    # Read the file and convert JSON text into Python data
        return json.load(f)

# save messages to JSON file
# receives message
def save_messages(messages):
    # w - write mode
    # create the file if it doesn’t exist
    # overwrite everything if it already exists
    # Open messages.json so I can write into it
    with open(MESSAGES_FILE, "w") as f:
        # Take Python data and convert it into JSON, then write it into the file
        # dump - write into notebook   #f - file   #intend=2 - neat handwriting
        json.dump(messages, f, indent=2)

# fronend page route
# hoempage - when user goes to the website, show them the homepage (index.html)
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





# Authentication system
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

# Contact form message system
# save new messages
@app.route("/message", methods=["POST"])
def save_message():
    try:
        # Get JSON data sent through frontend
        data = request.get_json()

        # Extract and clean values
        # If name does NOT exist, use empty string  #strip - remove extra spaces before and after the text
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
        # 1.opens messages.json 2.reads the file 3.converts JSON text into Python data 4.returns the data
        all_messages = read_messages()

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

    # exception - any python error
    # store the error in variable e
    except Exception as e:
        print("Error:", e)

        return jsonify({
            "success": False,
            # str - string
            "error": str(e)
        }), 500


# Admin message APIs
# Get all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    messages = read_messages()

    return jsonify({
        # len - how many items
        "total": len(messages),
        "messages": messages
    })


# Delete single message
@app.route("/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized."}), 401

    # Make a new list of messages, but skip the one I want to delete.
    updated_messages = [
        # first "m" - This is what you want to keep in the new list
        m for m in read_messages()
        # msg_id - the id of the message you want to delete
        if m["id"] != msg_id
    ]

    save_messages(updated_messages)

    return jsonify({"success": True})

# delete all message
@app.route("/messages/clear", methods=["DELETE"])
def clear_messages():

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