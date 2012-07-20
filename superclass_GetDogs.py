import MySQLdb
import requests
import settings

from datetime import date

class GetDogs():
    def __init__():
        pass

    def requests_url_contents(self, url):
        r = requests.get(url)
        return r

    def create_filename(self, url):
        now = datetime.datetime.now()
        filename = url + now
        return filename
        
    def save_contents(self, url):
        r = requests_url_contents(url)
        contents = r.text
        filename = create_filename(url)
        f = open(filename, 'w')
        f.write(contents)
        f.close

    def file_contents(self,filename):
        f = open(filename, 'r')
        contents = f.read()
        f.close()
        return contents

    def return_webpage_contents(self,url):
        r = self.requests_url_contents(url)
        filename = self.create_filename(url)
        self.save_contents(url)
        contents = self.file_contents(filename)
        return contents


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

    def dog_details_to_db(self, detail_dict):
        conn = MySQLdb.connect(host= "localhost",
                                user="root",
                                passwd = settings.db_password,
                                db="spcadogs")
        cursor = conn.cursor()
        rows = cursor.fetchall()
        if len(rows) == 0: 
            cursor.execute (" INSERT INTO details (name,spca_id,gender,breed,color,age,description,image) VALUES (%s,%s,%s,%s,%s,%s) ", (detail_dict['name'],detail_dict['spca_id'],detail_dict['gender'],detail_dict['breed'],detail_dict['color'], detail_dict['age'],detail_dict['description'],detail_dict['image']))
