#!/usr/bin/python


import json
import sys
import numpy as np
from flask import Flask, render_template, request, url_for
from cassandra.cluster import Cluster

#GLOBAL VARIABLES
app = Flask(__name__) 
add = []
usercom = []
cluster = Cluster()
session = cluster.connect('fucj')


#DB STUFF

def input_new_user(firstname,lastname,email,city,zip): 
	session.execute("""INSERT INTO users (firstname, lastname, email, city) 
		VALUES (%s, %s, %s, %s) """,
		(firstname, lastname, email, city))
	return()

def average_rating(testEmail,session,add):
	for row in session.execute("select * from rating where email = '%s'" % testEmail): 
		add.append(row.score)
	total = np.average(add)	
	return (total) 

def user_comments(session,testEmail,usercom):
	for row in session.execute("SELECT * FROM rating WHERE email = '%s'" % testEmail):
		usercom.append(row.notes)
	return (usercom)

#HTML FLASK STUFF
@app.route("/")
def form(): 
	return render_template('form_submit.html')

@app.route('/hello/', methods=['POST'])
def hello():
	firstname=request.form['firstname']
	lastname=request.form['lastname']
	email=request.form['email']
	city=request.form['city']
	zipcode=request.form['zipcode']
	input_new_user(firstname,lastname,email,city,zipcode)
	myavg=average_rating(email,session,add)
	comments=user_comments(session,email,usercom)
	return render_template('form_action.html', firstname=firstname, email=email, myavg=myavg, comments=comments)


# Run the app
if __name__ == '__main__':
  app.run(debug=True)





