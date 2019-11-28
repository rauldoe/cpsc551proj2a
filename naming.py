#!/usr/bin/env python3

# clear; python naming.py 224.0.0.1 54323

import sys
import struct
import socket
import logging

import proxy
import config

from common import Common

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507

# RecoveryFilename = 'naming.out.txt'
# ServerList = {}
# NotificationList = []
# MessageList = []

# MessageEntity = 'entity'
# MessageEvent = 'event'
# MessageData = 'data'

# EventStart = 'start'
# EventWrite = 'write'
# EventTake = 'take'
# EventRead = 'read'
# EventAdapter = 'adapter'

# ServerMessage = 'message'
# ServerInstance = 'instance'
# ServerName = 'name'

# NotifyNList = 'notificationlist'
# NotifyMList = 'messagelist'

# _ts = None

def preInit():

    configInfo = Common.getTsAdapterInfoFromConfig(Common.EntityNaming)
    ts = proxy.TupleSpaceAdapter(configInfo[2])
    if (Common.isValidTs(ts)):
        try:
            td = [configInfo[0], Common.EventStart, configInfo[1]]
            ts._out(td)

            td = [configInfo[0], Common.EventAdapter, configInfo[2]]
            ts._out(td)
        except:
            logging.error(f'preinit failure')

def replayHandlingInfo():
    return [[Common.EventStart, Common.EventAdapter], lambda msg, ts: handleEventForEachMessage(msg, ts)]

def handleEventForEachMessage(message, ts):

    if ((message[Common.MessageEvent] == Common.EventStart) or (message[Common.MessageEvent] == Common.EventAdapter)):
        ts._out(message[Common.MessageData])

def handleEventMain(notification, notificationList, messageList, ts, logFilename):

    message = Common.deserializeNotification(notification)

    entity = message[Common.MessageEntity]
    event = message[Common.MessageEvent]
    
    if ((event == Common.EventStart) or (event == Common.EventAdapter)):
        Common.logNotificationToFile(logFilename, notification)
        tupleData = [entity, event, message[Common.MessageData]]
        try:
            ts._out(tupleData)
        except Exception as e:
            logging.error(f'Update Server List Error {e}') 

        Common.updateServerList(ts, entity)
    
    notificationList.append(notification)
    messageList.append(message)

# def deserialize(data):
#     dList = data.split()

#     # print(f'data: {data} len: {len(dList)}')
#     event = dList[1]
#     data = dList[2] if (event == EventStart) or (event == EventAdapter) else eval(dList[2])
#     return {MessageEntity : dList[0], MessageEvent : event,  MessageData : data }

# def logToRecovery(recoveryFile, data):
#     with open(recoveryFile, 'a+') as f: 
#         f.write(f'{data}\n') 
#     # print(data, flush=True)

# def loadFromRecovery(recoveryFile):
#     notificationList = []
#     messageList = []

#     open(recoveryFile, 'a+').close()
#     with open(recoveryFile, 'r') as f: 
#         notificationList = list(filter(lambda i: i != '', [line.rstrip() for line in f]))

#     messageList = list(map(lambda i: deserialize(i), notificationList))

#     return { NotifyNList : notificationList, NotifyMList : messageList }

# def addItem(myList, item):
#     isFound = False
#     for i in myList:
#         if (i==item):
#             isFound = True
#             break
#     if (not isFound):
#         myList.append(item)
    
#     myList.sort()

#     return myList

# def updateServerList(ts, entity):
#     td = ts._in(['server_list', None])
#     serverList = td[1]
#     serverList = addItem(serverList, entity)
#     td[1] = serverList
#     ts._out(td)

# def replayEvents(messageList, ts):

#     replayList = list(filter(lambda i: ((i[MessageEvent] == EventStart) or (i[MessageEvent] == EventAdapter)), messageList))
#     # replayList = filterFromList(messageList, MessageEvent, EventStart)
#     for replay in replayList:
#         tupleData = [replay[MessageEntity], replay[MessageEvent], replay[MessageData]]
#         ts._out(tupleData)
#         updateServerList(ts, replay[MessageEntity])

def main(address, port):

    preInit()

    logFilename = f'{Common.EntityNaming}{Common.LogExtension}'

    namingTs = Common.getTsFromConfig(Common.EntityNaming, Common.TagAdapter)

    lists = Common.loadNotificationFromFile(logFilename)
    notificationList = lists[Common.NotifyNList]
    messageList = lists[Common.NotifyMList]
    
    eri = replayHandlingInfo()
    Common.replayEventsAll(namingTs, messageList, eri[0], eri[1])

    # See <https://pymotw.com/3/socket/multicast.html> for details

    server_address = ('', int(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")

    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)

            handleEventMain(notification, messageList, notificationList, namingTs, logFilename)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sock.close()

def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))