#!/usr/local/bin/ruby

require 'cassandra'
require 'json'
require 'rubygems'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host 
keyspace = 'fucj'
session	 = cluster.connect(keyspace)

#get test data
testEmail = 'rschmidt7@sitemeter.com'
#testEmail = 'bensmith@email.com'

add = Array.new
usercom = Array.new
userData = File.read('USER.json')
userJdata = JSON.parse(userData)
rateData = File.read('RATE.json')
rateJdata = JSON.parse(rateData)

def input_new_user (userJdata,session)
   userJdata.each do |line|
     firstname = line["firstname"]
     lastname = line["lastname"]
     email = line["email"]
     city = line["city"]
     session.execute("INSERT INTO users (firstname, lastname, email, city) VALUES ('#{firstname}', '#{lastname}', '#{email}', '#{city}')");
   end
end 

def input_rating(rateJdata,session)
   rateJdata.each do |line|
     date = Time.now.to_f
     email = line["email"]
     score = line["score"]
     notes = line["notes"]
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


input_rating(rateJdata,session)
input_new_user(userJdata,session)
myavg = average_rating(testEmail,session,add)
  puts "Users average score: #{myavg}" 
usercom = user_comments(session,testEmail,usercom)
  puts usercom.each { |x| puts x } 





