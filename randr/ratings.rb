#!/usr/local/bin/ruby

require 'cassandra'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host 
keyspace = 'fucj'
session	 = cluster.connect(keyspace)

#get test data
testEmail = 'corysmith@email.com'
add = Array.new
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

def average_rating(testEmail,session,add) 
   session.execute("SELECT * FROM rating WHERE email = '#{testEmail}'").each do |row|
      puts "User #{row['email']} has a score of #{row['score']}."
      add.push(row['score'])
      #puts "'new' + #{add}"
   end
      sum = 0 
      total = add.inject{|sum,x| sum + x }
      average = total / add.length 
      puts "Total is #{total}. Average is #{average}."
   return(add)
end 

def user_comments(session,testEmail)
   session.execute("SELECT * FROM rating WHERE email = '#{testEmail}'").each do |row|
      puts "User #{row['email']} has these comments: #{row['notes']}."
   end
end

input_rating(rateArray,session)
input_new_user(userArray,session)
average_rating(testEmail,session,add)
user_comments(session,testEmail)






