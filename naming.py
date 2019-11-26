#!/usr/bin/env python3

# clear; python naming.py 224.0.0.1 54323

import sys
import struct
import socket

import proxy
import config

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507
RecoveryFilename = 'naming.out.txt'
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
EventAdapter = 'adapter'

ServerMessage = 'message'
ServerInstance = 'instance'
ServerName = 'name'

NotifyNList = 'notificationlist'
NotifyMList = 'messagelist'

_ts = None

def deserialize(data):
    dList = data.split()

    # print(f'data: {data} len: {len(dList)}')
    event = dList[1]
    data = dList[2] if (event == EventStart) or (event == EventAdapter) else eval(dList[2])
    return {MessageEntity : dList[0], MessageEvent : event,  MessageData : data }

def logToRecovery(recoveryFile, data):
    with open(recoveryFile, 'a+') as f: 
        f.write(f'{data}\n') 
    # print(data, flush=True)

def handleEvent(messageObj, serverList, messageList):

    if ((messageObj[MessageEvent] == EventStart) or (messageObj[MessageEvent] == EventAdapter)):
        print('start handled')

        _ts._out(messageObj[MessageData])

    else:
        print('else handled')

def loadFromRecovery(recoveryFile):
    notificationList = []
    messageList = []

    open(recoveryFile, 'a+').close()
    with open(recoveryFile, 'r') as f: 
        notificationList = [line.rstrip() for line in f]

    messageList = list(map(lambda i: deserialize(i), notificationList))

    return { NotifyNList : notificationList, NotifyMList : messageList }

def replayEvents(messageList):

    replayList = list(filter(lambda i: ((i[MessageEvent] == EventStart) or (i[MessageEvent] == EventAdapter)), messageList))
    # replayList = filterFromList(messageList, MessageEvent, EventStart)
    for replay in replayList:
        _ts._out(replay[MessageData])

def main(address, port):

    config1 = config.read_config()

    adapter_host = config1['adapter']['host']
    adapter_port = config1['adapter']['port']

    adapter_uri = f'http://{adapter_host}:{adapter_port}'

    _ts = proxy.TupleSpaceAdapter(adapter_uri)

    lists = loadFromRecovery(RecoveryFilename)
    # print(lists)
    NotificationList = lists[NotifyNList]
    MessageList = lists[NotifyMList]

    replayEvents(MessageList)

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