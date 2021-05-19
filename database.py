import mysql.connector
import time
import os
from datetime import date
import numpy as np

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="vijay1234",
    database="testdb"
    )


def insert_user(username,email,age,sex):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO users (username, emailid, Age, Sex) VALUES (%(id)s, %(em)s, %(ag)s, %(sx)s)")
    details = {
        'id':username,
        'em':email,
        'ag':age,
        'sx':sex
        }

    try:
        cursor.execute(add_data,details)
        mydb.commit()
        return 1
    except:
        return 0

def search_user(user):
    cursor = mydb.cursor()
    cursor.execute("select * from users where username='{}'".format(user))
    result=cursor.fetchall()

    if(len(result)==0):
        return 0
    else:
        return 1

def get_data():
    today = date.today()
    cursor = mydb.cursor()
    cursor.execute("select * from problem")
    result=cursor.fetchall()
    prob_id = []
    image = []
    heading = []
    detail = []
    dates = []
    for res in result:
        prob_id.append(res[0])
        image.append(os.path.join('/static/files/',res[6]))
        heading.append(res[1][:30]+'...')
        detail.append(res[2][:100]+'...')
        dates.append("{}-{}-{}".format(res[8].day,res[8].month,res[8].year))
    return image,heading,detail,dates,prob_id

def get_sortdata(value):
    today = date.today()
    cursor = mydb.cursor()
    if int(value)==1:
        cursor.execute("select * from problem order by upload asc")
    if int(value)==2:
        cursor.execute("select * from problem order by upload desc")
    if int(value)==3:
        cursor.execute("select * from problem order by upvotes desc")
    if int(value)==4:
        cursor.execute("select * from problem order by upvotes asc")
    result=cursor.fetchall()
    prob_id = []
    image = []
    heading = []
    detail = []
    dates = []
    for res in result:
        prob_id.append(res[0])
        image.append(os.path.join('/static/files/',res[6]))
        heading.append(res[1][:30]+'...')
        detail.append(res[2][:100]+'...')
        dates.append("{}-{}-{}".format(res[8].day,res[8].month,res[8].year))
    return image,heading,detail,dates,prob_id

def recommendation(keyword):
    cursor = mydb.cursor()
    cursor.execute("select * from problem")
    result = cursor.fetchall()
    num_occurance = []
    for res in result:
        count = 0
        value = res[1] + ' ' + res[2] + ' ' + res[4]
        low_value = value.lower()
        count += value.count(keyword)
        count += low_value.count(keyword.lower())
        num_occurance.append(count)

    prob_id = []
    image = []
    heading = []
    detail = []
    dates = []
    occ = []
    for i,res in enumerate(result):
        if num_occurance[i]!=0:
            prob_id.append(res[0])
            image.append(os.path.join('/static/files/',res[6]))
            heading.append(res[1][:30]+'...')
            detail.append(res[2][:100]+'...')
            dates.append("{}-{}-{}".format(res[8].day,res[8].month,res[8].year))
            occ.append(num_occurance[i])

    prob_id = np.array(prob_id)
    image = np.array(image)
    heading = np.array(heading)
    detail = np.array(detail)
    dates = np.array(dates)
    occ = np.array(occ)

    inds = occ.argsort()[::-1]

    prob_id = list(prob_id[inds])
    image = list(image[inds])
    heading = list(heading[inds])
    detail = list(detail[inds])
    dates = list(dates[inds])
        
    return image,heading,detail,dates,prob_id

def get_headsum(prob):
    cursor = mydb.cursor()
    sql = "SELECT * FROM problem WHERE probid={}".format(prob)
    cursor.execute(sql)
    result=cursor.fetchall()
    for res in result:
        heading=res[1]
        detail=res[2]
    return heading,detail

def get_document(prob):
    cursor = mydb.cursor()
    sql = "SELECT * FROM pdf_upload WHERE probid={}".format(prob)
    cursor.execute(sql)
    result=cursor.fetchall()
    pdf_link = []
    names = []
    for res in result:
        pdf_link.append(res[2])
        names.append(res[2][:30]+'...')
    return pdf_link,names

def get_links(prob):
    cursor = mydb.cursor()
    sql = "SELECT * FROM links WHERE probid={}".format(prob)
    cursor.execute(sql)
    result=cursor.fetchall()
    link = []
    names = []
    for res in result:
        link.append(res[2])
        names.append(res[2][:30]+'...')
    return link,names

def get_contacts(prob):
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM contact_info WHERE probid={}".format(prob)
        cursor.execute(sql)
        result=cursor.fetchall()
        for res in result:
            contact = res[2]
        return contact
    except:
        return ''

def problemid_info(prob):
    cursor = mydb.cursor()
    sql = "SELECT * FROM problem WHERE probid={}".format(prob)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def image_probid(prob):
    image = []
    cursor = mydb.cursor()
    sql = "SELECT img_path FROM image_data WHERE probid={}".format(prob)
    cursor.execute(sql)
    result = cursor.fetchall()
    for res in result:
        image.append(res[0])
    return image


