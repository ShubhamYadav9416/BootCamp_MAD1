from flask import redirect, render_template, request, flash, url_for
from flask import current_app as app
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os


from .model import db,User,Posts,PostComments,UserFollower

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route('/',methods = ["GET"])
@login_required
def home():
    if request.method == "GET":
        user_logined_id = current_user.user_id
        user = User.query.filter_by(user_id = user_logined_id).first()
        return render_template("home.html",user=user)

@app.route("/user_profile", methods= ["GET"])
@login_required
def user_profile():
    if request.method == "GET":
        user_logined_id = current_user.user_id
        user = User.query.filter_by(user_id = user_logined_id).first()
        posts = Posts.query.filter_by(user_id = user_logined_id).all()
        no_of_posts = Posts.query.filter_by(user_id = user_logined_id).count()

        no_of_following = UserFollower.query.filter_by(user_id = user_logined_id).count()
        no_of_follower = UserFollower.query.filter_by(follower_user_id = user_logined_id).count()

        return render_template("profile.html", user = user,posts = posts,no_of_posts=no_of_posts,
                               no_of_follower = no_of_follower, no_of_following=no_of_following)
    
@app.route("/edit_profle", methods = ["GET","POST"])
@login_required
def edit_profile():
    if request.method == "GET":
        user_logined_id = current_user.user_id
        user = User.query.filter_by(user_id = user_logined_id).first()
        return render_template("edit_profile.html", user=user)
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_bio = request.form["user_bio"]
        profile_pic = request.files["profile_pic"]
        profile_pic.save("static/IMG/" + profile_pic.filename)

        user_logined_id = current_user.user_id
        user = User.query.filter_by(user_id = user_logined_id).first()
        user.user_name = user_name
        user.user_bio = user_bio
        user.profile_img_path = "../static/IMG/" + profile_pic.filename
        db.session.commit()
        return redirect('/user_profile')



@app.route("/add_post", methods=["GET","POST"])
@login_required
def add_post():
    if request.method == "GET":
        return render_template("add_post.html")
    if request.method == "POST":
        post_img = request.files["post_img"]
        post_desc = request.form["post_desc"]
        user_logined_id = current_user.user_id
        post_img.save("static/IMG/Posts_Images/" + post_img.filename)
        new_post = Posts(user_id=user_logined_id, post_image_path= "../static/IMG/Posts_Images/" + post_img.filename, post_desc=post_desc)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/user_profile')
    
@app.route("/dlt_post/<int:post_id>")
@login_required
def dlt_post(post_id):
    post = Posts.query.filter_by(post_id=post_id).first()
    if post == None:
        flash("Post not exists")
        return redirect("/user_profile")
    os.remove(post.post_image_path[3:])
    db.session.delete(post)
    db.session.commit()
    return redirect("/user_profile")
    

@app.route("/updt_post/<int:post_id>", methods=["GET","POST"])
@login_required
def updt_post(post_id):
    post = Posts.query.filter_by(post_id=post_id).first()
    if post == None:
        flash("Post not exists")
        return redirect("/user_profile")
    if request.method == "GET":
        post = Posts.query.filter_by(post_id=post_id).first()
        return render_template("edit_post.html", post=post)
    if request.method == "POST":
        post_img = request.files["post_img"]
        if post_img:
            post_img.save("static/IMG/Posts_Images/" + post_img.filename)
            post.post_image_path = "../static/IMG/Posts_Images/" + post_img.filename
        post.post_desc = request.form["post_desc"]
        db.session.commit()
        return redirect("/user_profile")


@app.route("/user_post/<int:post_id>",methods=["GET","POST"])
@login_required
def user_post(post_id):
    user_logined_id = current_user.user_id
    post = Posts.query.filter_by(post_id=post_id).first()
    show_dlt_edit_buttons = False
    if post.user_id == user_logined_id:
        show_dlt_edit_buttons = True
    return render_template("user_post.html",post=post,show_dlt_edit_buttons=show_dlt_edit_buttons)

@app.route("/other_user/<int:others_user_id>", methods=["GET"])
@login_required
def other_user(others_user_id):
    if request.method == "GET":
        user_logined_id = current_user.user_id
        user = User.query.filter_by(user_id = user_logined_id).first()
        other_user = User.query.filter_by(user_id = others_user_id).first()
        other_user_posts = Posts.query.filter_by(user_id = others_user_id).all()
        other_user_no_of_posts = Posts.query.filter_by(user_id = others_user_id).count()
        following_details = UserFollower.query.filter_by(user_id = others_user_id).first()
        show_unfollow_button,show_follow_button = False, False
        if user_logined_id != others_user_id:
            if following_details:
                print("3")
                show_unfollow_button = True
            else:
                print("2")
                show_follow_button = True
        
        no_of_following = UserFollower.query.filter_by(user_id = others_user_id).count()
        no_of_follower = UserFollower.query.filter_by(follower_user_id = others_user_id).count()



        return render_template("profile.html",show_follow_button= show_follow_button,show_unfollow_button=show_unfollow_button ,
                               other_user = True, user_logined = user,user=other_user, posts = other_user_posts, 
                               no_of_posts = other_user_no_of_posts,no_of_following=no_of_following, no_of_follower=no_of_follower)
    

@app.route("/follow/<int:others_user_id>")
@login_required
def follow(others_user_id):
    user_logined_id = current_user.user_id
    follow = UserFollower(user_id = others_user_id, follower_user_id = user_logined_id)
    db.session.add(follow)
    db.session.commit()
    return redirect(url_for("other_user", others_user_id=others_user_id))

@app.route("/unfollow/<int:others_user_id>")
@login_required
def unfollow(others_user_id):
    user_logined_id  = current_user.user_id
    unfollow = UserFollower.query.filter_by(user_id = others_user_id).filter_by(follower_user_id= user_logined_id).first()
    print(unfollow)
    db.session.delete(unfollow)
    db.session.commit()
    # return redirect(url_for("other_user", others_user_id=others_user_id))
    return "hello"
