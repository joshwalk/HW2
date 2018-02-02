## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators=[Required()])
	like_rating = RadioField("How much do you like this album? (1 low, 3 high)", choices = [("1", "1" ), ("2", "2"), ("3", "3")], validators=[Required()])
	submit = SubmitField("Submit")



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
	return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')

@app.route('/artistinfo', methods=['GET','POST'])
def artist_info():
	if request.method == 'GET':
		artist = request.args.get('artist')
		response = requests.get("https://itunes.apple.com/search?term=" + artist)
		results = json.loads(response.text)
		data = results['results']
	return render_template("artist_info.html", objects = data)

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
	response = requests.get("https://itunes.apple.com/search?term=" + artist_name)
	results = json.loads(response.text)
	data = results['results']
	return render_template("specific_artist.html", results = data)

@app.route("/album_entry", methods = ['GET', 'POST'])
def album_entry():
	form = AlbumEntryForm()
	return render_template("album_entry.html", form=form)

@app.route('/album_result', methods=['GET', 'POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		album_name = form.album_name.data
		like_rating = form.like_rating.data
		return render_template('album_data.html', album_name=album_name, like_rating=like_rating)

if __name__ == '__main__':
	app.run(use_reloader=True,debug=True)
