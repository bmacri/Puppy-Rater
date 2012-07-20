from superclass_GetDogs import GetDogs
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
		     abort, render_template, flash
import re

class DogDetails(GetDogs):

	def __init__(self):
		pass


	def trim_contents(self, contents):
		begin_index = contents.find('<div class="view-content">')
        end_index = contents.find('<div class="item-list"><ul class="pager"><li class="pager-current first">1</li>')
	    trimmed_contents = contents[begin_index:end_index] 
		return trimmed_contents


	def dog_name(self, contents):
		contents = self.trim_contents(contents)
		begin_name_class_index = contents.find('"views-field-field-animal-name-value">')
		end_name_class_index = contents.find('</a></span>')
		name_class = contents[begin_name_class_index:end_name_class_index + 1]
		name = re.search("[A-z]+[a-z]+", contents)
		return name


	def dog_id(self, contents):
		contents = self.trim_contents(contents)
	    begin_id_class_index = contents.find('views-field-field-id-value">')
        end_id_class_index = contents.find('</a></span>')
        id_class = contents[begin_id_class_index:end_id_class_index + 1]
	    spca_id = re.search("[0-9]+", contents)
        if spca_id:
	        spca_id = spca_id.group()
            return spca_id
        else:
            return None


	def dog_gender(self, contents):
		contents = self.trim_contents(contents)
	    begin_gender_class_index = contents.find('"views-field-field-sex-value">')
        end_gender_class_index = contents.find('</a></span>')
		gender_class = contents[begin_gender_class_index:end_gender_class_index + 1]
        gender = re.search("[A-z]+[a-z]+", contents)    
        if gender:
            gender = gender.group()
            return gender
        else:
		    return None


	def dog_breed(self, contents):
		contents = self.trim_contents(contents)
		begin_id_class_index = contents.find('"views-label-field-primarybreed-value">')
	    end_id_class_index = contents.find('</a></span>')
        id_class = contents[begin_id_class_index:end_name_id_index + 1]
        id = re.search("[A-z]+[a-z]+", contents)
        if gender:
	        gender = gender.group()
            return gender
        else:
            return None


	def dog_age(self, contents):
		contents = self.trim_contents(contents)
		begin_age_class_index = contents.find('')
		end_age_class_index = contents.find('')
		age_class = contents[begin_age_class_index:end_age_class_index]
		age = re.search("[0-9]+y [0-9]+m", contents) #how to match one letter?  y for year and m for month
		if age:
			age = age.group()
			return age
		else:
			return None


	def dog_color(self, contents):
		contents = self.trim_contents(contents)
		begin_photo_field = contents.find('class="views-field-field-photo-fid">')
		single_dog_begin_index = contents.find('a href=', begin_photo_field + 1)
		single_dog_end_index = contents.find('"', single_dog_begin_index + 8)
		url = 'http://www.sfspca.org' + contents[single_dog_begin_index + 8: single_dog_end_index]
		contents = GetDogs.request_url_contents(url)
		begin_color_class = contents.find('<p class="ap_type">COLOR:</p>')
		find_attr_index = contents.find('ap_attr', begin_color_Class + 1)
		end_attr_index = contents.find('</p>', find_attr_index + 1)
		color = contents[find_attr_index + 9:end_attr_index]
		return color


	def dog_description(self, contents):
		contents = self.trim_contents(contents)
	    begin_photo_field = contents.find('class="views-field-field-photo-fid">')
        single_dog_begin_index = contents.find('a href=', begin_photo_field + 1)
        single_dog_end_index = contents.find('"', single_dog_begin_index + 8)
        url = 'http://www.sfspca.org' + contents[single_dog_begin_index + 8: single_dog_end_index]
		contents = GetDogs.request_url_contents(url)
		begin_description_class = contents.find('"pet-detail">')
		end_description_class = contents.find('</div>', begin_description_class + 1)
		description = contents[begin_description + 11:end_description] 
		return description


	def dog_image(self, contents):
		contents = self.trim_contents(contents)
		begin_image_class_index = contents.find('<div class="views-field-field-photo-fid">')
		image_source_begin_index = contents.find('<img src="', begin_image_class_index)
		image_source_end_index = contents.find('"', image_source_begin_index + 10)
		image = contents[image_source_begin_index + 10:image_source_end_index]
		return image
