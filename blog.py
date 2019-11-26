#!/usr/bin/env python3

# clear; python blog.py -a post -p bob -t "my topic" -m "my message"

import argparse
import proxy
import config

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', type=str, default='read')
parser.add_argument('-p', '--poster', type=str, default='alice')
parser.add_argument('-t', '--topic', type=str, default='gtcn')
parser.add_argument('-m', '--message', type=str, default='empty message')

args = parser.parse_args()

# print(f'a {args.action}, p {args.poster}, t {args.topic}, m {args.message}')
configFile = 'naming.yaml'
config1 = config.read_config1(configFile)

ts_name      = config1['name']
adapter_host = config1['adapter']['host']
adapter_port = config1['adapter']['port']

adapter_uri = f'http://{adapter_host}:{adapter_port}'

ts = proxy.TupleSpaceAdapter(adapter_uri)

etd = ts._rdp([args.poster, 'adapter', None])
if (etd is not None):
    eadapter_uri = etd[2]
    ets = proxy.TupleSpaceAdapter(eadapter_uri)

    if (args.action == 'read'):
        dataList = []
        current = None
        td = [args.poster, args.topic, None]
        data = ets._inp(td)
        if ((data is not None) and (data != current)):
            dataList.append(data)
            print(f'read blog: {data}')
            current = data
        else:
            data = None

        while (data is not None):
            td = [args.poster, args.topic, None]
            data = ets._inp(td)
            if ((data is not None) and (data != current)):
                dataList.append(data)
                print(f'read blog: {data}')
            else:
                data = None
        for data in dataList:
            ets._out(data)
    elif (args.action == 'post'):
        td = [args.poster, args.topic, args.message]
        ets._out(td)
        print(f'post blog: {td}')
    # if (args.action == 'read'):
