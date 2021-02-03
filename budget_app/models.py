from datetime import datetime
from budget_app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', {self.email}"

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(100), nullable=False)
    expense_type = db.Column(db.Text, nullable=False)
    balance_before = db.Column(db.Integer, nullable=False)
    balance_after = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def __repr__(self):
        return f"User('{self.username}', {self.email}"

# class Budget(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = 
#     start_date = 
#     end_date = 
#     start_balance =
#     current_balance = db.Column(db.Integer, nullable=False)
     

#     def __repr__(self):
#         return f"User('{self.username}', {self.email}"

# class Budget_Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(100), nullable=False)
#     budget_id = db.Column(db.Text, nullable=False)
#     amount = 
#     category = 
#     description = 
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

#     def __repr__(self):
#         return f"User('{self.username}', {self.email}"
