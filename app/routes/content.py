from flask import Blueprint,render_template,request,redirect,flash,session,url_for
from app.models.models import Users,Category,Budget,Expanse
from functools import wraps
from app import db
from datetime import datetime,date,timedelta

cont_bp=Blueprint('cont',__name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'user_id' not in session or not session["loged_in"]:
            flash('Please log in to access our website','info')
            return redirect(url_for('auth.login'))
        return func(*args,**kwargs)
    return wrapper
def get_current_user():
    if 'user_id' in session and session.get("loged_in"):
        return Users.query.filter_by(id=session["user_id"])
    return None

def create_budget(category_id,amount,period):
    user_id=session.get("user_id")
    period=period.lower()
    today=date.today()
    start_date=today
    if period=="monthly":
        end_date=(today.replace(day=1)+timedelta(days=32))
        end_date=end_date.replace(day=1)-timedelta(days=1)
    elif period=="weekly":
        end_date=today+timedelta(days=7)
    else:
        end_date=today.replace(year=today.year+1)
    budget=Budget(amount=amount,period=period,start_date=start_date,end_date=end_date,user_id=user_id,category_id=category_id)
    db.session.add(budget)
    db.session.commit() 

def get_budget_status(category_id):
    user_id=session.get("user_id")
    today=date.today()
    budget=Budget.query.filter(
            Budget.user_id==user_id,
            Budget.category_id==category_id,
            Budget.start_date<=today,
            (Budget.end_date>=today) | (Budget.end_date==None)).first()
    if not budget:
        return None
    expenses=Expanse.query.filter(
        Expanse.user_id==user_id,
        Expanse.Category_id==category_id,
        Expanse.date>=budget.start_date,
        Expanse.date<=(budget.end_date if budget.end_date else today)
    ).all()
    total_spent=sum(expense.amount for expense in expenses )
    remaining=budget.amount-total_spent
    category=Category.query.filter_by(id=category_id).one()
    category_name=category.name
    remaining_days=budget.end_date-today
    if budget.amount > 0:
        percentage_used = min((total_spent / budget.amount) * 100, 100)
    else:
        percentage_used = 0

    is_active="active" if remaining>=0 else "deactive"
    return {
        'budget':budget,
        'category_name':category_name,
        'total_spent':total_spent,
        'remaining':remaining,
        'percentage_used':percentage_used,
        'period_start':budget.start_date,
        'period_end':budget.end_date,
        'remaining_days':remaining_days,
        "is_active":is_active
    }
@cont_bp.route("/")
@login_required
def dashboard():
   
    all_categories=Category.query.filter_by(user_id=session["user_id"]).all()
    return render_template("home.html",categories=all_categories)

@cont_bp.route("/budget")
@login_required
def budget():
    categories=Category.query.filter_by(user_id=session.get("user_id")).all()
    budgets=[]
    for category in categories:
        budToAdd=get_budget_status(category.id)
        if budToAdd:
            budgets.append(budToAdd)
    return render_template("budget.html",categories=categories,budgets=budgets)
@cont_bp.route("/help")
@login_required
def help():
    return render_template("help.html")

@cont_bp.route("/add_category",methods=["POST"])
@login_required
def add_category():
        name=request.form.get('category_name')
        description=request.form.get("description")
        exist_cate=Category.query.filter_by(user_id=session["user_id"],name=name).all()
        if exist_cate:
            flash("This Category already exists in your Categories list try another name","error")
            return redirect(url_for("cont.dashboard"))
        new_category=Category(name=name,description=description,user_id=session["user_id"])
        db.session.add(new_category)
        db.session.commit()
        flash("New category added","info")
        return redirect(url_for("cont.dashboard"))

@cont_bp.route("/category/<int:cate_id>")
@login_required
def go_to_category(cate_id):
    if not session.get("date"):
         session["date"]=datetime.date(datetime.today())
    category=Category.query.filter_by(id=cate_id).one()
    session["category"]=cate_id
    expanses=Expanse.query.filter_by(Category_id=cate_id,date=session["date"]).all()
    return render_template("category.html",category=category,expenses=expanses)

@cont_bp.route("/sort_date",methods=["POST"])
@login_required
def sort_date():
    date=request.form.get("date")
    session["date"]=date
    return redirect(url_for('cont.go_to_category',cate_id=session["category"]))

@cont_bp.route("/add_expanse",methods=["POST"])
@login_required
def add_expanse():
    amount=request.form.get('amount')
    title=request.form.get('title')
    pay_method=request.form.get('pay_method')
    location=request.form.get('location')
    receipt_filename=request.form.get('receipt_filename')
    category_id=request.form.get('category_id')
    new_expense=Expanse(amount=amount,title=title,payment_method=pay_method,location=location,
                        receipt_filename=receipt_filename,Category_id=category_id ,user_id=session.get("user_id"))
    db.session.add(new_expense)
    db.session.commit()
    flash(f"New Expanse amount {amount} added ","info")
    return redirect(url_for("cont.go_to_category",cate_id=category_id))

@cont_bp.route("/delete_exp/<int:exp_id>",methods=["POST"])
@login_required
def delete_exp(exp_id):
    expense=Expanse.query.get(exp_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("cont.go_to_category",cate_id=session.get("category")))

@cont_bp.route("/edit_exp/<int:exp_id>",methods=["GET","POST"])
@login_required
def edit_exp(exp_id):
    if request.method=="POST":
        expense=Expanse.query.get(exp_id)
        amount=request.form.get('amount')
        title=request.form.get('title')
        pay_method=request.form.get('pay_method') 
        location=request.form.get('location')
        receipt_filename=request.form.get('receipt_filename')  
        category_id=request.form.get('category_id')
        expense.category_id=category_id
        expense.payment_method=pay_method
        expense.date=date.today()
        if amount:
            expense.amount=amount
        if title :
            expense.title=title
        if location:
            expense.location=location
        if receipt_filename:
            expense.receipt_filename=receipt_filename
        db.session.commit()
        flash("Expanse Updated","info")
        return redirect(url_for("cont.go_to_category",cate_id=session.get("category")))
   
    categories=Category.query.filter_by(user_id=session.get("user_id"))
    return render_template("edit_expanses.html",categories=categories)



@cont_bp.route("/addBudget",methods=["POST"])
@login_required
def add_budget():
    amount=request.form.get("amount")
    period=request.form.get("period")
    category_id=request.form.get("category_id")
    create_budget(category_id=category_id,amount=amount,period=period)
    return redirect(url_for('cont.budget'))