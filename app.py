from flask import Flask, render_template, request
from flask import redirect, make_response,url_for
from flask import session
import secrets
from database import insert_user,search_user
from database import get_data,problemid_info
import database

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for("main"))
    return "You are not logged in !"

@app.route("/main")
def main():
#    if 'username' not in session:
#        return "You are not logged in !"
    data,head,det,dates,prob_id = get_data()
    return render_template("main.html",length=len(data),head=head,data=data,
                           det=det,dates=dates,prob_id=prob_id)

@app.route("/main/problem/<problem_id>")
def problem(problem_id):
#    if 'username' not in session:
#        return "You are not logged in !"
    result = problemid_info(problem_id)
    posted = result[0][4]
    img = database.image_probid(problem_id)
    head,detail = database.get_headsum(problem_id)
    pdf,pdf_name = database.get_document(problem_id)
    link,link_name = database.get_links(problem_id)
    contact = database.get_contacts(problem_id)
    return render_template("problem.html",data=result[0][1],
                           posted=posted,img=img,head=head,detail=detail,
                           pdf=pdf,pdf_name=pdf_name,pdf_len=len(pdf),
                           link=link,link_name=link_name,link_len=len(link),
                           contact=contact)

@app.route("/main/sort/<sort_id>")
def sort(sort_id):
#    if 'username' not in session:
#        return "You are not logged in !"
    data,head,det,dates,prob_id = database.get_sortdata(sort_id)
    return render_template("main.html",length=len(data),head=head,data=data,
                           det=det,dates=dates,prob_id=prob_id)


@app.route("/main/search",methods=["GET","POST"])
def search():
#    if 'username' not in session:
#        return "You are not logged in !"
    if request.method == "POST":
        keyword = request.form['keyvalue']
        data,head,det,dates,prob_id = database.recommendation(keyword)
        return render_template("main.html",length=len(data),head=head,data=data,
                               det=det,dates=dates,prob_id=prob_id,keyword=keyword,
                               keylen=len(data))
    return "sorry we can't find that"


@app.route("/login", methods=["GET","POST"])
def Login():
    if request.method == "POST":
        name = request.form.get("user")
        if(search_user(name)):
            session['username'] = request.form.get("user")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template("login.html")


@app.route("/logout")
def Logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user")
        email = request.form.get("email")
        age = request.form.get("age")
        sex = request.form.get("sex")
        stat = insert_user(username,email,int(age),sex)
        if(stat):
            return redirect(url_for('Login'))
        else:
            return "Usernamme Already exist"
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
