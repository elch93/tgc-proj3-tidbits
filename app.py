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
                    'followers': [],
                    'liked': [],
                    'joindate': datetime.now().strftime('%y-%m-%d %a %H:%M')
                })

                # then allow the user to login
                logged_in_user = User()
                user_data = client[dbname]['registered_users'].find_one({
                    "email": create_email
                })

                logged_in_user.id = user_data['email']
                logged_in_user.displayname = user_data['displayname']
                flask_login.login_user(logged_in_user)

                return redirect(url_for('profile', userid = logged_in_user.displayname))
            else:
                # if display name is used, prevent creation
                myalert = 'The display name "' + create_dname + \
                    '" is already in use. Please try again.'
                return render_template('index.template.html', myalert=myalert)

        else:
            # if found, prevent creation
            myalert = 'The email "' + create_email + \
                '" is already in use. Please try again.'
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

                return redirect(url_for('profile', userid = logged_in_user.displayname))
            else:
                myalert = 'Password is wrong. Please try again.'
                return render_template('index.template.html', myalert=myalert)
        else:
            myalert = 'Email is wrong. Please try again.'
            return render_template('index.template.html', myalert=myalert)
    else:
        return ('', 204)

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

# return array of user's liked notes


def liked_notes(userid):
    results = client[dbname]['registered_users'].find_one({
        'email': userid
    }, {
        'liked': 1,
        '_id': 0
    })
    return results['liked']


# find notes content in db
def search_by_topic(subject, topic):
    # if topic is specified, find notes under topic
    if topic != 'All':
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
    # if topic selected is 'all', find notes under subject
    elif topic == 'All':
        results = client[dbname]['notes'].find({
            'subject': subject
        })

        results_array = []

        for i in results:
            results_array.append(i)

        # return markup of summernote code
        for i in results_array:
            i['content'] = Markup(i['content'])
        return results_array


def search_all():
    raw_results = client[dbname]['notes'].find()
    results = list(raw_results)
    for i in results:
        i['content'] = Markup(i['content'])
    return results

# search/discover page
@app.route('/search', methods=['GET', 'POST'])
@flask_login.login_required
def search():
    if request.method == 'GET':
        # default load

        default_result = client[dbname]['notes'].find()

        sresults = list(default_result)
        for i in sresults:
            i['content'] = Markup(i['content'])

        user_liked_notes = liked_notes(flask_login.current_user.get_id())
        return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=sresults, chosens="All", user_liked_notes=user_liked_notes)

    if request.method == 'POST':
        # search for notes by topics wo keywords
        if not request.form.get('searchsubject') == 'All' and not request.form.get('customsearch'):
            subj_query = request.form.get('searchsubject')
            topic_query = request.form.get('searchtopic')

            results = search_by_topic(subj_query, topic_query)
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens=subj_query, chosent=topic_query, user_liked_notes=user_liked_notes)
        # view all notes without keywords
        elif request.form.get('searchsubject') == 'All' and not request.form.get('customsearch'):
            results = search_all()
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens='All', user_liked_notes=user_liked_notes)
        # search under all w keywords
        elif request.form.get('searchsubject') == 'All' and request.form.get('customsearch'):
            keyword_query = request.form.get('customsearch')

            custom_search = client[dbname]['notes'].find({
                'content': {'$regex': keyword_query,  '$options': 'i'}
            })

            results = []
            for i in custom_search:
                i['content'] = Markup(i['content'])
                results.append(i)
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens='All', user_liked_notes=user_liked_notes)
        # search under a subject & a topic with keywords
        elif not request.form.get('searchsubject') == 'All' and request.form.get('customsearch'):
            keyword_query = request.form.get('customsearch')
            subj_query = request.form.get('searchsubject')
            topic_query = request.form.get('searchtopic')

            if topic_query != 'All':
                custom_search = client[dbname]['notes'].find({
                    'topic': topic_query,
                    'content': {'$regex': keyword_query,  '$options': 'i'}
                })

            elif topic_query == 'All':
                custom_search = client[dbname]['notes'].find({
                    'subject': subj_query,
                    'content': {'$regex': keyword_query,  '$options': 'i'}
                })

            results = []
            for i in custom_search:
                i['content'] = Markup(i['content'])
                results.append(i)
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('search.template.html', username=flask_login.current_user.displayname, searchresults=results, chosens=subj_query, chosent=topic_query, user_liked_notes=user_liked_notes)

# mynotes page
@app.route('/mynotes', methods=['GET', 'POST'])
@flask_login.login_required
def mynotes():
    if request.method == 'GET':
        user_notes = load_user_notes(flask_login.current_user.get_id())
        return render_template('mynotes.template.html', searchresults=user_notes, username=flask_login.current_user.displayname, chosens="All")

    if request.method == 'POST':
        # search for user's notes by topic without keywords
        if not request.form.get('searchsubject') == "All" and not request.form.get('customsearch'):
            topic_query = request.form.get('searchtopic')
            subj_query = request.form.get('searchsubject')

            if topic_query != 'All':
                my_notes_query = client[dbname]['notes'].find({
                    'owner': flask_login.current_user.get_id(),
                    'topic': topic_query,
                    'subject': subj_query
                })

            elif topic_query == 'All':
                my_notes_query = client[dbname]['notes'].find({
                    'owner': flask_login.current_user.get_id(),
                    'subject': subj_query
                })

            results_array = []

            for i in my_notes_query:
                results_array.append(i)

            # return markup of summernote code
            for i in results_array:
                i['content'] = Markup(i['content'])
            return render_template('mynotes.template.html', username=flask_login.current_user.displayname, searchresults=results_array, chosens=subj_query, chosent=topic_query)

        # get all my notes
        elif request.form.get('searchsubject') == 'All' and not request.form.get('customsearch'):
            my_notes_query = client[dbname]['notes'].find({
                'owner': flask_login.current_user.get_id()
            })

            results_array = []

            for i in my_notes_query:
                results_array.append(i)

            # return markup of summernote code
            for i in results_array:
                i['content'] = Markup(i['content'])
            return render_template('mynotes.template.html', username=flask_login.current_user.displayname, searchresults=results_array, chosens='All')
        # get my notes by topic + custom query
        elif request.form.get('searchsubject') != 'All' and request.form.get('customsearch'):
            topic_query = request.form.get('searchtopic')
            subj_query = request.form.get('searchsubject')
            custom_query = request.form.get('customsearch')

            if topic_query != 'All':
                my_notes_query = client[dbname]['notes'].find({
                    'owner': flask_login.current_user.get_id(),
                    'topic': topic_query,
                    'subject': subj_query,
                    'content': {'$regex': custom_query, '$options': 'i'}
                })

            elif topic_query == 'All':
                my_notes_query = client[dbname]['notes'].find({
                    'owner': flask_login.current_user.get_id(),
                    'subject': subj_query,
                    'content': {'$regex': custom_query, '$options': 'i'}
                })

            results_array = []

            for i in my_notes_query:
                results_array.append(i)
            # return markup of summernote code
            for i in results_array:
                i['content'] = Markup(i['content'])
            return render_template('mynotes.template.html', username=flask_login.current_user.displayname, searchresults=results_array, chosens=subj_query, chosent=topic_query)

        # get all my notes + custom query
        elif request.form.get('searchsubject') == 'All' and request.form.get('customsearch'):
            custom_query = request.form.get('customsearch')
            my_notes_query = client[dbname]['notes'].find({
                'owner': flask_login.current_user.get_id(),
                'content': {'$regex': custom_query, '$options': 'i'}
            })

            results_array = []

            for i in my_notes_query:
                results_array.append(i)

            # return markup of summernote code
            for i in results_array:
                i['content'] = Markup(i['content'])
            return render_template('mynotes.template.html', username=flask_login.current_user.displayname, searchresults=results_array, chosens='All')


# update page
@app.route('/update/<index>', methods=['GET', 'POST'])
@flask_login.login_required
def update(index):
    if request.method == 'GET':
        selected_note = client[dbname]['notes'].find_one({
            '_id': ObjectId(index)
        })

        return render_template('update.template.html', username=flask_login.current_user.displayname, content=Markup(selected_note['content']))

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
            {'$set': {
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

# liking/saving a note
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
            'likes': 1, '_id': 0
        })
        print(selected_note['likes'])
        updated_likes = int(selected_note['likes']) + 1
        client[dbname]['notes'].update_one({
            '_id': ObjectId(index)
        }, {
            '$set': {
                'likes': updated_likes
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

        # return nothing but runs the function
        return ('', 204)
    # unlike
    else:
        # minus one like
        selected_note = client[dbname]['notes'].find_one({
            '_id': ObjectId(index)
        }, {
            'likes': 1, '_id': 0
        })
        updated_likes = int(selected_note['likes']) - 1
        client[dbname]['notes'].update_one({
            '_id': ObjectId(index)
        }, {
            '$set': {
                'likes': updated_likes
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
@app.route('/savednotes', methods=["GET", "POST"])
@flask_login.login_required
def savednotes():
    if request.method == "GET":
        results = client[dbname]['registered_users'].find_one({
            'email': flask_login.current_user.get_id()
        }, {
            'liked': 1,
            '_id': 0
        })

        saved_notes = []

        for i in results['liked']:
            note = client[dbname]['notes'].find_one({
                '_id': i
            })

            saved_notes.append(note)

        for i in saved_notes:
            i['content'] = Markup(i['content'])
        user_liked_notes = liked_notes(flask_login.current_user.get_id())
        return render_template('saved.template.html', username=flask_login.current_user.displayname, chosens="All", searchresults=saved_notes, user_liked_notes=user_liked_notes)
    if request.method == "POST":
        # search for user's liked notes by topic without keywords
        if not request.form.get('searchsubject') == 'All' and not request.form.get('customsearch'):
            topic_query = request.form.get('searchtopic')
            subj_query = request.form.get('searchsubject')
            # get array of objectids that user liked
            saved_notes_query = client[dbname]['registered_users'].find_one({
                'email': flask_login.current_user.get_id()
            }, {
                'liked': 1,
                '_id': 0
            })

            # filter out topics we don't need
            saved_notes = []

            for i in saved_notes_query['liked']:
                note = client[dbname]['notes'].find_one({
                    '_id': i
                })
                if topic_query != 'All':
                    if note['topic'] == topic_query:
                        saved_notes.append(note)
                elif topic_query == 'All':
                    if note['subject'] == subj_query:
                        saved_notes.append(note)

            if saved_notes:
                for i in saved_notes:
                    i['content'] = Markup(i['content'])
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('saved.template.html', username=flask_login.current_user.displayname, searchresults=saved_notes, chosens=subj_query, chosent=topic_query, user_liked_notes=user_liked_notes)

        # get all liked notes
        elif request.form.get('searchsubject') == 'All' and not request.form.get('customsearch'):
            saved_notes_query = client[dbname]['registered_users'].find_one({
                'email': flask_login.current_user.get_id()
            }, {
                'liked': 1,
                '_id': 0
            })

            saved_notes = []

            for i in saved_notes_query['liked']:
                note = client[dbname]['notes'].find_one({
                    '_id': i
                })
                saved_notes.append(note)

            if saved_notes:
                for i in saved_notes:
                    i['content'] = Markup(i['content'])
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('saved.template.html', username=flask_login.current_user.displayname, searchresults=saved_notes, chosens='All', user_liked_notes=user_liked_notes)

        # get liked notes by topic + custom query
        elif not request.form.get('searchsubject') == 'All' and request.form.get('customsearch'):
            topic_query = request.form.get('searchtopic')
            subj_query = request.form.get('searchsubject')
            custom_query = request.form.get('customsearch')

            saved_notes_query = client[dbname]['registered_users'].find_one({
                'email': flask_login.current_user.get_id()
            }, {
                'liked': 1,
                '_id': 0
            })

            # filter out topics we don't need
            saved_notes = []
            # compare to notes collection
            for i in saved_notes_query['liked']:
                note = client[dbname]['notes'].find_one({
                    '_id': i,
                    'content': {'$regex': custom_query, '$options': 'i'}
                })
                if note:
                    if topic_query != 'All':
                        if note['topic'] == topic_query:
                            saved_notes.append(note)
                    elif topic_query == 'All':
                        if note['subject'] == subj_query:
                            saved_notes.append(note)

            if saved_notes:
                for i in saved_notes:
                    i['content'] = Markup(i['content'])
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('saved.template.html', username=flask_login.current_user.displayname, searchresults=saved_notes, chosens=subj_query, chosent=topic_query, user_liked_notes=user_liked_notes)

        # return results from all and custom search
        elif request.form.get('searchsubject') == 'All' and request.form.get('customsearch'):
            custom_query = request.form.get('customsearch')

            saved_notes_query = client[dbname]['registered_users'].find_one({
                'email': flask_login.current_user.get_id()
            }, {
                'liked': 1,
                '_id': 0
            })

            # filter out topics we don't need
            saved_notes = []
            # compare to notes collection
            for i in saved_notes_query['liked']:
                note = client[dbname]['notes'].find_one({
                    '_id': i,
                    'content': {'$regex': custom_query, '$options': 'i'}
                })
                if note:
                    saved_notes.append(note)

            if saved_notes:
                for i in saved_notes:
                    i['content'] = Markup(i['content'])
            user_liked_notes = liked_notes(flask_login.current_user.get_id())
            return render_template('saved.template.html', username=flask_login.current_user.displayname, searchresults=saved_notes, chosens='All', user_liked_notes=user_liked_notes)

# profile page
@flask_login.login_required
@app.route('/profile/<userid>')
def profile(userid):
    userinfo = client[dbname]['registered_users'].find_one({
        'displayname': userid
    })
    userlikes = userinfo['liked']
    userfollowing = userinfo['following']
    userfollowers = userinfo['followers']

    usernotes = load_user_notes(dict(userinfo)['email'])
    user_notes = []
    likes_received = 0

    if usernotes:
        for i in usernotes:
            likes_received += i['likes']
            i['content'] = Markup(i['content'])
            user_notes.append(i)

    user_liked_notes = liked_notes(flask_login.current_user.get_id())

    return render_template('profile.template.html',user_liked_notes=user_liked_notes, searchresults=user_notes, username=flask_login.current_user.displayname, profilename=userid, followers = len(userfollowers), following = len(userfollowing), liked = len(userlikes), likes_received = likes_received)


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
