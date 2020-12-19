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

    def add_group(self, group_title):
        """Inserts a group and returns its ID."""

        cur = self.conn.cursor()
        cur.execute("INSERT INTO app.group (group_title) VALUES (%s) RETURNING group_id;", (group_title,))
        group_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        return group_id

    def add_group_to_users(self, group_id, user_ids):
        """Adds a group to users."""

        cur = self.conn.cursor()
        for user_id in user_ids:
            cur.execute("SELECT EXISTS(SELECT 1 FROM app.user WHERE user_id=%s)", (user_id,))
            
            result = cur.fetchone()[0]
            print(result)
            if result:
                cur.execute("INSERT INTO app.user_group (user_id, group_id) VALUES (%s, %s)", (user_id, group_id))

        self.conn.commit()
        cur.close()

        print(self.get_all_user_group_matches())

    def add_participants(self, group_id, participants, matches):
        """Insert participants under a group_id."""

        cur = self.conn.cursor()
        for participant in participants:

            if participant.email == None:
                participant.email = "NULL"

            cur.execute("INSERT INTO app.participant (group_id, participant_id, participant_name, participant_email, recipient_id) VALUES (%s, %s, %s, %s, %s)", (group_id, participant.participant_id, participant.name, participant.email, matches[participant].participant_id))

            for restriction in participant.restrictions:
                cur.execute("INSERT INTO app.participant_restriction (group_id, participant_id, restriction) VALUES (%s, %s, %s)", (group_id, participant.participant_id, restriction))

        self.conn.commit()
        cur.close()

    def add_user(self, user_email):
        """Inserts a user."""

        cur = self.conn.cursor()
        cur.execute("INSERT INTO app.user (user_email) VALUES (%s) RETURNING user_id;", (user_email,))
        user_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        
        return user_id

    def get_all_users(self):
        """Gets a list of all the users."""
        
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM app.user")
        users = cur.fetchall()
        cur.close()

        return users
    
    def get_all_user_group_matches(self):
        """Gets a list of all the group and user pairings."""

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM app.user_group")
        user_groups = cur.fetchall()
        cur.close()

        return user_groups
    
    def get_group(self, group_id):
        """Get data on a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT group_title FROM app.group WHERE group_id=%s LIMIT 1", (group_id,))
        group = cur.fetchone()
        cur.close()

        return group

    def get_user_ids(self, group_id):
        """Get all users in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT user_id FROM app.user_group WHERE group_id=%s", (group_id,))
        users = cur.fetchall()
        cur.close()

        return users

    def get_user_emails(self, group_id):
        """Get all emails for users in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT user_email FROM app.user INNER JOIN app.user_group ON app.user_group.group_id=%s", (group_id,))
        user_emails = cur.fetchall()

        cur.close()

        return user_emails

    def get_participants(self, group_id):
        """Get all participants in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT participant_id, participant_name FROM app.participant WHERE group_id=%s", (group_id,))

        participants = [Participant(*participant) for participant in cur.fetchall()]

        # get restrictions for each participant
        for participant in participants:
            cur.execute("SELECT restriction FROM app.participant_restriction WHERE group_id=%s AND participant_id=%s", (group_id, participant.participant_id))
            participant.restrictions = [restriction[0] for restriction in cur.fetchall()]
        
        cur.close()

        return participants

    def get_participant_email_matches(self, group_id):
        """Get all emails for participants in a group."""

        cur = self.conn.cursor()
        cur.execute("SELECT participant_name, participant_email, recipient_id FROM app.participant WHERE group_id=%s", (group_id,))
        participants = cur.fetchall()

        participants_output = []
        for participant_name, participant_email, recipient_id in participants:
            cur.execute("SELECT participant_name FROM app.participant WHERE group_id=%s AND participant_id=%s LIMIT 1", (group_id, recipient_id))

            recipient_name = cur.fetchone()[0]
            participants_output.append(((participant_name, participant_email), recipient_name))

        cur.close()

        return participants_output

    def get_participant_matches(self, group_id, participants):
        """Gets the participants with their matches."""

        participant_output = []

        cur = self.conn.cursor()
        for participant in participants:
            cur.execute("SELECT recipient_id FROM app.participant WHERE group_id=%s AND participant_id=%s LIMIT 1", (group_id, participant.participant_id))
            recipient_id = cur.fetchone()[0]
            
            cur.execute("SELECT participant_name FROM app.participant WHERE group_id=%s AND participant_id=%s", (group_id, recipient_id))

            recipient_name = cur.fetchone()[0]
            participant_output.append((participant.name, recipient_name))
        
        cur.close()

        return participant_output

    def update_participant_matches(self, group_id, new_matches):
        """Updates the participants with new matches."""

        cur = self.conn.cursor()
        for participant, recipient in new_matches.items():
            cur.execute("UPDATE app.participant SET recipient_id=%s WHERE participant_id=(SELECT participant_id FROM app.participant WHERE participant_id=%s LIMIT 1)", (recipient.participant_id, participant.participant_id))
        
        self.conn.commit()
        cur.close()
