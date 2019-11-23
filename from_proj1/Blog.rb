require "./XMLRPCLinda"
require "./ConverterModule"

include XMLRPCLinda
include ConverterModule

class Blog
    @client = nil

    def initialize()
        @client = Client1.new(Common.Host, Common.Port)
    end

    def _in(t)
        converted = Converter.tupleToXMLRPCTuple(t)
        @client.sendMessage(Common.getFullyNamedMethod(:take), converted)
    end
    def _rd(t)
        converted = Converter.tupleToXMLRPCTuple(t)
        @client.sendMessage(Common.getFullyNamedMethod(:read), converted)
    end
    def _out(t)
        converted = Converter.tupleToXMLRPCTuple(t)
        @client.sendMessage(Common.getFullyNamedMethod(:write), converted)
    end
end