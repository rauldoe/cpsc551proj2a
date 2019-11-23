# clear;python3 chuck.py
# clear;python chuck.py

import Blog

blog = Blog.Blog()

topicList = [{'topic' : 'gtcn', 'count' : 6}, {'topic' : 'distsys', 'count' : 6}]

for i in range(len(topicList)):
    for j in range(topicList[i]['count']):
        poster = str
        topic = topicList[i]['topic']
        t = blog._rd_next((poster, topic, str))
        print("reading" + " topic: " + topic)
        print("got message: " + t["output"][2] + " poster: " + t["output"][0])