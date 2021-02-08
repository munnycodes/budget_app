import os
import secrets
from flask import render_template, request, redirect, url_for, flash, session 
from budget_app import app, db, bcrypt
from budget_app.forms import RegistrationForm, LoginForm, ExpenseForm
from budget_app.models import User, Expense 
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/start')
def start():
    headings = ("Expense", "Expense Type", "Cost", "Date Posted")
    expenses = Expense.query.all()
    print(expenses)
    return render_template('start.html', expenses=expenses, headings=headings)



@app.route('/posts', methods=['GET', 'POST'])
def posts():

#     if request.method == 'POST': 
#         budget_expense = request.form['expense']
#         budget_type = request.form['type']
#         budget_before = request.form['before']
#         budget_after = request.form['after']

#         new_budget = Budget(expense=budget_expense,budget_type=type, before=budget_before, after=budget_after)
#         db.session.add(new_post) 
#         db.session.commit() 
#         return redirect('/posts')
#     else:
#         all_posts = Budget.query.order_by(Budget.date_posted).all()
        return render_template('posts.html', posts=all_posts) 

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



@app.route("/expense/new", methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():

        expense = Expense(vendor=form.expense.data, expense_type=form.expense_type.data, cost=form.cost.data, date_posted=form.date.data, user_id=session["user_id"])
        db.session.add(expense)
        db.session.commit()
        session["expense_id"] = expense.id
        flash('Expense successfully submitted.', 'success')
        return redirect(url_for('start'))
    return render_template('new_expense.html', title='New Expense', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))