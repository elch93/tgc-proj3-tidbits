import os
from flask import Flask, redirect, render_template, url_for, request, Markup
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import flask_login  # for handling logins/logouts
from passlib.hash import pbkdf2_sha256  # for encrypting password
from pprint import pprint

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

# find notes content in db


def search_by_topic(topic):
    results = client[dbname]['notes'].find({
        'topic': topic
    })

    results_array = []

    for i in results:
        results_array.append(i)

    # return markup of summernote code
    for i in results_array:
        i['content'] = Markup(i['content'])
    return results_array

# load user's notes


def load_user_notes(user):
    user_notes = client[dbname]['notes'].find({
        'owner': user
    })

    results_array = []

    for i in user_notes:
        results_array.append(i)

    # return markup of summernote code
    for i in results_array:
        i['content'] = Markup(i['content'])
    return results_array


# home page
@app.route('/', methods=["GET"])
def index():
    if flask_login.current_user.get_id():
        user_data = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        })
        user_notes = load_user_notes(flask_login.current_user.get_id())
        return render_template('index.template.html', username=user_data['displayname'], user_notes=user_notes)
    else:
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
                "password": password_encryptor(create_pw),
                'following': [],
                'liked': []
            })

            # then allow the user to login
            logged_in_user = User()
            user_data = client[dbname]['registered_users'].find_one({
                "email": create_email
            })

            logged_in_user.id = user_data['email']
            flask_login.login_user(logged_in_user)
            return render_template('index.template.html', username=user_data['displayname'])

        else:
            # if found, prevent creation
            myalert = create_email + ' is already in use. Please try again.'
            return render_template('index.template.html', myalert=myalert)

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
                user_notes = load_user_notes(flask_login.current_user.get_id())
                return render_template('index.template.html', username=user_data['displayname'], user_notes=user_notes)
            else:
                myalert = 'Password is wrong. Please try again.'
                return render_template('index.template.html', myalert=myalert)
        else:
            myalert = 'Email is wrong. Please try again.'
            return render_template('index.template.html', myalert=myalert)

    # create note
    if request.form.get('editordata'):
        created_subject = request.form.get('postedsubject')
        created_note = request.form.get('editordata')
        created_topic = request.form.get('subjecttopics')
        user_data = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        })

        client[dbname]['notes'].insert_one({
            'owner': user_data['email'],
            'displayname': user_data['displayname'],
            'subject': created_subject,
            'topic': created_topic,
            'content': created_note,
            'date': datetime.now().strftime('%y-%m-%d %a %H:%M'),
            'likes': 0
        })

        user_notes = load_user_notes(flask_login.current_user.get_id())
        return render_template('index.template.html', username=user_data['displayname'], user_notes=user_notes)

    # search for notes by topics
    if request.form.get('searchsubject'):
        topic_query = request.form.get('searchtopic')
        user_data = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        })

        results = search_by_topic(topic_query)
        user_notes = load_user_notes(flask_login.current_user.get_id())
        return render_template('index.template.html', username=user_data['displayname'], searchresults=results, user_notes=user_notes)

    # search for user's notes
    if request.form.get('searchmysubject'):
        user_data = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        })

        topic_query = request.form.get('searchmytopic')
        subj_query = request.form.get('searchmysubject')
        my_notes_query = client[dbname]['notes'].find({
            'owner': flask_login.current_user.get_id(),
            'topic': topic_query,
            'subject': subj_query
        })

        results_array = []

        for i in my_notes_query:
            results_array.append(i)

        # return markup of summernote code
        for i in results_array:
            i['content'] = Markup(i['content'])
        return render_template('index.template.html', username=user_data['displayname'], user_notes=results_array)



# logout
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))


# test route
@app.route('/test')
def test():
    print(results)
    return render_template('test.template.html', results=results)


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True
    )
