# clear;python3 alice.py
# clear;python alice.py

import Blog

blog = Blog.Blog()

poster = "alice"

topic = "gtcn"
messageText = "00This graph theory stuff is not easy"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "00I like systems more than graphs"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "01This graph theory stuff is not easy23232"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "01I like systems more than graph23232dssdsssdds565s"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "distsys"
messageText = "02I like systems modsdksd232"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)

topic = "gtcn"
messageText = "02This grgew32uff is not easy23232"
blog._out_next((poster, topic, messageText))
print("topic: " + topic + ", message: " + messageText)