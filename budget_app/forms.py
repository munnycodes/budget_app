from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from budget_app.models import User, Expense


class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Password',
     validators=[DataRequired(), Length(min=8, max=30), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    expense = StringField('Expense', validators=[DataRequired()])
    expense_type = SelectField(u'Expense Type', choices=[('housing', 'Housing'), ('food', 'Food'), ('transport', 'Transportation'), ('bills', 'Bills'),('entertainment', 'Entertainment'),('investments', 'Investments'),('misc','Miscellaneous'), ('groceries', 'Groceries')], validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    date = DateField('Date of Expense (yy/mm/dd)', format='%y/%m/%d', validators=[DataRequired()])
    submit = SubmitField('Submit Expense')  

class UpdateExpenseForm(FlaskForm):
    expense = StringField('Expense', validators=[DataRequired()])
    expense_type = SelectField(u'Expense Type', choices=[('housing', 'Housing'), ('food', 'Food'), ('transport', 'Transportation'), ('bills', 'Bills'),('entertainment', 'Entertainment'),('investments', 'Investments'),('misc','Miscellaneous'), ('groceries', 'Groceries')], validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    date = DateField('Date of Expense (yy/mm/dd)', format='%y/%m/%d', validators=[DataRequired()])
    submit = SubmitField('Update Expense')  



