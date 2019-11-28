#!/usr/bin/env python3

# clear; python recovery.py 224.0.0.1 54322

import sys
import struct
import socket
import uuid

import proxy
import config

from common import Common

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


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

def replayHandlingInfo():
    return [[Common.EventWrite, Common.EventTake], lambda msg, ts: handleEventForEachMessage(msg, ts)]

def handleEventForEachMessage(message, ts):

    if (message[Common.MessageEvent] == Common.EventWrite):
        ts._out(message[Common.MessageData])
    elif (message[Common.MessageEvent] == Common.EventTake):
        # ignore return value
        ts._inp(message[Common.MessageData])

def handleEventMain(notification, notificationList, messageList, ts, logFilename):

    message = Common.deserializeNotification(notification)

    entity = message[Common.MessageEntity]
    event = message[Common.MessageEvent]

    if (event == Common.EventStart):
        Common.logNotificationToFile(logFilename, notification)

        ets = Common.getTsFromNaming(entity, Common.TagAdapter, ts)
        eri = replayHandlingInfo()

        Common.replayEvents(entity, ets, messageList, eri[0], eri[1])
    elif ((event == Common.EventWrite) or (event == Common.EventTake)):
        Common.logNotificationToFile(logFilename, notification)
    else:
        return

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

# def getTs(entity):
#     configFilename = f'{entity}.yaml'
#     configObj = config.read_config_filename(configFilename)
#     adapter_host = configObj['adapter']['host']
#     adapter_port = configObj['adapter']['port']

#     adapter_uri = f'http://{adapter_host}:{adapter_port}'
#     ts = proxy.TupleSpaceAdapter(adapter_uri)
#     return ts

# def loadFromRecovery(recoveryFile):
#     notificationList = []
#     messageList = []

#     open(recoveryFile, 'a+').close()
#     with open(recoveryFile, 'r') as f: 
#         notificationList = list(filter(lambda i: i != '', [line.rstrip() for line in f]))

#     messageList = list(map(lambda i: deserialize(i), notificationList))

#     return { NotifyNList : notificationList, NotifyMList : messageList }

# def loadServerInfoFromRecovery(messageList):

#     serverList = {}
#     replayList = list(filter(lambda i: (i[MessageEvent] == EventStart), messageList))
#     # replayList = filterFromList(messageList, MessageEvent, EventStart)
#     for replay in replayList:

#         ts = getTs(replay[MessageEntity])
#         serverList[replay[MessageEntity]] = {ServerName : replay[MessageEntity], ServerMessage : replay, ServerInstance : ts}
    
#     return serverList

# def replayEvents(entity, entityAdapter, messageList):

#     replayList = list(filter(lambda i: (i[MessageEntity] == entity) and ((i[MessageEvent] == EventWrite) or (i[MessageEvent] == EventTake)), messageList))

#     for replay in replayList:
#         try:
#             if (replay[MessageEvent] == EventWrite):
#                 entityAdapter._out(replay[MessageData])
#             elif (replay[MessageEvent] == EventTake):
#                 j = entityAdapter._inp(replay[MessageData])
#                 print(f'write {j}')
#         except Exception as e:
#             print(f'replay err {e}')

# def replayEventsAll(namingAdapter, messageList):
    
#     try:
#         td = namingAdapter._rdp(['server_list', None])
#         if (td is not None):
#             serverList = td[1]
#             for server in serverList:
#                 td1 = namingAdapter._rd([server, 'adapter', None])
#                 adapterUri = td1[2]
#                 entityAdapter = proxy.TupleSpaceAdapter(adapterUri)
#                 replayEvents(server, entityAdapter, messageList)
#     except Exception as e:
#         print(f'naming: {e}')

# def isValidTs(ts):
#     isValid = False

#     try:
#         id = str(uuid.uuid4())
#         td = ts._rdp([id])

#         if (td is None):
#             ts._out([id])
#             ts._inp([id])

#         isValid = True
#     except:
#         isValid = False

#     return isValid

# def getEntityAdapter(ts, entity):
#     ets = None
#     td = ts._rdp([entity, 'adapter', None])
#     if (td is not None):
#         eadapter_uri = td[2]
#         ets = proxy.TupleSpaceAdapter(eadapter_uri)
#         if (not isValidTs(ets)):
#             ets = None

#     return ets

# def getEntityList(ts):
    # entityList = []
    # serverList = ts._rdp(['server_list', None])

    # for server in serverList:
    #     ets = getEntityAdapter(ts, server)
    #     if (ets is not None):
    #         entityList.append(ets)
    
    # return entityList

def main(address, port):

    logFilename = f'recovery{Common.LogExtension}'

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

            handleEventMain(notification, messageList, notificationList, namingTs, logFilename)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        print(f'{e}')
        sock.close()

def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))