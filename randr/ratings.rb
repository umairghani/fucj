#!/usr/local/bin/ruby

require 'cassandra'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host 
keyspace = 'fucj'
session	 = cluster.connect(keyspace)

#get test data
#testEmail = 'jkeating@email.com'
testEmail = 'bensmith@email.com'
#testEmail = 'fsmothing@email.com'
#testEmail = 'ughani@email.com'
#testEmail = 'corysmith@email.com'
add = Array.new
usercom = Array.new
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
      add.push(row['score'])
   end
      sum = 0 
      total = add.inject{|sum,x| sum + x }
      average = total / add.length 
   return(average)
end 

def user_comments(session,testEmail,usercom)
   session.execute("SELECT * FROM rating WHERE email = '#{testEmail}'").each do |row|
      usercom.push(row['notes'])
   end
      return(usercom) 
end

input_rating(rateArray,session)
input_new_user(userArray,session)
myavg = average_rating(testEmail,session,add)
  puts "Users average score: #{myavg}" 
usercom = user_comments(session,testEmail,usercom)
  puts usercom.each { |x| puts x } 





