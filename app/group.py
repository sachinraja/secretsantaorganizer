from flask import Blueprint, request, render_template, redirect, url_for, session, abort
import json

from app import db
from app.utils import secret_santa
from app.utils.helper import display_status
from app.utils.auth import is_valid_uuid

group = Blueprint("group", __name__)

@group.route("/", methods=["GET", "POST"])
def create_group():
    if request.method == "POST":
        group_title = request.form.get("title")
        if not group_title:
            return display_status("Group titles are necessary.")

        if len(group_title) > 50:
            return display_status("Group titles can only be 50 characters.")
        
        # get messages to send for emails
        participant_text_message = request.form.get("participantTextMessage")
        if len(participant_text_message) > 2000:
            return display_status("Participant text message is too long (2000 character limit).")
        
        participant_html_message = request.form.get("participantHTMLMessage")
        if not participant_html_message:
            participant_html_message = f"<p>{participant_text_message}</p>"
        
        elif len(participant_html_message) > 2000:
            return display_status("Participant HTML message is too long (2000 character limit).")

        participants = secret_santa.get_participants(request.form)

        # cannot match with only two people
        if len(participants) <= 2:
            return display_status("Not enough participants to match.")
        
        organizer_emails = []

        # add email of person who created group as a group organizer
        group_creator_email = session.get("email")
        if group_creator_email:
            organizer_emails.append(group_creator_email)
        
        # add rest of organizers
        organizer_emails.extend(secret_santa.get_organizer_emails(request.form))
        organizer_emails = set(organizer_emails)

        matches = secret_santa.match_people(participants)

        if matches != None:
            if request.form.get("type") == "generate":
                group_id = db.add_group(group_title, participant_text_message, participant_html_message)
                db.add_group_to_users(group_id, organizer_emails)
                db.add_participants(group_id, participants, matches)

                return redirect(url_for("group.display_group", group_id=group_id))
            
            else:
                participant_email_matches = [((gifter.name, gifter.email), recipient.name) for gifter, recipient in matches.items()]

                secret_santa.send_emails(
                    participant_email_matches,
                    participant_text_message, 
                    participant_html_message)

                return display_status("Successfully sent emails!")
        
        else:
            return display_status("The matches could not be made. Try lowering the restrictions.")
    
    return render_template("create_group.html")

@group.route("/group/<group_id>", methods=["GET", "POST"])
def display_group(group_id):
    if not group_id.isnumeric():
        abort(404)

    group_id = int(group_id)
    group_title = db.get_group_title(group_id)

    if not group_title:
        abort(404)
    
    email = session.get("email")
    session_id = session.get("_id")

    # check if the user is authorized to access this group
    if not email or not is_valid_uuid(session_id):
        abort(403)

    if not db.validate_session_id(email, session_id):
        abort(403)

    if not db.user_in_group(group_id, email):
        abort(403)
                
    group_title = group_title[0]
    organizers = db.get_user_emails(group_id)
    participants = db.get_participants(group_id)
    matches = db.get_participant_matches(group_id, participants)

    sent_emails = db.group_email_status(group_id)

    if request.method == "POST":
        if request.form.get("formName") == "refreshMatches":
            new_matches = secret_santa.match_people(participants)
            db.update_participant_matches(group_id, new_matches)

        elif request.form.get("formName") == "sendEmails":
            text_message, html_message = db.get_group_messages(group_id)
            
            participant_email_matches = db.get_participant_email_matches(group_id)
            
            secret_santa.send_emails(participant_email_matches, text_message, html_message)
            db.group_sent_emails(group_id)

        return redirect(url_for("group.display_group", group_id=group_id))
    
    return render_template("group.html", sent_emails=sent_emails, group_title=group_title, organizers=organizers, matches=matches)
