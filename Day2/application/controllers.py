from flask import redirect, render_template, request, flash
from flask import current_app as app
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt



from .model import db,User

#-------initiallize login manager--------------
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        email = request.form["email"]
        existing_email =  User.query.filter_by(user_mail = email).first()
        if existing_email:
            flash("email already registered")
            return redirect("/login")
        else:
            password = request.form["password"]
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(email = email, password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("You are now registered, Please Login")
            return redirect('/login')


@app.route("/login", methods =["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        password =  request.form["password"]
        user =  User.query.filter_by(user_mail = email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                flash("Wrong Password, Please Login")
                return redirect("/login")
        else:
            flash("You are not registered, Please register")
            return redirect("/register")



@app.route('/',methods = ["GET", "POST"])
@login_required
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