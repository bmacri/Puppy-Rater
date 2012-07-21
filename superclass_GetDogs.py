import codecs
import MySQLdb
import pdb
import requests
import settings

path = '/home/bethany/hackerschool/Puppy_Rater/pupfiles/'

class GetDogs():
    def __init__():
        pass

    def requests_url_contents(self, url):
        r = requests.get(url)
        return r

    def create_filename(self, url):
        url_sections = url.split('/')
        filename = path + url_sections[-1] + '.html'
        return filename
        
    def save_contents(self, url):
        r = self.requests_url_contents(url)
        contents = r.text
        filename = self.create_filename(url)
        #pdb.set_trace()
        #print repr(filename)
        f = codecs.open(filename, 'w', encoding='utf-8')
        f.write(contents)
        f.close
        return filename

    def file_contents(self,filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        contents = f.read()
        f.close()
        return contents

    def return_webpage_contents(self,url):
        filename = self.save_contents(url)
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
        #pdb.set_trace()
        cursor = conn.cursor()
        #cursor.execute("TRUNCATE dogdetails;")
        #conn.commit()
        cursor.execute ("INSERT INTO dogdetails (name, spca_id, gender, breed, color, age, description, image) VALUES (%(name)s, %(spca_id)s, %(gender)s, %(breed)s, %(color)s, %(age)s, %(description)s, %(image)s);", detail_dict)
        conn.commit()
