from datetime import date
from flask import Flask
import MySQLdb
import requests
import settings

app = Flask(__name__)

class GetDogs()
	def __init__():
		pass

	def request_url_contents(self, url):
		r = request.get(url)
		return r

	def create_filename(self, url):
		now = datetime.datetime.now()
		filename = url + now
		return filename

	def save_contents(self, url):
		r = request_url_contents(url)
		contents = r.text
		filename = create_filename(url)
		f = open(filename, 'w')
		f.write(contents)
		f.close
	
	def dog_details(self, contents):
		detail_dict = {}
		detail_dict['name'] = self.dog_name(contents)
		detail_dict['spca_id'] = self.dog_id(contents)
		detail_dict['gender'] = self.dog_gender(contents)
		detail_dict['breed'] = self.dog_breed(contents)
		detail_dict['color'] = self.dog_color(contents)
		detail_dict['age'] = self.dog_age(contents)
		detail_dict['description'] = self.dog_description(contents)
		detail_dict['image'] = self.dog_image(contents)
		return detail_dict

	def dog_detailts_to_db(self, detail_dict):
		conn = conn = MySQLdb.connect(host= "localhost",
			                          user="root",
				                      passwd = settings.db_password,
				                      db="dogdetailsdb")
	    cursor = conn.cursor()        
        cursor.execute (" SELECT * FROM  WHERE product_id = %s AND retailer_id = %s ", (product_dict['product_id'],product_dict['retailer_id']))
        rows = cursor.fetchall()
	    if len(rows) == 0: 
	        cursor.execute (" INSERT INTO details (name,spca_id,gender,breed,color,age,description,image) VALUES (%s,%s,%s,%s,%s,%s) ", (detail_dict['name'],detail_dict['spca_id'],detail_dict['gender'],detail_dict['breed'],detail_dict['color'], detail_dict['age'],detail_dict['description'],detail_dict['image']))

														
