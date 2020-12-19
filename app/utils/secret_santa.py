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


def send_emails(organizer_emails, matches, organizer_message, message_text, message_html):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(SENDER_EMAIL, APP_PASSWORD)

    if len(organizer_emails) > 0:
        matches_text_list = [f"{gifter[0]}: {recipient_name}" for gifter, recipient_name in matches]

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

        server.sendmail(SENDER_EMAIL, organizer_emails, organizer_message.as_string())

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
