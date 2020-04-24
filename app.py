import os 
from flask import Flask, redirect, render_template, url_for, request
from dotenv import load_dotenv
import pymongo
import flask_login  #for handling logins/logouts
from passlib.hash import pbkdf2_sha256  #for encrypting password

#load env file
load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('secret_key')

client = pymongo.MongoClient(MONGO_URI)
dbname = "projtidbits"

# create login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# create user
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(password):
    user_data = client.sample_proj3.users.find_one(
        {"password": password}
    )

    logged_in_user = User()
    logged_in_user.id = user_data["email"]
    return logged_in_user

# encrypt user's password
def password_encryptor(user_password):
    return pbkdf2_sha256.hash(user_password)

# verify user's password
def verify_password(user_input, encrypted_password):
    return pbkdf2_sha256.verify(user_input, encrypted_password)

# home page
@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.template.html')

# signup & login
@app.route('/', methods=["POST"])
def process_input():
    # user is trying to sign up
    if request.form.get('email') and request.form.get('password'):
        create_email, create_pw = request.form.get('email'), request.form.get('password')
        # first check if email already exists in database
        if not client[dbname]['registered_users'].find_one({
            "email": create_email
        }):
        # if not found, create an account
            client[dbname]['registered_users'].insert({
                "email": create_email,
                "password": password_encryptor(create_pw)
            })

            return "USER CREATED"
            
        else:
        # if found, prevent creation
            return "USER ALREADY EXISTS"
            

    # user is trying to login
    if request.form.get('registered_email') and request.form.get('registered_password'):
        login_email, login_pw = request.form.get('registered_email'), request.form.get('registered_password')
        if client[dbname]['registered_users'].find_one({"email": login_email}):
            # email exists, check pw now
            user_data = client[dbname]['registered_users'].find_one({"email": login_email})
            if verify_password(login_pw, user_data['password']):
            
                return "LOGIN SUCCESSFUL"
            else:
                return "USER FOUND BUT WRONG PASSWORD"
        else:
            return "USER NOT FOUND" 


# protected session
# @app.route("/protected")
# @flask_login.login_required
# def private_session():
#     return something

# logout
# flask_login.logout_user()
# return logged out

# testing
@app.route('/test')
def test():
    results = client.sample_proj3.studynotes.find()
    print(results)
    return render_template('test.template.html', results = results)















if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP'),
        port = os.environ.get('PORT'),
        debug = True
    )


