import json

from MySQLdb.constants.FIELD_TYPE import JSON
from django.contrib.sites import requests
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from interact_with_DB import interact_db
from pages.assignment10.assignment10 import assignment10
import requests

app = Flask(__name__)
app.secret_key = "123"


def set_users():
    users_list = [{'first name': 'Yossi', 'last name': 'Cohen', 'email': 'yo@gmail.com'},
                  {'first name': 'Aharon', 'last name': 'Aharoni', 'email': 'ah@gmail.com'},
                  {'first name': 'Oren', 'last name': 'Hazanov', 'email': 'or@gmail.com'},
                  {'first name': 'Ahlan', 'last name': 'Dvori', 'email': 'ahdv@gmail.com'},
                  {'first name': 'Amihai', 'last name': 'Yossi', 'email': 'ah@gmail.com'}]
    return users_list


@app.route('/home_page', methods=['GET', 'POST'])
@app.route('/home')
@app.route('/')
def home_page():
    return render_template('cv.html')


@app.route('/assignment8', methods=['GET', 'POST'])
def details():
    return render_template('assignment8.html',
                           degrees='bsc',
                           hobbies=('playing soccer', 'playing guitar', 'swimming'),
                           visited_places=['costa rica', 'brazil', 'Peru', 'argentina', 'amsterdam'],
                           like_the_course=True)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('assignment9.html')


@app.route('/assignment9', methods=['GET', 'POST'])
def forms():
    if request.method == 'GET':
        if 'search_key' in request.args:
            search_key = request.args['search_key']
            users_list = set_users()
            matches = []
            if search_key:
                for user in users_list:
                    if user["first name"] == search_key or user["last name"] == search_key or user[
                        "email"] == search_key:
                        matches.append(user)
            else:
                matches = users_list
            if session.get('login'):
                return render_template('assignment9.html', matches_list=matches, nick_name=session.get('nick'))
            else:
                return render_template('assignment9.html', matches_list=matches)
        else:
            return render_template('assignment9.html')
    if request.method == 'POST':
        first = request.form['first']
        last = request.form['last']
        nickname = request.form['nickname']
        email = request.form['email']
        session['nickname'] = nickname
        session['login'] = True
    if session.get('login'):
        return render_template('assignment9.html', nick_name=session.get('nickname'))
    return render_template('assignment9.html')


# assignment10:

app.register_blueprint(assignment10)


#Assignment 11:

@app.route('/assignment11/users')
def json_users_func():
    query = "select * from users"
    users_query = interact_db(query=query, query_type='fetch')
    json_users = jsonify(users_query)
    return json_users

@app.route('/assignment11/outer_source',  methods=['GET', 'POST'])
def assignment11_outer_source():
    return render_template('assignment11_outsource.html')

@app.route('/req_frontend', methods=['POST'])
def req_frontend_func():
    user_id = request.form['id']
    return render_template('assignment11_outsource.html', id=user_id)

@app.route('/req_backend')
def req_backend_func():
    user=0
    if "user_id" in request.args and request.args['user_id']!='':
        user = request.args['user_id']
    res = requests.get(f'https://reqres.in/api/users/{user}')
    res = res.json()
    return render_template('assignment11_outsource.html', user = res)


#Assignment 12:

@app.route('/assignment12/restapi_users/<int:user_id>')
@app.route('/assignment12/restapi_users', defaults={'user_id': 2})
def json_user_by_id(user_id):
    query = 'select * from users where id=%s' % user_id
    users = interact_db(query=query, query_type='fetch')
    if len(users) == 0:
        dict_to_print = {
            'status': 'failed',
            'message': 'user not found'
        }
    else:
        dict_to_print = {
            f'id': users[0].id,
            'first name': users[0].first_name,
            'last name': users[0].last_name,
            'email': users[0].email
        }
    return jsonify(dict_to_print)



if __name__ == '__main__':
    app.run(debug=True)
