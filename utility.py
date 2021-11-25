import psycopg2
import re
from datetime import datetime
import sys
import pytz

#check email format  
def validate_email_format(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

    if(re.search(regex,email) == None):   
        return -1

#create datetime object
def create_datetime_obj(time):
    #create datetime object without timezone
    datetime_obj_no_tz = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
    
    #add timezone
    timezone = pytz.timezone("UTC")
    date_obj = timezone.localize(datetime_obj_no_tz)

    return date_obj
    
    
#add a scan to the scans table in db
# returns -1 in case of an invalid email format
# or invalid datetime input 
# throws exception in case of error accessing db 
def add_scan(email,time,room_id):
    
    #Conect to DB
    conn = psycopg2.connect(database="ctdb", user = "postgres", password = "capstone rocks", host = "127.0.0.1", port = "5432")
    
    #cursor
    cur = conn.cursor()
    
    #sanitize scan info

    #validate email format
    if(validate_email_format(email) == -1):
        cur.close()
        conn.close()
        return -1
    
    #create datetime obj
    try:
        date_obj = create_datetime_obj(time)
    
    #invalid date format
    except:
        cur.close()
        conn.close()
        return -1
    

    #add scan info to scans table 
    cur.execute(f"INSERT INTO SCANS (SCAN_ID, PERSON_EMAIL,SCAN_TIME,ROOM_ID) \
            VALUES (DEFAULT,'{email}',TIMESTAMP '{date_obj}',{room_id})")
    
    #commit changes to db
    conn.commit()
    cur.close()
    conn.close()
    
    #success
    return 0

#Checks if a person with the specified email exists in the people table
def exists_in_people(email,cur):

    cur.execute(f"SELECT COUNT(*) FROM PEOPLE WHERE email = '{email}'")
    
    result = cur.fetchone()
    
    #person exists in people table
    if(result[0] != 0):
        return True
    #person doesn't exist in people table
    else:
        return False


# add person to people table
def add_person(first,last, id):
    
    #Conect to DB
    conn = psycopg2.connect(database="ctdb", user = "postgres", password = "capstone rocks", host = "127.0.0.1", port = "5432")
    
    #cursor
    cur = conn.cursor()

    #generate email
    email = first +last+ str(datetime.now().timestamp())+"@fake.com"
    
    #person exists in the people table
    if(exists_in_people(email,cur) == True):
        return -1

    name = first + " " + last
    
    #add person info to people table 
    cur.execute(f"INSERT INTO PEOPLE (EMAIL,NAME,ID) \
        VALUES ('{email}','{name}',{id})")
    
    #commit changes to db
    conn.commit()
    cur.close()
    conn.close()

    return 0

#retrieves info for person with email from db
#returns -1 if no match found 
def get_person(email):
    
     #Conect to DB
    conn = psycopg2.connect(database="ctdb", user = "postgres", password = "capstone rocks", host = "127.0.0.1", port = "5432")
    
    #cursor
    cur = conn.cursor()
    
    cur.execute(f"SELECT * FROM PEOPLE WHERE email = '{email}'")
    
    result = cur.fetchone()
    
    #person exists in people table
    if(result is not None):
        print(result)
    #person doesn't exist in people table
    else:
        print("person doesn't exist")
        cur.close()
        conn.close()
        return -1

#retrieves all users from people table 
def get_all_users():
    
     #Conect to DB
    conn = psycopg2.connect(database="ctdb", user = "postgres", password = "capstone rocks", host = "127.0.0.1", port = "5432")
    
    #cursor
    cur = conn.cursor()
    
    cur.execute(f"SELECT * FROM PEOPLE")
    
    result = cur.fetchall()
    
    #table is not empty
    if(result is not None):
        print(result)
    #table is empty
    else:
        print("Table is empty")
        cur.close()
        conn.close()
        return -1







if __name__ == "__main__":
    if(len(sys.argv) == 1):
        #if(add_scan(sys.argv[1],sys.argv[2],sys.argv[3]) == 0):
        #    print("success")
        #else:
        #    print("failed")
        #add_person(sys.argv[1],sys.argv[2],sys.argv[3])
        #get_person(sys.argv[1])
        get_all_users()
    
        

