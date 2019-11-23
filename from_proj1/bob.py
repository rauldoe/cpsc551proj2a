# clear;python3 bob.py
# clear;python bob.py

import Blog

blog = Blog.Blog()

poster = "bob"

topic = "distsys"
messageText = "I am studying chap 2"
blog._out((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "The linda example’s pretty simple"
blog._out((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "Cool book"
blog._out((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)
