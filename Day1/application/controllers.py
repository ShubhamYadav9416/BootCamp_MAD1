from flask import redirect, render_template, request
from flask import current_app as app
from .model import db,User

@app.route('/',methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        subject = "Modern Application Development1"
        users = User.query.all()
        return render_template("home.html", subject1 = subject,users = users)
    
    if request.method == "POST":
        name = request.form["text_submited"]
        new_user = User(user_name = name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")