#!/usr/bin/python

import json
import sys
import numpy as np
import gc
from cassandra.cluster import Cluster
from flask import Flask, render_template, flash, request, url_for, redirect, session as session2
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__) 

#GLOBAL VARIABLES
add = []
usercom = []
cluster = Cluster()
session = cluster.connect('fucj')

#REGISTRATION
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        		    validators.Required(),
        		    validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])
    
#HOMEPAGE
@app.route("/")
def homepage():
    title = "Epic site brah"
    try:
        return render_template("index.html", tittle=title)
    except Exception, e:
        return str(e)

#LOGIN 
@app.route('/login/', methods=['GET','POST'])
def login():
    try:
        error = None
        if request.method == 'POST':
	    pwd = session.execute("SELECT * FROM profile WHERE username = '%s'" % request.form['username'])
	    pwd = pwd[0][8]
            if sha256_crypt.verify(request.form['password'], pwd):
                session2['logged_in'] = True
                session2['username'] = request.form['username']
		return redirect(url_for('profile'))
            else:
                error = 'Invalid credentials. Try again'
	gc.collect()
	return render_template('login.html', error=error)
    except Exception, e:
	error = 'Invalid Creds'
	return render_template('login.html', error=error)


@app.route('/register/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
	form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            p = sha256_crypt.encrypt((str(form.password.data)))
            x = session.execute("SELECT * FROM profile WHERE username = '%s'" % username)
            if int(len(x)) > 0:
                print("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
		session.execute("""INSERT INTO profile (username, password, email) VALUES (%s, %s, %s) """,
                        ((username), (p), (email)))
                gc.collect()
                session2['logged_in'] = True
		session2['username'] = username
	 	return redirect(url_for('profile'))
        gc.collect()
        return render_template('register.html', form=form)
    except Exception as e:
        return(str(e))

@app.route('/profile', methods =['Get', 'POST'])
def profile():
    u = session2['username']
    myprofile = []
    for row in session.execute("SELECT * FROM profile WHERE username = '%s'" % u): 
	myprofile=row
    return render_template('profile.html', u=u, myprofile=myprofile)

# Run the app
if __name__ == '__main__':
  app.secret_key = 'super secret'
  app.run(debug=True)





