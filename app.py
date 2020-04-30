import os
from flask import Flask, redirect, render_template, url_for, request, Markup
from dotenv import load_dotenv
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
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
    logged_in_user.displayname = user_data['displayname']
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

            # check if displayname is taken
            if not client[dbname]['registered_users'].find_one({
                'displayname': create_dname
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
                logged_in_user.displayname = user_data['displayname']
                flask_login.login_user(logged_in_user)

                return redirect(url_for('search'))
            else:
                myalert = 'The display name ' + create_dname + \
                    ' is already in use. Please try again.'
                return render_template('index.template.html', myalert=myalert)

        else:
            # if found, prevent creation
            myalert = 'The email ' + create_email + ' is already in use. Please try again.'
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
                logged_in_user.displayname = user_data['displayname']
                flask_login.login_user(logged_in_user)

                return redirect(url_for('search'))
            else:
                myalert = 'Password is wrong. Please try again.'
                return render_template('index.template.html', myalert=myalert)
        else:
            myalert = 'Email is wrong. Please try again.'
            return render_template('index.template.html', myalert=myalert)

# create note page
@app.route('/create', methods=['GET', 'POST'])
@flask_login.login_required
def create():
    if request.method == 'GET':
        # display summernote api
        return render_template('create.template.html', username=flask_login.current_user.displayname)
    if request.method == 'POST':
        # create note
        created_subject = request.form.get('postedsubject')
        created_note = request.form.get('editordata')
        created_topic = request.form.get('subjecttopics')

        client[dbname]['notes'].insert_one({
            'owner': flask_login.current_user.get_id(),
            'displayname': flask_login.current_user.displayname,
            'subject': created_subject,
            'topic': created_topic,
            'content': created_note,
            'date': datetime.now().strftime('%y-%m-%d %a %H:%M'),
            'likes': 0
        })

        return redirect(url_for('mynotes'))


# search page
@app.route('/search', methods=['GET', 'POST'])
@flask_login.login_required
def search():
    if request.method == 'GET':
        # default load
        results = []
        default_result = client[dbname]['notes'].find().limit(5)
        for i in default_result:
            i['content'] = Markup(i['content'])
            results.append(i)
        return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens="Physics")
    if request.method == 'POST':
         # search for notes by topics
        subj_query = request.form.get('searchsubject')
        topic_query = request.form.get('searchtopic')
        



        results = search_by_topic(topic_query)
        return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens=subj_query, chosent=topic_query)


# mynotes page
@app.route('/mynotes', methods=['GET','POST'])
@flask_login.login_required
def mynotes():
    if request.method == 'GET':
        user_notes = load_user_notes(flask_login.current_user.get_id())
        return render_template('mynotes.template.html', user_notes=user_notes, username=flask_login.current_user.displayname,chosens="Physics")

    if request.method == 'POST':
        # search for user's notes
        topic_query = request.form.get('searchmytopic')
        print(topic_query)
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
        return render_template('mynotes.template.html', username=flask_login.current_user.displayname, user_notes=results_array,chosens=subj_query, chosent=topic_query)


# update page
@app.route('/update/<index>', methods=['GET','POST'])
@flask_login.login_required
def update(index):
    if request.method == 'GET':
        selected_note = client[dbname]['notes'].find_one({
            '_id' : ObjectId(index)
        })
        

        return render_template('update.template.html', username=flask_login.current_user.displayname, content=Markup(selected_note['content']) )

    if request.method == 'POST':
        # retrieve updated items
        updated_note = request.form.get('updatedata')
        updated_date = datetime.now().strftime('%y-%m-%d %a %H:%M')
        updated_subj = request.form.get('updatesubject')
        updated_topic = request.form.get('updatetopic')
        # update with pymongo
        client[dbname]['notes'].update_one(
            {'owner': flask_login.current_user.get_id(),
            'displayname': flask_login.current_user.displayname,
            '_id': ObjectId(index)
            },
            {'$set':{
            'subject': updated_subj,
            'topic': updated_topic,
            'content': updated_note,
            'date': updated_date,
            'likes': 0
        }})
        return redirect(url_for('mynotes'))

# delete note
@app.route('/delete/<index>', methods=["GET"])
@flask_login.login_required
def delete(index):
    if request.method == "GET":
        client[dbname]['notes'].delete_one(
            {'owner': flask_login.current_user.get_id(),
            'displayname': flask_login.current_user.displayname,
            '_id': ObjectId(index)
            })
        return redirect(url_for('mynotes'))

# like/save note
@app.route('/like/<index>', methods=["GET"])
@flask_login.login_required
def savenote(index):
    # check if note was saved before, if not, grant a like and save
    # else unsaved and minus one like
    # update likes
    if not client[dbname]['registered_users'].find_one({
        'email': flask_login.current_user.get_id(),
        'displayname': flask_login.current_user.displayname,
        'liked': ObjectId(index)
    }):
        selected_note = client[dbname]['notes'].find_one({
            '_id': ObjectId(index)
        }, {
            'likes':1,'_id':0
        })
        print(selected_note['likes'])
        updated_likes = selected_note['likes'] + 1
        client[dbname]['notes'].update_one({
            '_id': ObjectId(index)
        },{
            '$set':{
                'likes':updated_likes
            }
        } 
        
        )
        # save note to user's db
        client[dbname]['registered_users'].update_one({
            'email': flask_login.current_user.get_id(),
            'displayname': flask_login.current_user.displayname
        }, {
            '$push': {
                'liked': ObjectId(index)
            }
        })

        #return nothing but runs the function 
        return ('', 204)
    #unlike 
    else:
        # minus one like 
        selected_note = client[dbname]['notes'].find_one({
            '_id': ObjectId(index)
        }, {
            'likes':1,'_id':0
        })
        updated_likes = selected_note['likes'] - 1
        client[dbname]['notes'].update_one({
            '_id': ObjectId(index)
        },{
            '$set':{
                'likes':updated_likes
            }
        } 
        
        )
        # remove note
        client[dbname]['registered_users'].update_one({
            'email': flask_login.current_user.get_id(),
            'displayname': flask_login.current_user.displayname
        }, {
            '$pull': {
                'liked': ObjectId(index)
            }
        })

        return ('', 204)

# view saved notes
@app.route('/savednotes', methods=["GET","POST"])
@flask_login.login_required
def savednotes():
    if request.method=="GET":
        results = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        }, {
            'liked':1,
            '_id': 0
        })

        saved_notes = []

        for i in results['liked']:
            note = client[dbname]['notes'].find_one({
                '_id': i
            })

            saved_notes.append(note)
        
        print(saved_notes)

        for i in saved_notes:
            i['content'] = Markup(i['content'])

        
        

    return render_template('saved.template.html', username=flask_login.current_user.displayname, chosens = "Physics", user_notes = saved_notes)




# logout
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True
    )
