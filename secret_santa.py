import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

class Person:
    def __init__(self, name, email=None, restrictions=[]):
        self.name = name
        self.email = email
        self.restrictions = restrictions

def match_people(start_people):
    # randomize
    random.shuffle(start_people)
    # sort by number of restrictions: max to min
    people = sorted(start_people, key=lambda person: len(person.restrictions), reverse=True)

    matches = {}

    for person in people:

        iteration_count = 0
        # iterate from most restrictions to least restrictions, 
        # trying to match most restricted people first
        for potential_match in people:
            # if potential_match is not also the person trying to be matched and 
            # not already matched and 
            # is not restricted and 
            # does not have the person trying to get matched
            if (potential_match != person and 
            potential_match not in matches.values() and 
            potential_match.name not in person.restrictions and 
            matches.get(potential_match) != person):
                matches[person] = potential_match
                break

            if iteration_count == len(people) - 1:
                matches[person] = "Unmatched"
                return None
            
            iteration_count += 1
    
    return matches


def send_emails(organizers, matches, organizer_message, message_text, message_html):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(SENDER_EMAIL, APP_PASSWORD)

    matches_text_list = [f"{person[0].name}: {person[1].name}" for person in matches.items()]

    organizer_text_message = f"{organizer_message}\n\n"
    organizer_text_message += "".join([f"-{text}\n" for text in matches_text_list])

    organizer_html_message = f"""\
    <html>
        <body>
            <p>
                {organizer_message}
            </p>
            
            <ul>
                <li>Gifter: Recipient</li>
                {"".join([f"<li>{text}</li>" for text in matches_text_list])}
            </ul>
        </body>
    </html>
    """

    organizer_message = MIMEMultipart("alternative")
    organizer_message["Subject"] = "Secret Santa Matches"
    organizer_message["From"] = f"Secret Santa Organizer <{SENDER_EMAIL}>"

    organizer_part_1 = MIMEText(organizer_text_message, "plain")
    organizer_part_2 = MIMEText(organizer_html_message, "html")

    organizer_message.attach(organizer_part_1)
    organizer_message.attach(organizer_part_2)

    server.sendmail(SENDER_EMAIL, [organizer.email for organizer in organizers], organizer_message.as_string())

    for person in matches.items():
        if person[0].email == None:
            continue

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Secret Santa"
        msg["From"] = f"Secret Santa Organizer <{SENDER_EMAIL}>"
        msg["To"] = person[0].email
        
        # Create the body of the message (a plain-text and an HTML version)
        text = f"Your person is {person[1].name}.\n\n{message_text}"
        
        html = f"""\
        <html>
            <body>
                <p>Your person is <strong>{person[1].name}</strong>.</p>
                {message_html}
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(SENDER_EMAIL, person[0].email, msg.as_string())

    server.quit()


def log(matches):
    log_message = ""

    for person in matches.items():
        log_message += f"{person[0].name} has to get a gift for {person[1]}\n"

    with open("secret_santa_log.txt", "w") as f:
        f.write(log_message)
