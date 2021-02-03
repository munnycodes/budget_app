from flask import render_template, request, redirect, url_for, flash
from budget_app import app, db, bcrypt
from budget_app.forms import RegistrationForm, LoginForm
from budget_app.models import User, Budget 

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

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
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)