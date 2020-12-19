from flask import request, render_template, redirect, url_for
import app.utils.secret_santa as secret_santa
from app.utils.secret_santa import Participant
import json
from app import app, db

@app.route("/", methods=["GET", "POST"])
def secret_santa_match():
    if request.method == "POST":

        group_title = request.form.get("title")
        if not group_title:
            return display_status("Group titles are necessary!")

        participants = get_participants()

        # cannot match with only one person
        if len(participants) <= 1:
            return display_status("Not enough participants to match.")
        
        organizer_ids = get_organizer_ids()
        
        matches = secret_santa.match_people(participants)

        if matches != None:
            group_id = db.add_group(group_title)
            db.add_group_to_users(group_id, organizer_ids)
            db.add_participants(group_id, participants, matches)

            return redirect(url_for("group", group_id=group_id))
        
        else:
            return display_status("The matches could not be made. Try lowering the restrictions.")
    
    return render_template("secret_santa.html")

@app.route("/group/<group_id>", methods=["GET", "POST"])
def group(group_id):
    if not group_id.isnumeric():
        return display_status("This is not a valid group ID.")

    group_id = int(group_id)
    group = db.get_group(group_id)

    if not group:
        return display_status("This is not a valid group ID.")

    organizers = db.get_user_ids(group_id)
    participants = db.get_participants(group_id)
    matches = db.get_participant_matches(group_id, participants)

    if request.method == "POST":
        if request.form.get("formName") == "refreshMatches":
            new_matches = secret_santa.match_people(participants)
            db.update_participant_matches(group_id, new_matches)

        if request.form.get("formName") == "sendEmails":
            organizer_emails = db.get_user_emails(group_id)
            participant_email_matches = db.get_participant_email_matches(group_id)

            secret_santa.send_emails(
                organizer_emails, 
                participant_email_matches,
                "Hello, welcome to the secret santa, organizers!", 
                "Hello, welcome to secret santa!", 
                "<p>Hello, welcome to <strong>secret santa</strong>!</p>")
            
            return redirect(url_for("group", group_id=group_id))

    return render_template("group.html", group_title=group[0], organizers=organizers, matches=matches)

def display_status(status_msg):
    return render_template("status.html", status_msg=status_msg)

def get_organizer_ids():
    # get 15 organizers
    organizer_ids = []
    for i in range(15):
        organizer_id = request.form.get(f"organizer{i}")

        # add organizer by organizer_id
        if organizer_id:
            if organizer_id.isnumeric():
                organizer_ids.append(int(organizer_id))

            else:
                continue
    
        else:
            break

    return organizer_ids

def get_participants():
    # get 100 participants
    participants = []
    for i in range(100):
        participant = request.form.getlist(f"participant{i}")

        if participant == []:
            break

        name, email, restrictions = participant
        
        if name == "" and email == "":
            continue
        
        # if the user inserted a name that was too long
        if len(name) > 50 or len(email) > 100:
            return []
        
        if name == "":
            name = email
        
        # set email to none if it is blank, organizers will have to contact
        elif email == "":
            email = None
        
        restrictions = restrictions.splitlines()

        if restrictions == [""]:
            restrictions = []
        
        participants.append(Participant(i, name, email, restrictions))
    
    return participants
