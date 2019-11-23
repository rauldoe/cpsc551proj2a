
from DistributedOperation import DistributedOperation

class Blog(DistributedOperation):

    def __init__(self):
        super().__init__()
        self.readTopicList = []

    def _out_next(self, t):
        topic = t[1]
        method = 'write_count'
        topicInfo = self.processCounter(method, topic)

        t1 = t + (topicInfo[method],)
        # print(str(t1))
        m = self._out(t1)

        return m
    
    def _rd_next(self, t):
        topic = t[1]
        method = 'read_count'
        topicInfo = self.processCounterRead(method, topic)

        t1 = t + (topicInfo[method],)
        # print(str(t1))
        m = self._rd(t1)

        return m

    def processCounter(self, method, topic):
    
        topicList = None
        topicTuple = [DistributedOperation.topicListKey, topicList]
        topicInfo = None

        try:
            
            topicList = self._in(topicTuple)['output'][1]

            index = self.findTopic(topicList, topic)
            if (index == -1):
                topicList.append({'topic' : topic, 'write_count' : 0})
                index = len(topicList)-1
            
            topicInfo = topicList[index]

            topicInfo[method] += 1
            topicList[index] = topicInfo
            topicTuple = [DistributedOperation.topicListKey, topicList]

        except:
            print("Error")

        finally:
            if (topicList == None):
                topicList = []
            topicTuple = [DistributedOperation.topicListKey, topicList]
            self._out(topicTuple)

        return topicInfo 

    def processCounterRead(self, method, topic):
    
        topicList = None
        topicInfo = None

        try:
            
            topicList = self.readTopicList

            index = self.findTopic(topicList, topic)
            if (index == -1):
                topicList.append({'topic' : topic, 'read_count' : 0})
                index = len(topicList)-1
            
            topicInfo = topicList[index]

            topicInfo[method] += 1
            topicList[index] = topicInfo

        except:
            print("Error")

        finally:
            if (topicList == None):
                topicList = []
            self.readTopicList = topicList

        return topicInfo 

    def findTopic(self, lookup, topic):
        index = -1

        for i in range(len(lookup)):
            if (lookup[i]['topic'] == topic):
                index = i
                break
        return index