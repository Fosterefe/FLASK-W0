from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import  LoginManager, current_user, login_required ,login_user, UserMixin, logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id= db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_post = db.relationship("POSTS", backref="user", lazy=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
    def __repr__(self):
        return f'Username: {self.username}, Posts: {self.user_post}'

class POSTS(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(1000))
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __init__(self, image, description, user_id):
        self.image = image
        self.description = description
        self.user_id = user_id

    """  def __repr__(self):
        return  f'{self.image}' """

class RegisterForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Log in")

class AddPostForm(FlaskForm):
    image = StringField(label="Image URL:", validators=[Length(min=50, max=1000), DataRequired()])
    description = StringField(label="Description:", validators=[DataRequired()])
    submit = SubmitField(label="Add Post")

class UpdatePostForm(FlaskForm):
    image = StringField(label="Image URL:",validators=[Length(min=50, max=1000), DataRequired()])
    description = StringField(label="Description:", validators=[DataRequired()])
    submit = SubmitField(label="Update")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def home():
    posts = POSTS.query.all()
    def getUser(id):
        users = User.query.all()
        for u in users:
            if u.id == id:
                return u.username

    return render_template("home.html", posts=posts, getUser=getUser)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        look_for_user = User.query.filter_by(username=form.username.data).first()
        if look_for_user:
            error = "That username has already been taken!"
            return render_template("register.html", form=form, error=error)
        else:
            user_to_create = User(username=form.username.data, email=form.password.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for("login"))
            
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.password.data).first()
        if user:
            session["user"] = user.username
            login_user(user)
            flash(f'Success! You are logged in as: {user.username}', category="success")
            return redirect(url_for("dashboard"))
        else:
            flash(f'The username or the password does not match. Try again!', category="danger")
            #return redirect(url_for("register"))

    return render_template("login.html", form=form)

@app.route("/dashboard", methods=["GET", "POST", "DELETE"])
@login_required
def dashboard():
    if "user" in session:
        posts = POSTS.query.filter_by(user_id=current_user.id)
        Addform = AddPostForm()
        id = current_user.id

        if Addform.validate_on_submit():
            new_post = POSTS(image=Addform.image.data, description=Addform.description.data, user_id=id)
            db.session.add(new_post)
            db.session.commit()
            flash("You added a post!", category="success")
            Addform.image.data = ""
            Addform.description.data = ""

        return render_template("dashboard.html", posts=posts, form=Addform ) 
    else:
        return redirect(url_for("login"))
 
@app.route("/delete_post/<int:id>", methods=["GET", "DELETE"])
@login_required
def delPost(id):
    d_post = POSTS.query.get(id)
    db.session.delete(d_post)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/dashboard/update_post/<int:id>", methods=["GET", "POST"])
@login_required 
def update_post(id):
    isUpdate = True
    posts = POSTS.query.filter_by(user_id=current_user.id)
    post = POSTS.query.filter_by(id=id).first()
    image = post.image
    descc = post.description
    Addform = AddPostForm()

    new_img = request.form.get("image")
    new_desc = request.form.get("desc")

    if request.method == "POST":
        post.image = new_img
        post.description = new_desc
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html",image=image, descc=descc, isUpdate=isUpdate, form = Addform, posts=posts)
   
@app.route('/logout')  
def logout_page():
    session.pop("user")
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))

@app.route("/delete_account", methods=["GET", "DELETE", "POST"])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/user/<uname>", methods=["GET"])
def user_profile(uname):
    user = User.query.filter_by(username=uname).first()
    posts = POSTS.query.filter_by(user_id=user.id)
    return render_template("user_profile.html", user=user, posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
 