from flask import Flask

app = Flask(__name__)
# half a megabyte
app.config["MAX_CONTENT_LENGTH"] = 1024 * 512

from dotenv import load_dotenv
import os
import psycopg2
from app.database import Database

load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
db = Database(conn, "app/schema.sql")

from app import routes

"""import string
import random

for _ in range(10):
    email = ""
    iteration_count = random.randrange(15, 50)
    while iteration_count > 0:
        email += random.choice(string.ascii_lowercase)
        iteration_count -= 1;

    db.add_user(email)

print(db.get_all_users())"""
