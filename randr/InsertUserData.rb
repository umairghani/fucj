#!/usr/local/bin/ruby

require 'cassandra'
require 'json'
require 'rubygems'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host
keyspace = 'fucj'
session  = cluster.connect(keyspace)

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

input_new_user(userJdata,session)
puts "input user done"
input_rating(rateJdata,session)
puts "input user done"

