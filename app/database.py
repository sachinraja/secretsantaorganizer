from app.utils.secret_santa import Participant

class Database:
    def __init__(self, conn, schema_filepath):
        self.conn = conn
        self.schema_filepath = schema_filepath
        self.load()

    def load(self):
        """Runs the SQL to create the schema."""

        cur = self.conn.cursor()
        cur.execute(open(self.schema_filepath, "r").read())
        self.conn.commit()
        cur.close()

    def drop(self):
        """Drops the Schema."""

        cur = self.conn.cursor()
        cur.execute("DROP SCHEMA app CASCADE;")
        self.conn.commit()
        cur.close()

    def add_group(self, group_title, participant_text_message, participant_html_message):
        """Inserts a group and returns its ID."""

        cur = self.conn.cursor()
        cur.execute("INSERT INTO app.group (group_title, participant_text_message, participant_html_message) VALUES (%s, %s, %s) RETURNING group_id;", (group_title, participant_text_message, participant_html_message))
        group_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        return group_id

    def add_group_to_users(self, group_id, user_emails):
        """Adds a group to users."""

        cur = self.conn.cursor()
        for user_email in user_emails:
            cur.execute("SELECT EXISTS (SELECT 1 FROM app.user WHERE user_email=%s);", (user_email,))
            
            if cur.fetchone()[0]:
                cur.execute("INSERT INTO app.user_group (user_email, group_id) VALUES (%s, %s);", (user_email, group_id))

        self.conn.commit()
        cur.close()

    def user_in_group(self, group_id, user_email):
        """Check if a user is in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM app.user_group WHERE user_email=%s AND group_id=%s LIMIT 1);", (user_email, group_id))
        user_in_group = cur.fetchone()[0]
        cur.close()

        return user_in_group
        
    def add_participants(self, group_id, participants, matches):
        """Insert participants under a group_id."""

        cur = self.conn.cursor()
        for participant in participants:

            if participant.email == None:
                participant.email = "NULL"

            cur.execute("INSERT INTO app.participant (group_id, participant_id, participant_name, participant_email, recipient_id) VALUES (%s, %s, %s, %s, %s);", (group_id, participant.participant_id, participant.name, participant.email, matches[participant].participant_id))

            for restriction in participant.restrictions:
                cur.execute("INSERT INTO app.participant_restriction (group_id, participant_id, restriction) VALUES (%s, %s, %s);", (group_id, participant.participant_id, restriction))

        self.conn.commit()
        cur.close()

    def add_user(self, user_email, user_password):
        """Inserts a user and returns the session id."""

        cur = self.conn.cursor()
        cur.execute("INSERT INTO app.user (user_email, user_password) VALUES (%s, crypt(%s, gen_salt('bf'))) RETURNING user_session_id;", (user_email, user_password))
        session_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        return session_id
    
    def user_exists(self, user_email):
        """Check if there is a user with user_email."""

        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM app.user WHERE user_email=%s LIMIT 1);", (user_email,))
        _user_exists = cur.fetchone()[0]
        cur.close()
        
        return _user_exists
    
    def get_user(self, user_email):
        """Get a user."""

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM app.user WHERE user_email=%s LIMIT 1;", (user_email,))
        user = cur.fetchone()
        cur.close()

        return user

    def authenticate_user(self, user_email, user_password):
        """Verify if a user's password is correct. Returns the session_id if the user is authenticated."""
        
        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM app.user WHERE user_email=%s AND user_password=crypt(%s, user_password) LIMIT 1);", (user_email, user_password))
        user_authenticated = cur.fetchone()[0]
        session_data = None

        if user_authenticated:
            cur.execute("""WITH updates AS (
                UPDATE app.user SET user_session_id=uuid_generate_v4()
                WHERE user_email=%s
                RETURNING user_session_id, user_email)
                SELECT * FROM updates
                LIMIT 1;""", (user_email,))
            
            session_data = cur.fetchone()
            self.conn.commit()
        
        cur.close()

        return session_data
    
    def authenticate_user_session_id(self, user_email, user_session_id):
        """Check if the user's session id is correct."""

        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM app.user WHERE user_email=%s AND user_session_id=%s LIMIT 1);", (user_email, user_session_id))
        user_authenticated = cur.fetchone()[0]
        cur.close()

        return user_authenticated
    
    def get_user_session_id(self, user_email):
        """Get user's current, valid session id."""

        cur = self.conn.cursor()
        cur.execute("SELECT user_session_id FROM app.user WHERE user_email=%s LIMIT 1;", (user_email,))
        user_session_id = cur.fetchone()[0]
        cur.close()

        return user_session_id

    def get_user_group_titles(self, user_email, offset=0):
        """Get 12 titles of groups that a user owns starting at the offset."""

        cur = self.conn.cursor()
        cur.execute("SELECT group_id FROM app.user_group WHERE user_email=%s;", (user_email,))
        cur.execute("""SELECT group_id FROM app.user_group
        WHERE user_email=%s
        ORDER BY group_id
        OFFSET %s ROWS
        FETCH FIRST 12 ROW ONLY;""", (user_email, offset))

        group_ids = [group_attrs[0] for group_attrs in cur.fetchall()]
        
        groups = []
        for group_id in group_ids:
            cur.execute("SELECT group_title FROM app.group WHERE group_id=%s LIMIT 1;", (group_id,))
            groups.append((group_id, cur.fetchone()[0]))
        
        cur.close()

        return groups
    
    def get_all_users(self):
        """Gets a list of all the users."""
        
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM app.user;")
        users = cur.fetchall()
        cur.close()

        return users
    
    def get_all_user_group_matches(self):
        """Gets a list of all the group and user pairings."""

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM app.user_group;")
        user_groups = cur.fetchall()
        cur.close()

        return user_groups
    
    def validate_session_id(self, user_email, session_id):
        """Check if the session_id is valid for user_email."""

        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM app.user WHERE user_email=%s AND user_session_id::text=%s LIMIT 1);", (user_email, session_id))
        user_validated = cur.fetchone() != None
        cur.close()

        return user_validated
    
    def remove_session_id(self, user_email):
        """Remove the session id from a user (set to null)."""

        cur = self.conn.cursor()
        cur.execute("UPDATE app.user SET user_session_id=NULL WHERE user_email=%s", (user_email,))
        self.conn.commit()
        cur.close()
    
    def get_group_title(self, group_id):
        """Get a group's title."""

        cur = self.conn.cursor()
        cur.execute("SELECT group_title FROM app.group WHERE group_id=%s LIMIT 1;", (group_id,))
        group_title = cur.fetchone()
        cur.close()

        return group_title

    def get_group_messages(self, group_id):
        """Get a group's messages to send to participants."""

        cur = self.conn.cursor()
        cur.execute("SELECT participant_text_message, participant_html_message FROM app.group WHERE group_id=%s LIMIT 1;", (group_id,))
        group_messages = cur.fetchone()
        cur.close()

        return group_messages

    def group_sent_emails(self, group_id):
        """Set sent_emails to True for a group."""

        cur = self.conn.cursor()
        cur.execute("UPDATE app.group SET sent_emails=true WHERE group_id=%s;", (group_id,))
        self.conn.commit()
        cur.close()
        
        return True
    
    def group_email_status(self, group_id):
        """Get if the emails were sent in a group or not."""

        cur = self.conn.cursor()
        cur.execute("SELECT sent_emails FROM app.group WHERE group_id=%s LIMIT 1;", (group_id,))
        sent_emails = cur.fetchone()[0]
        cur.close()

        return sent_emails
        
    def get_user_emails(self, group_id):
        """Get all users in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT user_email FROM app.user_group WHERE group_id=%s;", (group_id,))
        users = cur.fetchall()
        cur.close()

        return [user_fields[0] for user_fields in users]

    def get_participants(self, group_id):
        """Get all participants in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT participant_id, participant_name FROM app.participant WHERE group_id=%s;", (group_id,))

        participants = [Participant(*participant) for participant in cur.fetchall()]

        # get restrictions for each participant
        for participant in participants:
            cur.execute("SELECT restriction FROM app.participant_restriction WHERE group_id=%s AND participant_id=%s;", (group_id, participant.participant_id))
            participant.restrictions = [restriction[0] for restriction in cur.fetchall()]
        
        cur.close()

        return participants

    def get_participant_email_matches(self, group_id):
        """Get all emails for participants in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT participant_name, participant_email, recipient_id FROM app.participant WHERE group_id=%s;", (group_id,))
        participants = cur.fetchall()

        participants_output = []
        for participant_name, participant_email, recipient_id in participants:
            cur.execute("SELECT participant_name FROM app.participant WHERE group_id=%s AND participant_id=%s LIMIT 1;", (group_id, recipient_id))

            recipient_name = cur.fetchone()[0]
            participants_output.append(((participant_name, participant_email), recipient_name))

        cur.close()

        return participants_output

    def get_participant_matches(self, group_id, participants):
        """Gets the participants with their matches."""

        participant_output = []

        cur = self.conn.cursor()
        for participant in participants:
            cur.execute("SELECT recipient_id FROM app.participant WHERE group_id=%s AND participant_id=%s LIMIT 1;", (group_id, participant.participant_id))
            recipient_id = cur.fetchone()[0]
            
            cur.execute("SELECT participant_name FROM app.participant WHERE group_id=%s AND participant_id=%s;", (group_id, recipient_id))

            recipient_name = cur.fetchone()[0]
            participant_output.append((participant.name, recipient_name))
        
        cur.close()

        return participant_output

    def update_participant_matches(self, group_id, new_matches):
        """Updates the participants with new matches."""

        cur = self.conn.cursor()
        for participant, recipient in new_matches.items():
            cur.execute("UPDATE app.participant SET recipient_id=%s WHERE participant_id=(SELECT participant_id FROM app.participant WHERE participant_id=%s LIMIT 1);", (recipient.participant_id, participant.participant_id))
        
        self.conn.commit()
        cur.close()
