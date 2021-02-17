from budget_app import app
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
if __name__ == '__main__':
    app.run(debug=True)