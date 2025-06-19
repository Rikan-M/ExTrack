from flask import Blueprint,render_template,request,redirect,flash,session,url_for
from app import db
from app.models.models import Users,Feedback
from functools import wraps
import re
auth_bp=Blueprint("auth",__name__)

def login_user(user):
    session["username"]=user.username
    session["user_id"]=user.id
    session["loged_in"]=True


def input_validator(username,email,password):
    def validate_username(username):
        if not username:
            return (False, "Username cannot be empty")
        if len(username) < 4 or len(username) > 20:
            return (False, "Username must be 4-20 characters long")
        if not username[0].isalpha():
            return (False, "Username must start with a letter")
        if not re.fullmatch(r'^[A-Za-z0-9_]+$', username):
            return (False, "Username can only contain letters, numbers and underscores")
        if '__' in username:
            return (False, "Username cannot contain consecutive underscores")
        if username.endswith('_'):
            return (False, "Username cannot end with underscore")
        return (True,)


    def validate_email(email):
        if not email:
            return (False, "Email cannot be empty")
        if len(email) > 254:
            return (False, "Email is too long (max 254 chars)")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.fullmatch(pattern, email):
            return (False, "Please enter a valid email address")
        parts = email.split('@')
        if len(parts) != 2:
            return (False, "Email must contain exactly one @")
        
        local_part = parts[0]
        domain_part = parts[1]
        if len(local_part) > 64:
            return (False, "Email local part is too long (max 64 chars)")
        if local_part.startswith('.') or local_part.endswith('.'):
            return (False, "Email local part cannot start or end with dot")
        if '..' in local_part:
            return (False, "Email local part cannot contain consecutive dots")
        if '.' not in domain_part:
            return (False, "Domain must contain a dot")
        if domain_part.startswith('-') or domain_part.endswith('-'):
            return (False, "Domain cannot start or end with hyphen")
        if '..' in domain_part:
            return (False, "Domain cannot contain consecutive dots")
        return (True,)
    

    def validate_password(password):
        if not password:
            return (False,"Password cannot be empty")
        if len(password) < 8:
            return (False,"Password is too short (minimum 8 characters) ")
        if len(password)>12:
            return (False,"Password is too long (maximum 12 characters) ")
        if not re.search(r"[A-Z]", password):
            return (False,"Password must contain a uppercase character")
        if not re.search(r"[a-z]", password):
            return (False,"Password must contain a lowercase character")
        if not re.search(r"[0-9]", password):
            return (False,"Password must contain a digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return (False,"Password must contain a special character")
        return (True,)
    
    return [validate_username(username),validate_email(email),validate_password(password)]



def logout_user():
    session.clear()

def get_current_user():
    if 'user_id' in session and session.get("loged_in"):
        return Users.query.filter_by(id=session["user_id"])
    return None

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'user_id' not in session or not session["loged_in"]:
            flash('Please log in to access this page','info')
            return redirect(url_for('auth.login'))
        return func(*args,**kwargs)
    return wrapper


@auth_bp.route("/login",methods=["POST","GET"])
def login():
    logout_user()
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        user=Users.query.filter_by(email=email).first()
        if user and user.username==username and user.check_password(password):
                login_user(user=user)
                flash(f"Welcome {username} !You have successfully loged in","success")
                return redirect(url_for("cont.dashboard"))
        flash('Invalid credentials','error')
    return render_template("login.html")

@auth_bp.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        user=Users.query.filter_by(email=email).first()
        if user:
            flash("This email address already exists try another email","error")
        else:
            inp_validity=input_validator(username=username,email=email,password=password)
            for valid in inp_validity:
                if not valid[0]:
                    flash(valid[1],"error")
                    return redirect(url_for("auth.register"))
            
            new_user=Users(username=username,email=email)
            new_user.set_password(password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.success"))

    return render_template("register.html")

@auth_bp.route("/success")
def success():
    logout_user()
    return render_template("success.html")

@auth_bp.route("/feedback",methods=["POST"])
def feedback():
    got_user=True
    username=session.get("username")
    feedback=request.form.get('feedback')
    star=request.form.get('star')
    try:
        star=int(star)
    except:
        pass
    if not username:
        username="Unknown User"
        got_user=False
    
    if username and feedback:
        new_feedback=Feedback(username=username,feedback=feedback,star=star)
        db.session.add(new_feedback)
        db.session.commit()
        if got_user:
            flash(f"Thanks {username} for your feedback","success")
        else:
            flash("Thanks Sir for your feedback","success")
        
        return redirect(url_for("cont.dashboard"))
    
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully loged out","info")
    return redirect(url_for("auth.login"))
           
    


    

