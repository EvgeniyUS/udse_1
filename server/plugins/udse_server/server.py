# -*- coding: utf-8 -*-

from SecureXMLRPCServer import ThreadingSecureXMLRPCServer
from api import API
from settings import srvIP, srvPort, certFile, keyFile

def main():
    try:
        server = ThreadingSecureXMLRPCServer((srvIP, srvPort), certFile, keyFile)
        server.register_instance(API())
        print 'Server accepting secure connections {}...'.format(server.server_address)
        server.serve_forever()
    except Exception as error:
        print str(error).decode('utf8')

if __name__ == '__main__':
    main()
