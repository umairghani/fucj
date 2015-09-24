#!/usr/local/bin/ruby

require 'cassandra'
 
addresses = ["127.0.0.1"]
round_robin = Cassandra::LoadBalancing::Policies::RoundRobin.new
whitelist   = Cassandra::LoadBalancing::Policies::WhiteList.new(addresses, round_robin)
cluster = Cassandra.cluster(retry_policy: Cassandra::Retry::Policies::Default.new,load_balancing_policy: whitelist)
session  = cluster.connect('fucj')


def new_provider()
        #sql statement to add new provider
	#session.execute("INSERT INTO users (firstname, lastname, age, email, city) VALUES ('John', 'Smith', 46, 'johnsmith@email.com', 'Sacramento')");
end

def insert_raiting(rate)
 #sql statement to add raiting from user
 update = session.prepare (
  "UPDATE users SET raiting = ? WHERE (email = ?)"
  )

  stats = [
    {
      :raiting => 9,
      :email => 'blah@blah.com'
    },
  ]

  stats.each do |stat|
    session.execute(update, stat[:raiting], stat[:email])

end

def insert_review(review)
  #sql statement to add review from user
  update = session.prepare (
  "UPDATE users SET review = ? WHERE (email = ?)"
  )
 
  stats = [
    {
      :review => "so much to say",
      :email => 'blah@blah.com'
    },
  ]
 
  stats.each do |stat|
    session.execute(update, stat[:review], stat[:email])
  end
end






