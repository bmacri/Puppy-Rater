from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from get_details import DogDetails

app = Flask(__name__)

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
            flash('You were logged in')
            return redirect(url_for('show_all_dogs'))
    return render_template('login.html', error=error)
    

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
    


app.debug = True 

if __name__ == '__main__':
    app.run()   
