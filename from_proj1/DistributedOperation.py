
import re
import xmlrpc.client

import ConverterModule

class DistributedOperation:

    xmlrpcUrl = "http://localhost:8088/"
    topicListKey = "__topic_list__"

    def __init__(self):
        with xmlrpc.client.ServerProxy(DistributedOperation.xmlrpcUrl, allow_none=True) as proxy:
            self.srv = proxy.LindaDistributed

    def _in(self, t):
        converted = ConverterModule.Converter.tupleToXMLRPCTuple(t)
        return self.srv._in(converted)

    def _rd(self, t):
        converted = ConverterModule.Converter.tupleToXMLRPCTuple(t)
        return self.srv._rd(converted)

    def _out(self, t):
        converted = ConverterModule.Converter.tupleToXMLRPCTuple(t)
        return self.srv._out(converted)
