#admin utility
import psycopg2
import re
from datetime import datetime
import sys

#validate email address format
def validate_email_format(email: str):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    return re.search(regex, email) != None


#Retrieve people who were in contact with the person reporting a positive covid test
def retrieve_contacts(email:str):

    #validate email format
    validate_email_format(email)

    # Conect to DB
    conn = psycopg2.connect(
        database="ctdb",
        user="postgres",
        password="capstone rocks",
        host="127.0.0.1",
        port="5432",
    )

    # Cursor
    cur = conn.cursor()

    
