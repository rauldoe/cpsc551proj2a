# clear;python3 bob.py
# clear;python bob.py

import Blog

blog = Blog.Blog()

poster = "bob"

topic = "distsys"
messageText = "03I am studying chap 2"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "04The linda example’s pretty simple"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "05The linda example’s pretty simple"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "03Cool book"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "04Cool book"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "05Cool book"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)