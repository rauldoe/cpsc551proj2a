#!/usr/bin/env python3
# clear; python recovery.py 224.0.0.1 54322

import sys
import struct
import socket

import proxy
from constants import Constants

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507
RecoveryFilename = 'recovery.out.txt'
ServerList = {}
NotificationList = []
MessageList = []

def deserialize(data):
    dList = data.split()

    # print(f'data: {data} len: {len(dList)}')
    return {Constants.MessageEntity : dList[0], Constants.MessageEvent : dList[1],  Constants.MessageData : eval(dList[2]) }

def logToRecovery(recoveryFile, data):
    with open(recoveryFile, 'a+') as f: 
        f.write(f'{data}\n') 
    # print(data, flush=True)

def handleEvent(messageObj, serverList, messageList):

    if (messageObj[Constants.MessageEvent] == Constants.EventStart):
        print('start handled')
        ts = proxy.TupleSpaceAdapter(messageObj[Constants.MessageData])
        serverList[messageObj[Constants.MessageEntity]] = {Constants.ServerMessage : messageObj, Constants.ServerInstance : ts}

        replayEvents(messageObj[Constants.MessageEntity], serverList, messageList)
    elif (messageObj[Constants.MessageEvent] == Constants.EventWrite):
        print('write handled')
    else:
        print('else handled')

def loadFromRecovery(recoveryFile):
    notificationList = []
    messageList = []

    with open(recoveryFile, 'r') as f: 
        notificationList = [line.rstrip() for line in f]

    messageList = map(lambda i: deserialize(i), notificationList)

    return { Constants.NotifyNList : notificationList, Constants.NotifyMList : messageList }

def loadFromRecoveryServers(messageList):

    serverList = []
    replayList = list(filter(lambda i: (i[Constants.MessageEvent] == Constants.EventStart), MessageList))
    for replay in replayList:
        ts = proxy.TupleSpaceAdapter(replay[Constants.MessageData])
        serverList[replay[Constants.MessageEntity]] = {Constants.ServerMessage : replay, Constants.ServerInstance : ts}
    
    return serverList

def replayEvents(entity, serverList, messageList):
    
    ts = serverList[entity][Constants.ServerInstance]

    replayList = list(filter(lambda i: (i[Constants.MessageEntity] == entity) and (i[Constants.MessageEvent] == Constants.EventWrite), messageList))

    for replay in replayList:
        ts._out(replay[Constants.MessageData])

def main(address, port):

    address = '224.0.0.1'
    port = 54322

    lists = loadFromRecovery(RecoveryFilename)
    print(lists)
    NotificationList = lists[Constants.NotifyNList]
    MessageList = lists[Constants.NotifyMList]

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

            logRecovery(RecoveryFilename, notification)

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
