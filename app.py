import os
from flask import Flask, redirect, render_template, url_for, request
from dotenv import load_dotenv
import pymongo
import flask_login  # for handling logins/logouts
from passlib.hash import pbkdf2_sha256  # for encrypting password

# load env file
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
def user_loader(email):
    user_data = client["projtidbits"]['registered_users'].find_one({
        'email': email
    })

    logged_in_user = User()
    logged_in_user.id = user_data['email']
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
    return render_template('index.template.html')



# signup & login
@app.route('/', methods=["POST"])
def process_input():
    # user is trying to sign up
    if request.form.get('registeremail') and request.form.get('registerpw') and request.form.get('registername'):
        create_email, create_pw, create_dname = request.form.get(
            'registeremail'), request.form.get('registerpw'), request.form.get('registername')
        # first check if email already exists in database
        if not client[dbname]['registered_users'].find_one({
            "email": create_email
        }):
            # if not found, create an account
            client[dbname]['registered_users'].insert_one({
                "displayname": create_dname,
                "email": create_email,
                "password": password_encryptor(create_pw)
            })

            # then allow the user to login
            logged_in_user = User()
            user_data = client[dbname]['registered_users'].find_one({
                "email": create_email
            })

            logged_in_user.id = user_data['email']
            flask_login.login_user(logged_in_user)
            return render_template('index.template.html', state="default")

        else:
            # if found, prevent creation
            myalert = create_email + ' is already in use. Please try again.'
            return render_template('index.template.html',myalert=myalert)

    # user is trying to login
    if request.form.get('loginemail') and request.form.get('loginpw'):
        login_email, login_pw = request.form.get(
            'loginemail'), request.form.get('loginpw')
        if client[dbname]['registered_users'].find_one({"email": login_email}):
            # email exists, check pw now
            user_data = client[dbname]['registered_users'].find_one(
                {"email": login_email})
            if verify_password(login_pw, user_data['password']):
                logged_in_user = User()
                logged_in_user.id = user_data['email']
                flask_login.login_user(logged_in_user)
                return render_template('index.template.html', state="default")
            else:
                return "USER FOUND BUT WRONG PASSWORD"
        else:
            return "USER NOT FOUND"

    # create note
    if request.form.get('editordata'):
        created_note = request.form.get('editordata')
        print(created_note)
        return "Work in progress"



# logout
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))



# test route
@app.route('/test')
def test():
    results = client.sample_proj3.studynotes.find()
    print(results)
    return render_template('test.template.html', results=results)



if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True
    )

