#!/usr/bin/env python3

# clear; python blog.py -a post -p bob -t "mytopic" -m "mymessage"

import uuid
import argparse

import proxy
import config

from common import Common


def commandLine():

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=str, default='read')
    parser.add_argument('-p', '--poster', type=str, default='alice')
    parser.add_argument('-t', '--topic', type=str, default='gtcn')
    parser.add_argument('-m', '--message', type=str, default='emptymessage')

    return parser.parse_args()

def readBlog(server, poster, args, ts):
    ets = Common.getTsFromNaming(server, Common.TagAdapter, ts)
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

args = commandLine()
# print(f'a {args.action}, p {args.poster}, t {args.topic}, m {args.message}')
ts = Common.getTsFromConfig(Common.EntityNaming, Common.TagAdapter)

if (args.action == 'read'):
    
    if (args.poster == 'all'):
        readBlog('alice', None, args, ts)
    else:
        readBlog(args.poster, args.poster, args, ts)
    # if (args.poster == 'all'):
    
elif (args.action == 'post'):

    td = [args.poster, args.topic, args.message]
    entityList = Common.getEntityTsList(ts)
    for entityObj in entityList:
        entityObj[1]._out(td)
    print(f'post blog: {td}')
# if (args.action == 'read'):
