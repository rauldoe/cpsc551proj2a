#!/usr/bin/env python3
# clear; python recovery.py 224.0.0.1 54322

import sys
import struct
import socket

import proxy

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507
RecoveryFilename = 'recovery.out.txt'
ServerList = {}
NotificationList = []
MessageList = []

MessageEntity = 'entity'
MessageEvent = 'event'
MessageData = 'data'

EventStart = 'start'
EventWrite = 'write'
EventTake = 'take'
EventRead = 'read'

ServerMessage = 'message'
ServerInstance = 'instance'

NotifyNList = 'notificationlist'
NotifyMList = 'messagelist'

def deserialize(data):
    dList = data.split()

    # print(f'data: {data} len: {len(dList)}')
    return {MessageEntity : dList[0], MessageEvent : dList[1],  MessageData : dList[2] }

def logToRecovery(recoveryFile, data):
    with open(recoveryFile, 'a+') as f: 
        f.write(f'{data}\n') 
    # print(data, flush=True)

def handleEvent(messageObj, serverList, messageList):

    if (messageObj[MessageEvent] == EventStart):
        print('start handled')
        ts = proxy.TupleSpaceAdapter(messageObj[MessageData])
        serverList[messageObj[MessageEntity]] = {ServerMessage : messageObj, ServerInstance : ts}

        replayEvents(messageObj[MessageEntity], serverList, messageList)
    elif (messageObj[MessageEvent] == EventWrite):
        print('write handled')
    else:
        print('else handled')

def loadFromRecovery(recoveryFile):
    notificationList = []
    messageList = []

    with open(recoveryFile, 'r') as f: 
        notificationList = [line.rstrip() for line in f]

    messageList = list(map(lambda i: deserialize(i), notificationList))

    return { NotifyNList : notificationList, NotifyMList : messageList }

# def filterFromList(list, tag, val):
#     newList = []

#     for i in list:
#         if (i[tag] == val):
#             newList.append(i)
    
#     return newList

def loadFromRecoveryServers(messageList):

    serverList = []
    replayList = list(filter(lambda i: (i[MessageEvent] == EventStart), messageList))
    # replayList = filterFromList(messageList, MessageEvent, EventStart)
    for replay in replayList:
        ts = proxy.TupleSpaceAdapter(replay[MessageData])
        serverList[replay[MessageEntity]] = {ServerMessage : replay, ServerInstance : ts}
    
    return serverList

def replayEvents(entity, serverList, messageList):
    
    ts = serverList[entity][ServerInstance]

    replayList = list(filter(lambda i: (i[MessageEntity] == entity) and (i[MessageEvent] == EventWrite), messageList))

    for replay in replayList:
        ts._out(replay[MessageData])

def main(address, port):

    lists = loadFromRecovery(RecoveryFilename)
    # print(lists)
    NotificationList = lists[NotifyNList]
    MessageList = lists[NotifyMList]

    ServerList = loadFromRecoveryServers(MessageList)

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

            logToRecovery(RecoveryFilename, notification)

            message = deserialize(notification)

            NotificationList.append(notification)
            MessageList.append(message)
            # print(deserialize(notification))

            handleEvent(message, ServerList, MessageList)
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