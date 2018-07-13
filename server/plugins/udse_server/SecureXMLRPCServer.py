# -*- coding: utf-8 -*-

from SocketServer import TCPServer, ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler
from ssl import PROTOCOL_SSLv23, wrap_socket

class SecureXMLRPCServer(TCPServer, SimpleXMLRPCDispatcher):
    allow_reuse_address = True
 
    def __init__(self, addr, certfile, keyfile=None, 
            requestHandler=SimpleXMLRPCRequestHandler,
            logRequests=True, allow_none=False, encoding=None, 
            bind_and_activate=True, ssl_version=PROTOCOL_SSLv23):
        self.logRequests = logRequests
        self.ssl_version = ssl_version
        self.keyfile = keyfile
        self.certfile = certfile
 
        SimpleXMLRPCDispatcher.__init__(self, allow_none, 
                encoding)
        # call TCPServer constructor
        TCPServer.__init__(self, addr, requestHandler, 
                bind_and_activate)
 
    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        # create a server-side SSL socket
        sslsocket = wrap_socket(newsocket, server_side=True,
                                ssl_version=self.ssl_version,
                                keyfile=self.keyfile,
                                certfile=self.certfile)
        return sslsocket, fromaddr

class ThreadingSecureXMLRPCServer(ThreadingMixIn, SecureXMLRPCServer): pass
