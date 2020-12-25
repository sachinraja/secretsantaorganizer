from flask import Blueprint, request, render_template, redirect, url_for, session

from app import db
from app.utils.helper import display_status
from app.utils.session import set_session_data
from app.utils.auth import is_valid_uuid

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    # check session data
    session_id = session.get("_id")
    email = session.get("email")

    if email and is_valid_uuid(session_id):
        if db.validate_session_id(email, session_id):
            return display_status("Logged in already!")

    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        session_data = db.authenticate_user(email, password)

        if session_data:
            set_session_data(session, *session_data)
            return redirect(url_for("user.groups"))
        
        return render_template("login.html", error="Incorrect email or password.")
    
    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email").lower()
        if len(email) > 200:
            return display_status("Emails can only be 200 characters.")
        
        password = request.form.get("password")
        if len(password) > 72:
            return display_status("Passwords can only be 72 characters.")
        
        if db.user_exists(email):
            return display_status(f"User with email {email} already exists!")
        
        session_id = db.add_user(email, password)
        set_session_data(session, session_id, email)

        return redirect(url_for("group.create_group"))
    
    return render_template("signup.html")

@auth.route("/logout", methods=["POST"])
def logout():
    session_id = session.get("_id")
    email = session.get("email")

    if email and is_valid_uuid(session_id):
        if db.validate_session_id(email, session_id):
            db.remove_session_id(email)
    
            session.clear()
            return "success"
    
    return "failure"
