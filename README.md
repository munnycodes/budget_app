# Munny Money
This is a basic expense tracking app called "Munny Money”. 

## Table of Contents
* [Features](#features)
* [Setup](#setup)
* [Files](#files)
* [Background](#background)


# Features
Users are able to:
* Register an account on the website
* Login using a password and email
* Create expenses and save them to a database
* View, update and delete existing expenses
* Choose two dates and display the total expenditure in that timeframe



For this project, ensure that you have `python3`, `pip3` and `virtualenv` library set up. 

# Setup
1. Clone this repo onto your local machine.
2. From the root directory, create a virtualenv with the command:
    `python3 -m venv <name of your env>`
3. Activate your virtual env by entering the following command:
    `source <env>/bin/activate`
3. Install requirements:
    `pip install -r requirements.txt`
4. Build and run the Flask app in VSCode

5. In your browser enter the following URL:
    `http://127.0.0.1:5000/`



# Files

**routes.py** contains the URLs and functions for each page used in the app.

**forms.py** contains all of the webforms used in this application (using WTForms).

**models.py** contains the database models used for the application.
There are two tables in the database: 
* User stores information about each user.
* Expense stores information related to each expense the user makes.
The primary key field in the User table, 'id', contains unique values. The foreign key field in the Expense table, 'User_id', allows multiple instances of the same value. A user can have many expenses whereas an expense can only have one user. 

# Background
I started working on this app in February 2021. I decided to make an expense tracker as a tool to help teach my nephew how to budget. 

In the future I would like to add the following:
* A sign in option using a user's Github and Google accounts.
* Add graphs and charts to display spending in different categories.
* Improve the design of the app. 
