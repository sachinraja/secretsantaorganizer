from flask import Flask, request, render_template, redirect, url_for
import secret_santa
from secret_santa import Person

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def secret_santa_match():
    if request.method == "POST":

        # get 15 organizers
        organizers = []
        for i in range(15):
            organizer = request.form.getlist(f"organizer{i}")

            if organizer == []:
                break

            name, email = organizer

            # check first two fields (name, email)
            if name == "" and email == "":
                continue
            
            # set name to email if it is blank
            if name == "":
                name = email

            # continue, can't fulfill function of organizer without email
            elif email == "":
                continue

            organizers.append(Person(name, email))
        
        # get 100 participants
        participants = []
        for i in range(100):
            participant = request.form.getlist(f"participant{i}")

            if participant == []:
                break

            name, email, restrictions = participant

            
            if name == "" and email == "":
                continue
            
            if name == "":
                name = email
            
            # set email to none if it is blank, organizers will have to contact
            elif email == "":
                email = None;
            
            restrictions = restrictions.split("\r\n")

            if restrictions == [""]:
                restrictions = []
            
            participants.append(Person(name, email, restrictions))
        
        matches = secret_santa.match_people(participants)

        if matches != None:
            secret_santa.send_emails(organizers, 
            matches, 
            "Welcome organizers! It is your duties to ensure everyone is performing their duties, ironic, I know, but still.", 
            "Hello, welcome to the first secret santa!", 
            "<p>Hello, welcome to the first secret santa!</p>")
        
        return redirect(url_for("secret_santa_match"))
    
    return render_template("secret_santa.html")

app.run()