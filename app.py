import os 
from flask import Flask, redirect, render_template, url_for, request
from dotenv import load_dotenv
import pymongo
import flask_login  #for handling logins/logouts
from passlib.hash import pbkdf2_sha256  #for encrypting pw

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
secret_key = os.environ.get('secret_key')

client = pymongo.MongoClient(MONGO_URI)

# create login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# create user
class User(flask_login.UserMixin):
    pass

# encrypt user's password
def password_encryptor(user_password):
    return pbkdf2_sha256.hash(user_password)

# verify user's password
def verify_password(user_input, encrypted_password):
    return pbkdf2_sha256.verify(user_input, encrypted_password)









@app.route('/')
def index():
    return render_template('index.template.html')


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


