import signal
import sys
import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import functions.airbnb as airbnb
import functions.queries as queries


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('localhost', 9000,), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def signal_handler(signum, frame):
        print("\nreceived signal")
        server.server_close()

        # perform clean up, etc. here...

        print("exiting, gracefully")
        sys.exit(0)

    os.system("clear")
    print("Starting..")

    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # register both functions
    server.register_function(airbnb.insert)
    server.register_function(airbnb.delete)
    server.register_function(airbnb.index)
    server.register_function(queries.fetchAirbnbs)
    server.register_function(queries.fetchAreas)
    server.register_function(queries.fetchTypes)
    server.register_function(queries.countAirbnbs)
    server.register_function(queries.fetchByArea)
    server.register_function(queries.fetchByType)

    # start the server
    print("RPC Server has started!")
    server.serve_forever()
