#!/usr/local/bin/ruby

require 'cassandra'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host 
keyspace = 'fucj'
session	 = cluster.connect(keyspace)

#get test data
rateArray = Array.new
rateArray = IO.readlines('rate.txt')

userArray = Array.new
userArray = IO.readlines('newuser.txt')

def input_new_user (userArray,session)
   userArray.each do |user|
     firstname, lastname, email, city, zip = user.split(',')
     zip.to_i
     session.execute("INSERT INTO users (firstname, lastname, email, city, zip) VALUES ('#{firstname}', '#{lastname}', '#{email}', '#{city}', #{zip})");
   end
end 

def input_rating(rateArray,session)
   rateArray.each do |rate|
     email, notes, score = rate.split(',')
     score.to_i
     date = Time.now.to_f
     session.execute("INSERT INTO rating (date, email, score, notes) VALUES ('#{date}', '#{email}', #{score}, '#{notes}')");
   end
end 

def average_rating() 
   email = 'corysmith@email.com'
   add = Array.new
   session.execute("SELECT * FROM rating WHERE email = '#{email}'").each do |row|
   puts "User #{row['email']} has a score of #{row['score']}."
   add = row['score']
   end
end 


input_rating(rateArray,session)
input_new_user(userArray,session)

