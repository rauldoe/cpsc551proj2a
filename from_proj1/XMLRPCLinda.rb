
require "xmlrpc/server"
require 'xmlrpc/client'
require "./LindaDistributed"
require "./ConverterModule"

module XMLRPCLinda
    class Common

        @@Port = 8088
        @@Host = "localhost"
        @@Path = "/"
        @@Namespace = "LindaDistributed"

        def self.Port
            @@Port
        end
        def self.Host
            @@Host
        end
        def self.Path
            @@Path
        end
        def self.Namespace
            @@Namespace
        end
        
        def self.getFullyNamedMethod(method)
            tag = LindaDistributed::Common.OperationLookup[method][:tag]
            "#{@@Namespace}.#{tag}"
        end
    end

    class Server

        @port = nil
        @server = nil
        @lindaUrl = nil
        @lindaClient = nil

        def initialize(port, lindaUrl)
            @port = port
            @lindaUrl = lindaUrl
        end

        def start()

            @server = XMLRPC::Server.new(@port)
            @lindaClient = LindaDistributed::Client.new(@lindaUrl)
            
            puts "Started At #{Time.now}"
            serverProcessThread = Thread.new{internalStart()}
            serverProcessThread.join
            puts "End at #{Time.now}"
        end

        def internalStart()
            addHandlers()
            @server.serve
        end

        def addHandlers()
            
            @server.add_handler(Common.getFullyNamedMethod(:take)) do |t|
                process(:take, t)
            end
            @server.add_handler(Common.getFullyNamedMethod(:read)) do |t|
                process(:read, t)
            end
            @server.add_handler(Common.getFullyNamedMethod(:write)) do |t|
                process(:write, t)
            end
        end

        def getMethodInfo(m)
            {:key => m.to_s, :val => m, m => Common.getFullyNamedMethod(m)}
        end

        def process(m, t)
            method = getMethodInfo(m)
            converted = ConverterModule::Converter.xmlRPCTupleToTuple(t)
            output = @lindaClient.send(method[:val], converted)

            if (!output.is_a?(Module.const_get('Array')))
                output = output.to_s
            end

            { "status" => true, "context" => {"method" => method, "input" => t}, "output": output }
        end
    end

    class Client

        @host = nil
        @port = nil
        @proxy = nil

        def initialize(host, port)
            
            @host = host
            @port = port
            path = Common.Path

            @proxy = XMLRPC::Client.new(@host, path, @port)
        end

        def sendMessage(method, tuple)
            @proxy.call(method, tuple)
        end

    end
end