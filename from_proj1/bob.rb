
# clear;ruby bob.rb

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

poster = "bob"

topic = "distsys"
messageText = "I am studying chap 2"
t = [poster, topic, messageText]
output = blog._out(t)
#puts output
puts "topic: " + topic + ", message: " + messageText

topic = "distsys"
messageText = "The linda example’s pretty simple"
t = [poster, topic, messageText]
output = blog._out(t)
#puts output
puts "topic: " + topic + ", message: " + messageText

topic = "gtcn"
messageText = "Cool book"
t = [poster, topic, messageText]
output = blog._out(t)
#puts output
puts "topic: " + topic + ", message: " + messageText