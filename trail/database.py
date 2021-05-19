import mysql.connector
import time
from datetime import date

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="vijay1234",
    database="testdb"
    )


def insert_user(probhead,problem,userid,username,upvotes,image,categ,date):
    #today = date.today()
    cursor = mydb.cursor()
    add_data = ("INSERT INTO problem (probhead,problem,userid,username,upvotes,image,categ,upload) VALUES (%(head)s,%(prob)s,%(us)s,%(user)s,%(up)s,%(img)s,%(categ)s,%(dob)s)")
    details = {
        'head':probhead,
        'prob':problem,
        'us':int(userid),
        'user':username,
        'up':int(upvotes),
        'img':image,
        'categ':categ,
        #'dob':today.strftime("%y-%m-%d")
        'dob':date
        }

    try:
        cursor.execute(add_data,details)
        mydb.commit()
        return 1
    except:
        return 0

def insert_image(probid,image):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO image_data (probid,img_path) VALUES (%(pid)s,%(img)s)")
    details = {
        'pid':probid,
        'img':image
        }
    cursor.execute(add_data,details)
    mydb.commit()

def insert_pdf(probid,pdf):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO pdf_upload (probid,pdf) VALUES (%(pid)s,%(p)s)")
    details = {
        'pid':probid,
        'p':pdf
        }
    cursor.execute(add_data,details)
    mydb.commit()

def insert_link(probid,link):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO links (probid,link) VALUES (%(pid)s,%(l)s)")
    details = {
        'pid':probid,
        'l':link
        }
    cursor.execute(add_data,details)
    mydb.commit()

def insert_contact(probid,contact):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO contact_info (probid,contact) VALUES (%(pid)s,%(con)s)")
    details = {
        'pid':probid,
        'con':contact
        }
    cursor.execute(add_data,details)
    mydb.commit()





