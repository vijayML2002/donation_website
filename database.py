import mysql.connector
import time
import os
from datetime import date
import numpy as np
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="vijay1234",
    database="testdb"
    )


def insert_user(username,email,age,sex,password,facebook,twitter,phone,prof,insta):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO users (username, emailid, age, sex,pass,facebook,twitter,phone,profession,instagram) VALUES (%(id)s, %(em)s, %(ag)s, %(sx)s, %(p)s, %(fc)s, %(tw)s, %(ph)s, %(pr)s, %(ins)s)")
    details = {
        'id':username,
        'em':email,
        'ag':age,
        'sx':sex,
        'p':password,
        'fc':facebook,
        'tw':twitter,
        'ph':phone,
        'pr':prof,
        'ins':insta
        }

    try:
        cursor.execute(add_data,details)
        mydb.commit()
        return 1
    except:
        return 0

def get_user(user):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE username='{}'".format(user))
    return cursor.fetchall()[0]

def insert_problem(probhead,problem,userid,username,upvotes,image,categ,date):
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

    cursor.execute(add_data,details)
    mydb.commit()

    sql = ("SELECT * FROM problem WHERE problem='{}'".format(problem))
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][0]

def incre_likes(probid):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM problem where probid='{}'".format(probid))
    result = int(cursor.fetchall()[0][5]) + 1

    sql = ("UPDATE problem SET upvotes='{}' WHERE probid='{}'".format(result,probid))
    cursor.execute(sql)
    mydb.commit()

def decre_likes(probid):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM problem where probid='{}'".format(probid))
    result = int(cursor.fetchall()[0][5]) - 1

    sql = ("UPDATE problem SET upvotes='{}' WHERE probid='{}'".format(result,probid))
    cursor.execute(sql)
    mydb.commit()    
    

def payentry(probid,username,comments,amount):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO payment (probid,amount,comts,username) VALUES (%(pid)s,%(am)s,%(com)s,%(user)s)")
    details = {
        'pid':probid,
        'am':amount,
        'com':comments,
        'user':username
        }
    cursor.execute(add_data,details)
    mydb.commit()
    updategoal(int(probid),int(amount))

def top_contributor(probid):
    cursor = mydb.cursor()
    sql = ("SELECT username,amount FROM payment WHERE probid='{}' ORDER BY amount DESC".format(probid))
    cursor.execute(sql)
    result = cursor.fetchall()

    index = []
    user = []
    amount = []

    for i,res in enumerate(result):
        index.append(i+1)
        user.append(res[0])
        amount.append(res[1])
    return index,user,amount

def goalinit(probid,goal):
    cursor = mydb.cursor()
    add_data = ("INSERT INTO goal (probid,amount,goal) VALUES (%(pid)s,%(am)s,%(go)s)")
    details = {
        'pid':probid,
        'am':0,
        'go':goal
        }
    cursor.execute(add_data,details)
    mydb.commit()

def updategoal(probid,amount):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM goal WHERE probid='{}'".format(probid))
    result = cursor.fetchall()
    curr = amount + int(result[0][2])

    sql = ("UPDATE goal SET amount='{}' WHERE probid='{}'".format(curr,probid))
    cursor.execute(sql)
    mydb.commit()

def goalpercent(probid):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM goal WHERE probid='{}'".format(probid))
    result = cursor.fetchall()

    percent = int(result[0][2])/int(result[0][3])

    if(percent>=1):
        return 100,int(result[0][2]),int(result[0][3])
    
    return percent*100,int(result[0][2]),int(result[0][3])
        
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

def search_user(user,password):
    cursor = mydb.cursor()
    cursor.execute("select * from users where username='{}'".format(user))
    result=len(cursor.fetchall())

    if result==0:
        return 0

    cursor.execute("select * from users where username='{}' and pass='{}'".format(user,password))
    result=len(cursor.fetchall())

    if result!=0:
        return 1
    else:
        return -1

    
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
        cursor.execute("select * from old_to_new")
    if int(value)==2:
        cursor.execute("select * from new_to_old")
    if int(value)==3:
        cursor.execute("select * from high_upvotes")
    if int(value)==4:
        cursor.execute("select * from low_upvotes")
        
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

def insert_postlike(probid,user,flag):
    cursor = mydb.cursor()
    if flag==1:
        add_data = ("INSERT INTO like_post (probid,username) VALUES (%(pid)s,%(user)s)")
        details = {
            'pid':probid,
            'user':user
            }
        cursor.execute(add_data,details)
        incre_likes(probid)
    else:
        sql = ("DELETE FROM like_post WHERE probid='{}' AND username='{}'".format(probid,user))
        cursor.execute(sql)
        decre_likes(probid)
    mydb.commit()

def get_likedata(probid,user):
    cursor = mydb.cursor()
    sql = ("SELECT * FROM like_post WHERE probid='{}' AND username='{}'".format(probid,user))
    cursor.execute(sql)
    result = cursor.fetchall()
    return len(result)

def like_array(prob_arr,user):
    value=[]
    for p in prob_arr:
        value.append(get_likedata(p,user))
    return value

def profile_vector(gender):

    image = []

    if gender=='M':
        path = 'static/files/user/male'
    else:
        path = 'static/files/user/female'

    for file in os.listdir(path):
        image.append(path+'/'+file)

    return random.choice(image)

def upvote_user(user):
    try:
        cursor = mydb.cursor()
        sql = ("select sum(upvotes) from problem where username='{}'".format(user))
        cursor.execute(sql)
        result = cursor.fetchall()
        return int(result[0][0])
    except:
        return 0

def total_donation(user):
    cursor = mydb.cursor()
    sql = ("select * from ranking where username='{}'".format(user))
    cursor.execute(sql)
    result = cursor.fetchall()
    return int(result[0][1])

def get_rank(user):
    cursor = mydb.cursor()
    sql = ("select * from ranking")
    cursor.execute(sql)
    result = cursor.fetchall()

    for i,res in enumerate(result):
        if res[0]==user:
            return i+1

    return "not known"

def rank_list():
    cursor = mydb.cursor()
    sql = ("select * from ranking")
    cursor.execute(sql)
    result = cursor.fetchall()

    rank = []
    name = []
    amount = []

    for i,res in enumerate(result):
        rank.append(i+1)
        name.append(res[0])
        amount.append(int(res[1]))

    return rank,name,amount
