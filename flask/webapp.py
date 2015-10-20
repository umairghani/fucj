#!/usr/bin/python

import simplejson as json
import sys
import numpy as np
import gc
import time
from datetime import timedelta
from cassandra.cluster import Cluster
from flask import Flask, render_template, flash, request, url_for, redirect, session as session2, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
#CORS
from flask.ext.cors import CORS


app = Flask(__name__) 
CORS(app)
app.permanent_session_lifetime = timedelta(seconds=900)

#GLOBAL VARIABLES
cluster = Cluster()
session = cluster.connect('fucj')

#def __init__(self, Form): 
username = None
lastname = None
location = None
birthdate = None
phone = None
email = None
password = None
comments = None
myid = None
rating = None

#REGISTRATION
class RegistrationForm(Form):
	firstname = TextField('firstname')
	lastname = TextField('lastname')
	location = TextField('location')
	birthdate = TextField('birthdate')
	phone = TextField('phone')
	comments = TextField('comments')
	rating = TextField('rating')
	email = TextField('email', [validators.DataRequired(), validators.Email()]) 
	password = PasswordField('password', [
        		    validators.Required(),
        		    validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])

class ListingForm(Form):
	summary = TextField('summary')
	price = TextField('price') 
	description = TextField('description') 
	location = TextField('location') 



# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session2:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

#HOMEPAGE
@app.route("/")
@login_required
def homepage():
    try:
	myid = session2['myid']
	return redirect(url_for('user', myid=myid))
    except Exception, e:
        return str(e)

#LOGIN 
@app.route('/login/', methods=['GET','POST'])
def login():
    try:
        error = None
        if request.method == 'POST':
	    sqlrow = session.execute("SELECT * FROM profile WHERE email = '%s'" % request.form['email'])
	    myid = sqlrow[0][2] 
	    pwd = sqlrow[0][6]
            if sha256_crypt.verify(request.form['password'], pwd):
                session2['logged_in'] = True
                session2['email'] = request.form['email']
                session2['myid'] = myid 
		return redirect(url_for('user', myid=myid))
            else:
                error = 'Invalid credentials. Try again'
	gc.collect()
	return render_template('login.html', error=error)
    except Exception, e:
	error = 'Invalid Creds'
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session2.pop('logged_in', None)
	u = session2['email']
	flash("You were just logged out! '%s' brah!" % u) 
	return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
	date = int(time.time())
	date = str(date)
	form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data
            p = sha256_crypt.encrypt((str(form.password.data)))
            x = session.execute("SELECT * FROM profile WHERE email = '%s'" % email)
            if int(len(x)) > 0:
                flash("That email is already registered, please choose another!") 
                return render_template('register.html', form=form)
            else:
		session.execute("""INSERT INTO profile (password, email, date) VALUES (%s, %s, %s) """,
                        (p, email, date))
                session2['logged_in'] = True
		session2['email'] = email 
		session2['myid'] = date
		myid = session2['myid'] 
	 	return redirect(url_for('user', myid=myid))
        gc.collect()
        return render_template('register.html', form=form)
    except Exception as e:
        return(str(e))


@app.route('/profile/', methods =['GET', 'POST'])
@app.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
        form = RegistrationForm(request.form) 
        myprofile = [] 
        if request.method == 'POST': 
            email = form.email.data 
            firstname = form.firstname.data 
            lastname = form.lastname.data 
            birthdate = form.birthdate.data 
            location = form.location.data 
            phone = form.phone.data 
	    session.execute("""UPDATE profile SET firstname = %s, lastname = %s, birthdate = %s, location = %s, phone = %s WHERE email = %s""",
			   (firstname, lastname, birthdate, location, phone, email))
            return render_template('profile.html', action="Edit", myprofile=myprofile)
        else:
            email = form.email.data
            e = session2['email']
	    flash(session2)
            for row in session.execute("SELECT * FROM profile WHERE email = '%s'" % e): 
                myprofile=row
        return render_template('profile.html', myprofile=myprofile)


@app.route('/listing/', methods =['GET', 'POST'])
@app.route('/listing', methods =['GET', 'POST'])
#@login_required
def listing():
        print "here"
        form = ListingForm(request.form)
        mylisting = []
        if request.method == 'POST':
          summary = form.summary.data
          price = form.price.data
          description = form.description.data
          location = form.location.data
          myid = session2['myid']
          session.execute("""INSERT INTO listing (date, summary, price, description, location) VALUES (%s, %s, %s, %s, %s) """,(myid, summary, price, description, location))
          return json.dumps(mylisting)
        else:
          return json.dumps(session.execute("SELECT * from listing"))
		#return render_template('listing.html', action="Edit", mylisting=mylisting)
        #else:
		#return render_template('listing.html')




@app.route('/dashboard/', methods =['GET', 'POST'])
@app.route('/dashboard', methods =['GET', 'POST'])
@login_required
def dashboard():
	myprofile = []
	myreviews = []
	myemail = session2['email']
	myid = session2['myid']
	for row in session.execute("SELECT * FROM profile"):
		myprofile.append(row)
	return render_template('dashboard.html', myemail=myemail, myprofile=myprofile)

#HOMEPAGE
@app.route('/user/<myid>', methods =['GET', 'POST'])
@login_required
def user(myid):
	myprofile = []
	myreviews = []
	form = RegistrationForm(request.form)
	if request.method == 'POST':
	        now = int(time.time())
	        now = str(now)
		comments = form.comments.data
		customer = myid 
		rating = form.rating.data
		reviewer= session2['email']
		session.execute("""INSERT INTO reviews(date, comments, customer, reviewer, rating) VALUES (%s, %s, %s, %s, %s) """,
				(now, comments, customer, reviewer, rating))
		return redirect(url_for('user', myid=myid))
	else:	
                for row in session.execute("SELECT * FROM reviews WHERE customer = '%s'" % myid):
                        myreviews.append(row)
		for row in session.execute("SELECT * FROM profile WHERE date = '%s'" % myid):
			myprofile=row
        return render_template('user.html', myid=myid, myreviews=myreviews, myprofile=myprofile)



# Run the app
if __name__ == '__main__':
	app.secret_key = 'super secret'
	app.run(host='10.222.185.35', port=8080, debug=True)





