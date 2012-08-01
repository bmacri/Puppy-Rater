import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from get_details import DogDetails
import settings

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = settings.secret_key
USERNAME = settings.username
PASSWORD = settings.password


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('DATABASE') as f:
            db.cursor().executescript(f.read())
        db.commit()

dog = DogDetails()

class DogFromDB():
    pass
    
@app.before_request
def before_request():
    g.db = connect_db()

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
            flash('You were logged in')
            return redirect(url_for('show_all_dogs'))
    return render_template('login.html', error=error)
    
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_all_dogs  '))


@app.route('/')
def show_comments():
    cur = g.db.execute('select text from comments order by id desc')
    comments = [dict(text=row[0]) for row in cur.fetchall()]
    return render_template('template.html', comments=comments)

@app.route('/add', methods=['POST'])
def add_comment():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into comments (text) values (?)',
                 [request.form['text']])
    g.db.commit()
    flash('Comment has been saved')
    return redirect(url_for('show_comments'))
    

@app.route('/dogs')
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
    return render_template('template.html', db_dogs=dog_info_list)
    
@app.teardown_request
def teardown_request(exception):
    g.db.close()
    

app.debug = True 

if __name__ == '__main__':
    app.run()   
