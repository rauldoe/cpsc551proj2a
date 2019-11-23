import re

class Converter:
    @staticmethod
    def tupleToXMLRPCTuple(tupleItem):
        l = list(tupleItem)
        for i in range(len(tupleItem)):
            l[i] = Converter.itemToXMLRPCItem(l[i])
        
        return tuple(l)

    @staticmethod
    def itemToXMLRPCItem(item):
        converted = item

        if (type(item) == str):
            converted = item
        elif (type(item) == int):
            converted = item
        elif (item == str):
            converted = {'class' : 'String'}
        elif (item == int):
            converted = {'class' : 'Numeric'}
        elif (type(item) == re.Pattern):
            converted = {'regexp' : item.pattern}
        elif (type(item) == range):
            converted = {'from' : item[0], 'to' : item[len(item)-1]+1}
        elif (type(item) == dict):
            if ('symbol' in item):
                converted = item
            else:
                converted = item
        else:
            converted = item
        
        return converted
