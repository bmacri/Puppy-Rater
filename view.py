from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from get_details import DogDetails
from contextlib import closing
import settings
import MySQLdb

DEBUG = True
SECRET_KEY = settings.secret_key
#USERNAME = settings.username
#PASSWORD = settings.password


app = Flask(__name__)
app.config.from_object(__name__)

dog = DogDetails()

class DogFromDB():
    pass
    
class User():
    pass 
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn, cursor = dog.mysql_get_cursor()
    cursor.execute ("SELECT * FROM users;")
    user_info = cursor.fetchall()  
    conn.commit()
    usernames = []
    passwords = []
    for user in user_info:
        User.username = user[1]
        User.password = user[2]
        usernames.append(User.username)
        passwords.append(User.password)  
    error = None 
    if request.method == 'POST':
        if request.form['username'] not in usernames:
            error = 'Invalid username'
        else:
            username_index = usernames.index(request.form['username'])
            if request.form['password'] != passwords[username_index]: 
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = request.form['username'] #session carries username information
                return redirect(url_for('show_all_dogs'))
    return render_template('login.html', error=error)
    
    
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_comment():
    if not session.get('logged_in'):
        print "not logged in"
        abort(401)        
    if request.method == 'POST':
        ratings_dict = {}
        ratings_dict['spca_id']  = request.form["spca_id"]
        ratings_dict['cuteness'] = request.form["Cuteness Rating"]
        ratings_dict['personality'] =  request.form["Personality Rating"]
        ratings_dict['comment'] = request.form['text']
        dog.insert_ratings_dict(ratings_dict)
        flash('Your comment has been saved')
    return redirect(url_for('show_all_dogs'))
       

@app.route('/dogs', methods=['GET','POST'])
def show_all_dogs():
    dog_info_list = dog.details_from_db()
    return render_template('template.html', db_dogs=dog_info_list)
  
@app.route('/test', methods=['POST'])
def test_func():
    return 
    

app.debug = True 

if __name__ == '__main__':
    app.run()   
