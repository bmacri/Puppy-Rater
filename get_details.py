import re
import requests
import settings

from superclass_GetDogs import GetDogs

class DogDetails(GetDogs):

    def __init__(self):
        pass
        
        
    def trim_contents_singledog(self, contents):
        begin_index = contents.find('<h1 class="title"')
        end_index = contents.find('<div id="animal_profile_logos">', begin_index + 1)
        trimmed_contents = contents[begin_index:end_index] 
        return trimmed_contents
        

    def individual_dog_urls(self, contents, dog_url_list=[]):
        domain = "http://www.sfspca.org"
        animal_name_class = contents.find('"views-field-field-animal-name-value"')
        if animal_name_class == -1:
            return dog_url_list
        link_tag = contents.find('<a href=', animal_name_class + 1)
        start_quote = contents.find('"', link_tag + 1)
        end_quote = contents.find('"', start_quote + 1)
        next_url = domain + contents[start_quote + 1:end_quote]
        dog_url_list.append(next_url)
        #print dog_url_list
        rest_of_urls = self.individual_dog_urls(contents[end_quote + 1:], dog_url_list)
        return dog_url_list
        
    def dog_image(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        begin_image_section = trimmed_contents.find('<h1 class')
        end_image_section = trimmed_contents.find('NAME:', begin_image_section + 1)
        image_section = trimmed_contents[begin_image_section:end_image_section]
        begin_image_index = image_section.find('src=')
        end_image_index = image_section.find('"', begin_image_index + 6)
        image = image_section[begin_image_index + 5:end_image_index]
        return image
        
            
    def dog_name(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_name_index = trimmed_contents.find('NAME:')
        trimmed_contents = trimmed_contents[find_name_index:]
        name = re.search("[A-Z]+[a-z]+", trimmed_contents)
        if name:
            name = name.group()
            return name
        return None

    def dog_id(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_id_index = trimmed_contents.find('ID:')
        trimmed_contents = trimmed_contents[find_id_index:]
        spca_id = re.search("[0-9]+", trimmed_contents)
        if spca_id:
            spca_id = spca_id.group()
            print spca_id
            return spca_id
        return None
        

    def dog_gender(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_gender_index = trimmed_contents.find('GENDER:')
        trimmed_contents = trimmed_contents[find_gender_index:]
        gender = re.search("[A-Z]+[a-z]+", trimmed_contents)
        if gender:
            gender = gender.group()
            return gender
        return None


    def dog_breed(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_breed_index = trimmed_contents.find('BREED:')
        trimmed_contents = trimmed_contents[find_breed_index:]
        breed = re.search('<p class="ap_attr">([^<>]+?)<', trimmed_contents)
        if breed:
            breed = breed.group(1)
            breed = breed.replace(',','\,')
            return breed
        return None
        
    
    def dog_color(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_color_index = trimmed_contents.find('COLOR:')
        trimmed_contents = trimmed_contents[find_color_index:]
        color = re.search("[A-Z]+[a-z]+", trimmed_contents)
        if color:
            color = color.group()
            return color
        return None
            
    
    def dog_age(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_age_index = trimmed_contents.find('AGE:')
        trimmed_contents = trimmed_contents[find_age_index:]
        age = re.search("([0-9]+y) ([0-9]+m)", trimmed_contents)
        if age:
            age = age.group()
            return age
        else:
            return None


    def dog_description(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        begin_description = trimmed_contents.find('"pet-detail">')
        end_description = trimmed_contents.find('</div>', begin_description + 1)
        description = trimmed_contents[begin_description + 13:end_description]
        description = description.replace('&#39;',"\'")
        description = description.replace(',','\,')
        return description




#-------------------------------------------------------------------------------------------------------------------------------------------
dog = DogDetails()

contents = dog.file_contents(settings.project_path + 'alldogs.html')

dog_url_list = dog.individual_dog_urls(contents)
assert dog_url_list[0] == 'http://www.sfspca.org/adoptions/pet-details/10424952-1', dog_url_list[0]
assert dog_url_list[1] == 'http://www.sfspca.org/adoptions/pet-details/15425048-3', dog_url_list[1]
assert dog_url_list[-1] == 'http://www.sfspca.org/adoptions/pet-details/16563222-0', dog_url_list[-1]
assert len(dog_url_list) == 21; len(dog_url_list)

contents = dog.file_contents(settings.project_path + 'singledog.html')
single_dog_dict = dog.dog_details(contents)

assert single_dog_dict['image'] == 'http://www.sfspca.org/sites/default/files/imagecache/animal_profile_default/photos/55513a35-c8c4-4b35-acd8-e90a05746766.jpg', single_dog_dict['image']
assert single_dog_dict['name'] == 'Lychee', single_dog_dict['name']
assert single_dog_dict['spca_id'] == '10424952', single_dog_dict['spca_id']
assert single_dog_dict['gender'] == 'Female', single_dog_dict['gender']
assert single_dog_dict['breed'] == 'Chihuahua\, Short Coat', single_dog_dict['breed']
assert single_dog_dict['color'] == 'Tan', single_dog_dict['color']
assert single_dog_dict['age'] == '3y 8m', single_dog_dict['age']
assert single_dog_dict['description'] == "Lychee is a friendly\, curious\, somewhat shy at first lady who\'s heart\'s desire is to be someone\'s constant friend. She can get a bit overwhelmed at too much noise so would prefer someone who is more book-worm than rock-star.  She is a volunteer favorite for her affectionate personality and stellar leash manners.  She would love to be the only dog in her household.", single_dog_dict['description']

#-------------------------------------------------------------------------------------------------------------------------------------------
def populate_db(contents):
    dog_url_list = dog.individual_dog_urls(contents)
    for url in dog_url_list:
        print url
        contents = dog.return_webpage_contents(url)
        dog_detail_dict = dog.dog_details(contents)
        #dog.dog_details_to_db(dog_detail_dict)
    return
        
        
contents = dog.file_contents(settings.project_path + 'alldogs.html')
populate_db(contents)



