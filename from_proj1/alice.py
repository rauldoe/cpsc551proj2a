# clear;python3 alice.py
# clear;python alice.py

import Blog

blog = Blog.Blog()

poster = "alice"

topic = "gtcn"
messageText = "This graph theory stuff is not easy"
blog._out((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "I like systems more than graphs"
blog._out((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)