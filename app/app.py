from dotenv import load_dotenv
import os

# app
from flask import Flask, render_template, url_for, session

app = Flask(__name__)

# half a megabyte
app.config["MAX_CONTENT_LENGTH"] = 1024 * 512

app.secret_key = bytes(os.getenv("SECRET_KEY"), "utf-8")

from app.group import group
from app.auth import auth
from app.user import user
from app.helper_routes import helper

app.register_blueprint(group)
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(helper)

@app.context_processor
def check_user_login():
    return {
        "user_email" : session.get("email")
    }

@app.errorhandler(403)
def forbidden(e):
    return render_template("status.html", status_msg="403: Forbidden", description=f"You may need to <a href='{url_for('auth.login')}'>login</a> to your account to view this."), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template("status.html", status_msg="404: Page Not Found")
