import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

class Participant:
    def __init__(self, participant_id, name, email=None, restrictions=[]):
        self.participant_id = participant_id
        self.name = name
        self.email = email
        self.restrictions = restrictions

def match_people(start_people):
    # randomize
    random.shuffle(start_people)
    # sort by number of restrictions: max to min
    people = sorted(start_people, key=lambda person: len(person.restrictions), reverse=True)
    potential_matches = people.copy()
    matches = {}

    # iterate from most restrictions to least restrictions, 
    # trying to match most restricted people first
    for person in people:
        for i, potential_match in enumerate(potential_matches):
            # if potential_match is not also the person trying to be matched and
            # is not restricted and 
            # does not have the person trying to get matched
            if (potential_match != person and
            potential_match.name not in person.restrictions and
            matches.get(potential_match) != person):
                matches[person] = potential_match

                potential_matches.pop(i)
                break
            
            # person could not be matched
            if i == len(potential_matches) - 1:
                # attempt to replace from an earlier match
                for i, (gifter, recipient) in enumerate(matches.items()):
                    if (person != recipient and
                    recipient.name not in person.restrictions and
                    matches.get(recipient) != person and
                    person.name not in gifter.restrictions):
                        matches[gifter] = person
                        matches[person] = recipient
                        break
                    
                    # no replacements could be made
                    if i == len(matches) - 1:
                        return None
    
    return matches


def send_emails(matches, message_text, message_html):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    
    for gifter, recipient_name in matches:
        if gifter[1] == None:
            continue

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Secret Santa"
        msg["From"] = f"Secret Santa Organizer <{SENDER_EMAIL}>"
        msg["To"] = gifter[1]
        
        # Create the body of the message (a plain-text and an HTML version)
        text = f"Your person is {recipient_name}.\n\n{message_text}"
        
        html = f"""\
        <html>
            <body>
                <p>Your person is <strong>{recipient_name}</strong>.</p>
                {message_html}
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(SENDER_EMAIL, gifter[1], msg.as_string())

    server.quit()


def log(matches):
    log_message = ""

    for gifter, recipient_name in matches:
        log_message += f"{gifter[0]} has to get a gift for {recipient_name}\n"

    with open("secret_santa_log.txt", "w") as f:
        f.write(log_message)

def get_organizer_emails(form):
    """Get up to 15 organizer emails from an input form."""

    return form.getlist("organizer")[:15]

def get_participants(form):
    """Get up to 100 participants from an input form."""

    participants = []
    null_participants = 0
    for i in range(100):
        participant = form.getlist(f"participant{i}")

        if participant == []:
            null_participants += 1

            if null_participants >= 5:
                break
            
            continue

        name, email, restrictions = participant
        
        if name == "" and email == "":
            continue
        
        # if the user inserted a name or email that was too long
        if len(name) > 50 or len(email) > 200:
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

