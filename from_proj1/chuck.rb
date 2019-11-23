
# clear;ruby chuck.rb

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

stringClass = Module.const_get('String')

poster = "bob"
topic = "distsys"
t1 = blog._rd([poster, topic, stringClass])
puts "reading poster: " + poster + ", topic: " + topic
puts "got message: " + t1["output"][2]

poster = "alice"
topic = "gtcn"
t2 = blog._rd([poster, topic, stringClass])
puts "reading poster: " + poster + ", topic: " + topic
puts "got message: " + t2["output"][2]

poster = "bob"
topic = "gtcn"
messageText = stringClass
t = [poster, topic, messageText]
puts "reading poster: " + poster + ", topic: " + topic
puts "got message: " + t1["output"][2]
