
# clear;ruby alice.rb

require "./Blog"

#include Blog

def suppress_warnings
    previous_VERBOSE, $VERBOSE = $VERBOSE, nil
    yield
    $VERBOSE = previous_VERBOSE
end

suppress_warnings do
    XMLRPC::Config::ENABLE_NIL_PARSER = true
    XMLRPC::Config::ENABLE_NIL_CREATE = true
end

blog = Blog.new()

poster = "alice"

#blog._out(("alice","gtcn","This graph theory stuff is not easy"))
topic = "gtcn"
messageText = "This graph theory stuff is not easy"
t = [poster, topic, messageText]
output = blog._out(t)
#puts output
puts "topic: " + topic + ", message: " + messageText

#blog._out(("alice","distsys","I like systems more than graphs"))
topic = "distsys"
messageText = "I like systems more than graphs"
t = [poster, topic, messageText]
output = blog._out(t)
#puts output
puts "topic: " + topic + ", message: " + messageText