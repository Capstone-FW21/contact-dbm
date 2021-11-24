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
def add_scan(email,time,room_id):
    
    #Conect to DB
    try:
        conn = psycopg2.connect(database="ctdb", user = "postgres", password = "capstone rocks", host = "127.0.0.1", port = "5432")
    #error connecting to DB
    except:
        return -1
    
    #cursor
    cur = conn.cursor()
    
    #sanitize scan info

    #validate email format
    if(validate_email_format(email) == -1):
        print("invalid email")
        conn.close()
        return -1
    
    #create datetime obj
    try:
        date_obj = create_datetime_obj(time)
    
    #invalid date format
    except:
        print("invalid date")
        conn.close()
        return -1
    

    #add scan info to scans table 
    cur.execute(f"INSERT INTO SCANS (SCAN_ID, PERSON_EMAIL,SCAN_TIME,ROOM_ID) \
            VALUES (DEFAULT,'{email}',TIMESTAMP '{date_obj}',{room_id})")
    
    #commit changes to db
    conn.commit()
    conn.close()
    
    #success
    return 0

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        if(add_scan(sys.argv[1],sys.argv[2],sys.argv[3]) == 0):
            print("success")
        else:
            print("failed")
