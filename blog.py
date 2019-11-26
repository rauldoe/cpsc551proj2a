#!/usr/bin/env python3

# clear; python blog.py -a post -p bob -t "my topic" -m "my message"

import argparse
import proxy
import config
import uuid

def commandLine():

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=str, default='read')
    parser.add_argument('-p', '--poster', type=str, default='alice')
    parser.add_argument('-t', '--topic', type=str, default='gtcn')
    parser.add_argument('-m', '--message', type=str, default='emptymessage')

    return parser.parse_args()

def getNamingTs():
    configFile = 'naming.yaml'
    config1 = config.read_config1(configFile)

    adapter_host = config1['adapter']['host']
    adapter_port = config1['adapter']['port']

    adapter_uri = f'http://{adapter_host}:{adapter_port}'

    return proxy.TupleSpaceAdapter(adapter_uri)

def isValidTs(ts):
    isValid = False

    try:
        id = str(uuid.uuid4())
        td = ts._rdp([id])

        if (td is None):
            ts._out([id])
            ts._inp([id])

        isValid = True
    except:
        isValid = False

    return isValid

def getEntityAdapter(ts, entity):
    ets = None
    td = ts._rdp([entity, 'adapter', None])
    if (td is not None):
        eadapter_uri = td[2]
        ets = proxy.TupleSpaceAdapter(eadapter_uri)
        if (not isValidTs(ets)):
            ets = None

    return ets

def getEntityList(ts):
    entityList = []
    serverList = ts._rdp(['server_list', None])

    for server in serverList:
        ets = getEntityAdapter(ts, server)
        if (ets is not None):
            entityList.append(ets)
    
    return entityList

args = commandLine()
# print(f'a {args.action}, p {args.poster}, t {args.topic}, m {args.message}')
ts = getNamingTs()

if (args.action == 'read'):
    
    poster = None
    if (args.poster != 'none'):
        poster = args.poster

        ets = getEntityAdapter(ts, poster)
        if (ets is not None):
            dataList = []
            current = None
            td = [poster, args.topic, None]
            data = ets._inp(td)
            if ((data is not None) and (data != current)):
                dataList.append(data)
                print(f'read blog: {data}')
                current = data
            else:
                data = None

            while (data is not None):
                td = [poster, args.topic, None]
                data = ets._inp(td)
                if ((data is not None) and (data != current)):
                    dataList.append(data)
                    print(f'read blog: {data}')
                else:
                    data = None

            for data in dataList:
                ets._out(data)
        # if (ets is not None):
    # if (args.poster != 'none'):
elif (args.action == 'post'):
    td = [args.poster, args.topic, args.message]
    entityList = getEntityList(ts)
    for ets in entityList:
        ets._out(td)
    print(f'post blog: {td}')
# if (args.action == 'read'):
