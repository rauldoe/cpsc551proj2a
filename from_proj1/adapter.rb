# clear;ruby adapter.rb

require 'xmlrpc/server'

require "./XMLRPCLinda"
require "./LindaDistributed"

def suppress_warnings
    previous_VERBOSE, $VERBOSE = $VERBOSE, nil
    yield
    $VERBOSE = previous_VERBOSE
end

suppress_warnings do
    XMLRPC::Config::ENABLE_NIL_PARSER = true
    XMLRPC::Config::ENABLE_NIL_CREATE = true
end

server = XMLRPCLinda::Server.new(XMLRPCLinda::Common.Port, LindaDistributed::Common.Url)
server.start()