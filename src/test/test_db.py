import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)

with conn.cursor() as cursor:
    cursor.execute("SELECT current_database(), current_user;")

    result = cursor.fetchone()

    print(result)

conn.close()