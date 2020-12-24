from flask import session

def set_session_data(session, session_id, email):
    """Sets the session data for a user to remain logged in."""

    session["_id"] = session_id
    session["email"] = email

def get_session_data(session):
    """Gets the session data to check if a user is logged in."""
    
    return (session.get("_id"), session.get("email"))
