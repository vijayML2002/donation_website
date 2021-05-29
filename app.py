from flask import Flask, render_template, request
from flask import redirect, make_response,url_for
from flask import session
import secrets
from database import insert_user,search_user
from database import get_data,problemid_info
import database
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route("/main")
def main():
    if 'probid' in session:
        session.pop('probid',None)
    if 'username' not in session:
        return redirect(url_for('Login'))
    data,head,det,dates,prob_id = get_data()
    like_data = database.like_array(prob_id,session['username'])
    return render_template("main.html",length=len(data),head=head,data=data,
                           det=det,dates=dates,prob_id=prob_id,like_data=like_data)

@app.route("/main/problem/<problem_id>")
def problem(problem_id):
    if 'username' not in session:
        return redirect(url_for('Login'))
    session['probid'] = problem_id
    percent,amount,goal = database.goalpercent(problem_id)
    result = problemid_info(problem_id)
    posted = result[0][4]
    img = database.image_probid(problem_id)
    head,detail = database.get_headsum(problem_id)
    pdf,pdf_name = database.get_document(problem_id)
    link,link_name = database.get_links(problem_id)
    contact = database.get_contacts(problem_id)
    index,user,user_am = database.top_contributor(problem_id)
    return render_template("problem.html",data=result[0][1],
                           posted=posted,img=img,head=head,detail=detail,
                           pdf=pdf,pdf_name=pdf_name,pdf_len=len(pdf),
                           link=link,link_name=link_name,link_len=len(link),
                           contact=contact,percent=percent,amount=amount,goal=goal,
                           index=index,user=user,user_am=user_am,user_len=len(user))

@app.route("/main/problem/pay",methods=["GET","POST"])
def payment():
    if request.method=='POST':
        if 'username' not in session:
            return redirect(url_for('Login'))

        if 'probid' not in session:
            return redirect(url_for('main'))

        problem_id = session['probid']
        user = session['username']
        amount = request.form.get('amount')
        comment = request.form.get('comment')

        database.payentry(problem_id,user,comment,amount)
        
        return redirect(url_for("problem",problem_id=problem_id))

    return render_template("payment.html")

@app.route("/main/sort/<sort_id>")
def sort(sort_id):
    if 'probid' in session:
        session.pop('probid',None)
    if 'username' not in session:
        return redirect(url_for('Login'))
    data,head,det,dates,prob_id = database.get_sortdata(sort_id)
    like_data = database.like_array(prob_id,session['username'])
    return render_template("main.html",length=len(data),head=head,data=data,
                           det=det,dates=dates,prob_id=prob_id,like_data=like_data)


@app.route("/main/search",methods=["GET","POST"])
def search():
    if 'probid' in session:
        session.pop('probid',None)
    if 'username' not in session:
        return redirect(url_for('Login'))
    if request.method == "POST":
        keyword = request.form['keyvalue']
        data,head,det,dates,prob_id = database.recommendation(keyword)
        like_data = database.like_array(prob_id,session['username'])
        return render_template("main.html",length=len(data),head=head,data=data,
                               det=det,dates=dates,prob_id=prob_id,keyword=keyword,
                               keylen=len(data),like_data=like_data)
    return "sorry we can't find that"


@app.route("/", methods=["GET","POST"])
def Login():
    if request.method == "POST":
        name = request.form.get("user")
        password = request.form.get("pass")
        res = search_user(name,password)
        if res==1:
            session['username'] = request.form.get("user")
            return redirect(url_for('main'))
        elif res==0:
            return redirect(url_for('register'))
        else:
            return render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
def Logout():
    if 'username' not in session:
        return redirect(url_for('Login'))
    session.pop('username',None)
    return redirect(url_for('Login'))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user")
        email = request.form.get("email")
        age = request.form.get("age")
        sex = request.form.get("sex")
        facebook = request.form.get("face")
        twitter = request.form.get("twt")
        password = request.form.get("pass")
        instagram = request.form.get("inst")
        phone = request.form.get("phone")
        prof = request.form.get("prof")
        stat = insert_user(username,email,int(age),sex,password,facebook,twitter,phone,prof,instagram)
        if(stat):
            return redirect(url_for('Login'))
        else:
            return "Usernamme Already exist"
    return render_template("register.html")

@app.route("/api",methods=["GET","POST"])
def api():
     if request.method == 'POST':
        if 'username' in session:
            data = request.get_json()
            database.insert_postlike(int(data['probid']),session['username'],data['increment'])
        else:
            print("username not in session")
        return 'OK', 200

@app.route("/datafill",methods=["GET","POST"])
def datafill():
    if 'username' not in session:
        return redirect(url_for('Login'))
    
    try:
        session.pop('problem_id',None)
    except:
        pass
    
    if request.method=="POST":
        file=request.files['file']
        problem=request.form.get('problem')
        detail=request.form.get('detail')
        userid=request.form.get('userid')
        username=request.form.get('username')
        upvotes=request.form.get('upvotes')
        category=request.form.get('categ')
        goal=request.form.get('goal')
        date = request.form.get('date_value')
        contact = request.form.get('contact')
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/files', filename))
        filename = os.path.join('/static/files/', filename)
        session['problem_id'] = database.insert_problem(problem,detail,userid,username,upvotes,filename,category,date)
        database.insert_contact(session['problem_id'],contact)
        database.goalinit(int(session['problem_id']),int(goal))
        return redirect(url_for("image_upload"))
    return render_template("datafill.html")

@app.route("/datafill/data1",methods=["GET","POST"])
def image_upload():
    if 'username' not in session:
        return redirect(url_for('Login'))
    
    if request.method=="POST":
        if 'files[]' not in request.files:
            return "no file"
        probid = session['problem_id']
        files = request.files.getlist('files[]')
        
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/files/', filename))
            database.insert_image(probid,os.path.join('/static/files/', filename))
        return redirect(url_for("pdf_upload"))
    return render_template("image_upload.html")

@app.route("/datafill/data2",methods=["GET","POST"])
def pdf_upload():
    if 'username' not in session:
        return redirect(url_for('Login'))
    
    if request.method=="POST":
        probid = session['problem_id']
        pdf = request.form.getlist('addmore[]')
        for p in pdf:
            database.insert_pdf(probid,p)
        return redirect(url_for("link"))
    return render_template("pdf_upload.html")

@app.route("/datafill/data3",methods=["GET","POST"])
def link():
    if 'username' not in session:
        return redirect(url_for('Login'))
    
    if request.method=="POST":
        probid = session['problem_id']
        links = request.form.getlist('addmore[]')
        for l in links:
            database.insert_link(probid,l)
        session.pop('problem_id',None)
        return redirect(url_for("main"))
    return render_template("link.html")


@app.route("/profile",methods=["GET","POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for('Login'))

    detail = database.get_user(session['username'])
    upvote = database.upvote_user(session['username'])
    donation = database.total_donation(session['username'])
    rank = database.get_rank(session['username'])
    image = database.profile_vector(detail[4])
    return render_template("profile.html",detail=detail,image=image,
                           upvote=upvote,donation=donation,rank=rank)


@app.route("/rank",methods=["GET","POST"])
def rank():
    if 'username' not in session:
        return redirect(url_for('Login'))
    
    rank,name,amount = database.rank_list()
    
    return render_template("rank.html",rank=rank,name=name,
                           amount=amount,tab_len=len(rank))

if __name__ == "__main__":
    app.run(debug=True)
