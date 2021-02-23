import os
import secrets
from flask import render_template, request, redirect, url_for, flash, session, abort
from budget_app import app, db, bcrypt
from budget_app.forms import RegistrationForm, LoginForm, ExpenseForm, UpdateExpenseForm, GetDateRange
from budget_app.models import User, Expense 
from flask_login import login_user, current_user, logout_user, login_required
from oauthlib.oauth2 import WebApplicationClient
from flask_dance.contrib.github import make_github_blueprint, github
import datetime


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

@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():

    expenseData = Expense.query.filter_by(user_id = session["user_id"])
    print(expenseData)
    totalSpend = []
    form = GetDateRange()
    
    flag = False

    if form.validate_on_submit():
        startdate = form.startdate.data.strftime('%Y-%m-%d')
        enddate = form.enddate.data.strftime('%Y-%m-%d')
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')

        if enddate < startdate:
            flash ('End date should be after start date.', 'danger')
            return redirect(url_for('start'))
        
        flag = True


    current_date = datetime.date.today()
    current_month = current_date.month
    current_year = current_date.year
    spend_this_month = 0
    spend_this_year = 0
    spend = 0
    for cost in expenseData:
        i = cost.cost
        totalSpend.append(i)
        year = (cost.date_posted.year)  
        month = (cost.date_posted.month)

        if flag:

            if startdate <= cost.date_posted <= enddate:
                spend += cost.cost
                

        if year == current_year:
            spend_this_year += cost.cost
            if month == current_month:
                spend_this_month += cost.cost

    
        
        
    totalSpend = sum(totalSpend)
    headings = ("Expense", "Expense Type", "Cost", "Date Posted", "Delete")
    expenses = Expense.query.filter_by(user_id = session["user_id"])
  
    return render_template('start.html', expenseData=expenseData, totalSpend=totalSpend, expenses=expenses, headings=headings, form=form, spend_this_month=spend_this_month, spend_this_year=spend_this_year, spend=spend)



@app.route("/expense/new", methods=['GET', 'POST'])
@login_required
def new_expense():
    user = User.query.get_or_404(current_user.id)
    form = ExpenseForm()
      
    if form.validate_on_submit():
        dateposted = form.date.data.strftime('%Y-%m-%d')
        dateposted = datetime.datetime.strptime(dateposted, '%Y-%m-%d')
        expense = Expense(vendor=form.expense.data, expense_type=form.expense_type.data, cost=form.cost.data, date_posted=dateposted, user_id=session["user_id"])
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
    print(current_user.id)
    print(expense.user.id)
    if current_user.id != expense.user.id:
        abort(403)

    form = UpdateExpenseForm()
    if form.validate_on_submit():
        dateposted = form.date.data.strftime('%Y-%m-%d')
        dateposted = datetime.datetime.strptime(dateposted, '%Y-%m-%d')
       
        expense.vendor = form.expense.data
        expense.expense_type = form.expense_type.data
        expense.cost = form.cost.data 
        expense.date_posted = dateposted
        expense.user_id = session["user_id"]
        user.total_cost += expense.cost
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

@app.route("/expense/delete/<int:expense_id>", methods=['GET', 'DELETE'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expenses = Expense.query.filter_by(user_id = session["user_id"])
    try:
        db.session.delete(expense)
        db.session.commit()
        flash ('Your expense has been deleted.')
        return redirect(url_for('start'))

    except:
        return 'There was an error deleting that expense.'
        


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
