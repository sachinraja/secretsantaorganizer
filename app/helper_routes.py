from flask import Blueprint, request, render_template

helper = Blueprint("helper", __name__)

@helper.route("/status")
def status():
    return render_template("status.html", status_msg=request.args.get("status_msg"))
