# set up database
from dotenv import load_dotenv
import os

load_dotenv()

import psycopg2
from app.database import Database
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
db = Database(conn, "app/schema.sql")

from app.app import app