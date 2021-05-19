from flask import Flask, render_template, request
from flask import redirect, make_response,url_for
from werkzeug.utils import secure_filename
import os
from database import insert_user,insert_image
import database

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
    if(request.method=="POST"):
        file=request.files['file']
        problem=request.form.get('problem')
        detail=request.form.get('detail')
        userid=request.form.get('userid')
        username=request.form.get('username')
        upvotes=request.form.get('upvotes')
        category=request.form.get('categ')
        date = request.form.get('date_value')
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/', filename))
        filename = os.path.join('/static/files/', filename)
        insert_user(problem,detail,userid,username,upvotes,filename,category,date)
        return "successfully uploaded"
    return render_template("index.html")

@app.route("/upload",methods=["GET","POST"])        
def upload():
    if request.method=='POST':
        if 'files[]' not in request.files:
            return "no file"
        probid = request.form.get('problem')
        files = request.files.getlist('files[]')
        
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/', filename))
            insert_image(probid,os.path.join('/static/files/', filename))
        return "files submitted"
    return render_template("upload.html")

@app.route("/pdf_upload",methods=["GET","POST"])
def pdf_upload():
    if request.method=='POST':
        probid = request.form.get('probid')
        pdf = request.form.getlist('addmore[]')
        for p in pdf:
            database.insert_pdf(probid,p)
        return "form entered"
    return render_template("pdfupload.html")

@app.route("/link",methods=["GET","POST"])
def link():
    if request.method=='POST':
        probid = request.form.get('probid')
        links = request.form.getlist('addmore[]')
        for l in links:
            database.insert_link(probid,l)
        return "form entered"
    return render_template("link.html")

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=='POST':
        probid = request.form.get('problem')
        contact = request.form.get('contact')
        print([probid,contact])
        database.insert_contact(probid,contact)
        return "form entered"
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
