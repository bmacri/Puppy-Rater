from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from get_details import DogDetails
from contextlib import closing
import settings
import MySQLdb

DEBUG = True
SECRET_KEY = settings.secret_key
USERNAME = settings.username
PASSWORD = settings.password


app = Flask(__name__)
app.config.from_object(__name__)

dog = DogDetails()

class DogFromDB():
    pass
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('show_all_dogs'))
    return render_template('login.html', error=error)
    
    
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('login'))


@app.route('/')
def show_comments():
    comments = dog.get_comments()
    print comments
    return render_template('template.html', comments=comments)

@app.route('/add', methods=['POST'])
def add_comment():
    if not session.get('logged_in'):
        print "not logged in"
        abort(401)        
    if request.method == 'POST':
        ratings_dict = {}
        ratings_dict['spca_id,' (cuteness, personality, comments)] = spca_id, (request.form["Cuteness Rating"], request.form["Personality Rating"], request.form['text'] 
        
        dog.insert_comments(comments_dict)
        flash('Your comment has been saved')
    return redirect(url_for('show_comments'))
       

@app.route('/dogs', methods=['GET','POST'])
def show_all_dogs():
    dog_info_list = []
    all_db_data = dog.details_from_db()
    for each_dog in all_db_data:
        db_dog = DogFromDB()
        db_dog.name = each_dog[0]
        db_dog.spca_id = each_dog[1]
        db_dog.gender = each_dog[2]
        db_dog.breed = each_dog[3]
        db_dog.color = each_dog[4]
        db_dog.age = each_dog[5]
        db_dog.description = each_dog[6]
        db_dog.image = each_dog[7]
        dog_info_list.append(db_dog)
    #if dog.select_comments() !
    return render_template('template.html', db_dogs=dog_info_list)
  
@app.route('/test', methods=['POST'])
def test_func():
    return 
    

app.debug = True 

if __name__ == '__main__':
    app.run()   
