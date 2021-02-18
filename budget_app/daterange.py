from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import SubmitField



class GetDateRange(FlaskForm):
    startdate = DateField('startdate',format='%Y-%m-%d')
    enddate = DateField('enddate',format='%Y-%m-%d')
    submit = SubmitField('Enter Dates')  