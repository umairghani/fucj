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

userArray.each do |user|
  firstname, lastname, email, city, zip = user.split(',')
  zip.to_i
  session.execute("INSERT INTO users (firstname, lastname, email, city, zip) VALUES ('#{firstname}', '#{lastname}', '#{email}', '#{city}', #{zip})");
end

rateArray.each do |rate|
  email, notes, score = rate.split(',')
  score.to_i
  session.execute("INSERT INTO raiting (email, score, notes) VALUES ('#{email}', #{score}, '#{notes}')");
end

