#!/usr/local/bin/ruby

require 'cassandra'
require 'json'
require 'rubygems'

#connect to cassandra default is localhost
cluster = Cassandra.cluster
cluster.each_host
keyspace = 'fucj'
session  = cluster.connect(keyspace)

#get test data
testEmail = ARGV[0] 
#testEmail = 'bensmith@email.com'

add = Array.new
usercom = Array.new

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

myavg = average_rating(testEmail,session,add)
  puts "Users average score: #{myavg}"
usercom = user_comments(session,testEmail,usercom)
  puts usercom.each { |x| puts x }
