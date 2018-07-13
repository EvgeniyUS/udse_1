# -*- coding: utf-8 -*-

import os, json

try:
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    with open('{}/settings.cfg'.format(currentFolder)) as file:
        config = json.load(file)
    srvIP = config['srvIP']
    srvPort = config['srvPort']
    certFile = '{}/{}'.format(currentFolder, config['certFile'])
    keyFile = '{}/{}'.format(currentFolder, config['keyFile'])
    domains = config['domains']
    ldapBase = config['ldapBase']
    dbName = config['dbName']
    dbUser = config['dbUser']
    dbHost = config['dbHost']
    dbPort = config['dbPort']
    dbPassword = config['dbPassword']
    systemTypes = config['systemTypes']
    reservedTypes = config['reservedTypes']
    referenceTypes = []
    for entry in reservedTypes.values():
        referenceTypes.extend(entry)
except Exception as error:
    raise
