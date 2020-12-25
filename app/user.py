from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify

from app import db
from app.utils.helper import display_status
from app.utils.auth import is_valid_uuid

user = Blueprint("user", __name__)

@user.route("/groups", methods=["GET", "POST"])
def groups():
    email = session.get("email")
    session_id = session.get("_id")

    user_groups = []
    if email and is_valid_uuid(session_id):
        if db.authenticate_user_session_id(email, session_id):
            user_groups = db.get_user_group_titles(email)

        else:
            return display_status("User's email or session ID (logout and login to reset) is not valid.")
    
    else:
        return display_status("You need an account in order to manage and view groups.")
    
    return render_template("user_groups.html", groups=user_groups)

@user.route("/get-group-titles", methods=["POST"])
def get_group_titles():
    offset = request.json.get("offset")
    if offset == None:
        return "failure", 400
    
    if not type(offset) is int:
        return "failure", 400
    
    offset = int(offset)
    
    email = session.get("email")
    session_id = session.get("_id")

    if email and is_valid_uuid(session_id):
        if db.authenticate_user_session_id(email, session_id):
            return jsonify(db.get_user_group_titles(email, offset=offset))

    return "failure", 403

