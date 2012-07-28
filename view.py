from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import MySQLdb
from get_details import DogDetails

app = Flask(__name__)
app.config.from_object(__name__)

dog = DogDetails()

#@route('/login')

@app.route('/dogs')
def show_all_dogs():
    all_db_data = dog.details_from_db()
    for each_dog in all_db_data:
        name = each_dog[0]
        spca_id = each_dog[1]
        gender = each_dog[2]
        breed = each_dog[3]    
        color = each_dog[4]
        age = each_dog[5]
        description = each_dog[6]
        image = each_dog[7]
    #flask.render_template(template.html, all_db_data)

show_all_dogs()

if __name__ == '__main__':
    app.run()   
