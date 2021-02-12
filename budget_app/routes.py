import os
import secrets
from flask import render_template, request, redirect, url_for, flash, session 
from budget_app import app, db, bcrypt
from budget_app.forms import RegistrationForm, LoginForm, ExpenseForm, UpdateExpenseForm
from budget_app.models import User, Expense 
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():

    return render_template('index.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            session["user_id"] = user.id
            return redirect(next_page) if next_page else redirect(url_for('start'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/start')
@login_required
def start():
    expenseData = Expense.query.filter_by(user_id = session["user_id"])
    totalSpend = []
    for cost in expenseData:
        i = cost.cost
        totalSpend.append(i)
    totalSpend = sum(totalSpend)
    headings = ("Expense", "Expense Type", "Cost", "Date Posted", "Total Cost")
    expenses = Expense.query.filter_by(user_id = session["user_id"])

    return render_template('start.html', expenseData=expenseData, totalSpend=totalSpend, expenses=expenses, headings=headings)



@app.route("/expense/new", methods=['GET', 'POST'])
@login_required
def new_expense():
    user = User.query.get_or_404(current_user.id)
    form = ExpenseForm()
    if form.validate_on_submit():

        expense = Expense(vendor=form.expense.data, expense_type=form.expense_type.data, cost=form.cost.data, date_posted=form.date.data, user_id=session["user_id"])
        db.session.add(expense)
        user.total_cost += form.cost.data
        db.session.commit()
        

        flash('Expense successfully submitted.', 'success')
        return redirect(url_for('start'))
    return render_template('new_expense.html', title='New Expense', form=form)

    
@app.route("/expense/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def expense(expense_id):
    user = User.query.get_or_404(current_user.id)
    expense = Expense.query.get_or_404(expense_id)
    form = UpdateExpenseForm()
    if form.validate_on_submit():
       
        expense.vendor = form.expense.data
        expense.expense_type = form.expense.data
        expense.cost = form.cost.data 
        expense.date_posted = form.date.data 
        expense.user_id = session["user_id"]
        user.total_cost += expense.cost
        print(user.total_cost)
        db.session.commit()
        flash('Expense successfully updated.', 'success')
    

        return redirect(url_for('start'))
    
    elif request.method == "GET":
        form.expense.data = expense.vendor  
        form.expense.data = expense.expense_type 
        form.cost.data  = expense.cost 
        form.date.data  = expense.date_posted 
        session["user_id"] = expense.user_id  
        
    return render_template('expense.html', title='Expense', expense=expense, form=form)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))