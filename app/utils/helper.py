from flask import redirect, url_for

def display_status(status_msg):
    return redirect(url_for("helper.status", status_msg=status_msg))
