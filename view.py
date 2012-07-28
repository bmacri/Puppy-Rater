from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from get_details import DogDetails

app = Flask(__name__)
#app.config.from_object(__name__)

dog = DogDetails()

#@route('/login')

@app.route('/dogs')
def show_all_dogs():
    all_db_data = dog.details_from_db()
    return render_template('template.html', all_db_data=all_db_data)

if __name__ == '__main__':
    app.run()   
