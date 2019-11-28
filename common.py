import logging
import uuid

import config
import proxy

class Common:
    MessageEntity = 'entity'
    MessageEvent = 'event'
    MessageData = 'data'

    EventStart = 'start'
    EventWrite = 'write'
    EventTake = 'take'
    EventRead = 'read'
    EventAdapter = 'adapter'

    ServerMessage = 'message'
    ServerInstance = 'instance'
    ServerName = 'name'

    NotifyNList = 'notificationlist'
    NotifyMList = 'messagelist'

    ServerList = 'server_list'
    TagAdapter = 'adapter'
    TagUri = 'uri'
    TagName = 'name'

    EntityNaming = 'naming'

    LogExtension = '.out.txt'

    @staticmethod
    def deserializeNotification(data):

        dList = data.split()

        # print(f'data: {data} len: {len(dList)}')
        event = dList[1]
        data = dList[2] if (event == Common.EventStart) or (event == Common.EventAdapter) else eval(dList[2])

        return {Common.MessageEntity : dList[0], Common.MessageEvent : event,  Common.MessageData : data }

    @staticmethod
    def logNotificationToFile(filename, data):

        with open(filename, 'a+') as f:
            f.write(f'{data}\n')

    @staticmethod
    def loadNotificationFromFile(filename):

        notificationList = []
        messageList = []

        open(filename, 'a+').close()
        with open(filename, 'r') as f: 
            notificationList = list(filter(lambda i: i != '', [line.rstrip() for line in f]))

        messageList = list(map(lambda i: Common.deserializeNotification(i), notificationList))

        return { Common.NotifyNList : notificationList, Common.NotifyMList : messageList }

    @staticmethod
    def getServerList(ts):

        serverList = []
        td = None

        try:
            td = ts._rdp([Common.ServerList, None])
        except:
            logging.error("Error in _inp for getServerList")

        if (td is not None):
            serverList = td[1]
        
        return serverList

    @staticmethod
    def updateServerList(ts, entity):
        
        serverList = Common.getServerList(ts)
        
        if (serverList is not None):
            s = set(serverList)
            s.add(entity)
            serverList = list(s)

        td = [Common.ServerList, serverList]
        
        try:
            ts._out(td)
        except:
            logging.error("Error in _out for updateServerList")            

    @staticmethod
    def getTsAdapterInfoFromConfig(entity):


        configFilename = f'{entity}.yaml'
        configObj = config.read_config_filename(configFilename)
        host = configObj[Common.TagAdapter]['host']
        port = configObj[Common.TagAdapter]['port']

        name = configObj[Common.TagName]
        tsUri = configObj[Common.TagUri]
        adapterUri = f'http://{host}:{port}'

        return (name, tsUri, adapterUri)

    @staticmethod
    def getTsFromConfig(entity, serverType):

        info = Common.getTsAdapterInfoFromConfig(entity)
        ts = proxy.TupleSpaceAdapter(info[2])

        return ts

    @staticmethod
    def getTsFromNaming(entity, serverType, namingTs):
        
        ts = None

        try:
            td = namingTs._rdp([entity, serverType, None])
            if (td is not None):
                uri = td[2]
                ts = proxy.TupleSpaceAdapter(uri)
        except:
            logging.error("Error in _rdp for getTsFromNaming")

        return ts

    @staticmethod
    def isValidTs(ts):

        isValid = False

        if (ts is None):
            return isValid

        try:
            id = str(uuid.uuid4())
            td = ts._rdp([id])

            if (td is None):
                ts._out([id])
                td = ts._inp([id])

            isValid = (td is not None)
        except Exception as e:
            logging.error(f'isValidTs failure {e}')
            isValid = False

        return isValid

    @staticmethod
    def getEntityTsList(ts):

        entityList = []
        serverList = Common.getServerList(ts)

        for server in serverList:
            ets = Common.getTsFromNaming(server, Common.TagAdapter, ts)
            if Common.isValidTs(ets):
                entityList.append([server, ets])
        
        return entityList

    @staticmethod
    def messageToTuple(message):
        return [message[Common.MessageEntity], message[Common.MessageEvent], message[Common.MessageData]]

    @staticmethod
    def replayEvents(entity, entityTs, messageList, eventList, handleEventFunc):

        replayList = list(filter(lambda i: (i[Common.MessageEvent] in eventList), messageList))

        for replay in replayList:
            try:
                handleEventFunc(replay, entityTs)
            except Exception as e:
                logging.error(f'Replay Error {e}')            

    @staticmethod
    def replayEventsAll(ts, entityList, messageList, eventList, handleEventFunc):

        try:
            for i in range(len(entityList)):
                entity = entityList[i][0]
                entityTs = entityList[i][1]
                Common.replayEvents(entity, entityTs, messageList, eventList, handleEventFunc)

        except:
            logging.error("Error in replayEventsAll")