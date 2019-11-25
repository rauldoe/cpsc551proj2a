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

def deserialize(data):
    dList = data.split()

    # print(f'data: {data} len: {len(dList)}')
    return {'entity' : dList[0], 'event' : dList[1],  'message' : eval(dList[2]) }

def logToRecovery(recoveryFile, data):
    with open(recoveryFile, 'a+') as f: 
        f.write(f'{data}\n') 
    # print(data, flush=True)

def handleEvent(messageObj, serverList, messageList):

    if (messageObj['event'] == 'start'):
        ts = proxy.TupleSpaceAdapter(messageObj['message'])
        serverList[messageObj['entity']] = {'message' : messageObj, 'instance' : ts}

        replayEvents(messageObj['entity'], serverList, messageList)
        print('start handled')
    elif (messageObj['event'] == 'write'):
        print('write handled')
    else:
        print('else handled')

def loadFromRecovery(recoveryFile):
    notificationList = []
    messageList = []

    with open(recoveryFile, 'r') as f: 
        notificationList = [line.rstrip() for line in f]

    messageList = map(lambda i: deserialize(i), notificationList)

    return { 'notificationlist' : notificationList, 'messagelist' : messageList }

def replayEvents(entity, serverList, messageList):
    
    ts = serverList[entity]['instance']

    replayList = list(filter(lambda i: (i['entity'] == entity) and (i['event'] == 'write'), messageList))

    for replay in replayList:
        ts._out(replay['message'])

def main(address, port):

    lists = loadFromRecovery(RecoveryFilename)
    NotificationList = lists['notificationlist']
    MessageList = lists['messsagelist']

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

            logRecovery(RecoveryFilename, notification)

            messageObj = deserialize(notification)

            NotificationList.append(notification)
            MessageList.append(messageObj)
            # print(deserialize(notification))

            handleEvent(messageObj, ServerList, MessageList)
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
