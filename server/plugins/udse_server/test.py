# -*- coding: utf-8 -*-

import ssl
from passlib.hash import lmhash, nthash
import xmlrpclib
import json
import os
import time
import socket

print 'Starting...'

server = xmlrpclib.ServerProxy('https://127.0.0.1:41724')

login = 'root'
password = '12345678'
domain = ''
pwdHash = lmhash.hash(password)+':'+nthash.hash(password)
auth = login, pwdHash

dataType = 'test'


try:
    print 'List:', server.getType(auth).keys()
    print 'Type (template):', server.getType(auth,'template')
    server.addType(auth,'test2')
    print 'AddType:', test2
except xmlrpclib.Fault as error:
    print 'AddType ERROR:', error.faultString
finally:
    print '\n'

try:
    server.addType(auth,dataType)
    print 'AddType:', dataType
except xmlrpclib.Fault as error:
    print 'AddType ERROR:', error.faultString
finally:
    print '\n'

# ПОЛУЧЕНИЕ ВСЕХ ДАННЫХ
try:
    response = server.getData(auth,dataType)
    print type(response)
    data = json.loads(response)
    print 'Get All:', len(data), type(data), data
    for entry in data:
        dataID = entry[0]
        data = entry[1]
        print 'ID:', dataID, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'


data = json.dumps({"test": "ddd"})
print data, type(data)
dataID = 'asdas'

# ДОБАВЛЕНИЕ ДАННЫХ
try:
    dataID = server.addData(auth, dataType, dataID, data)
    print 'Add:', dataID, data
except xmlrpclib.Fault as error:
    print 'Add ERROR:', error.faultString
finally:
    print '\n'
    
# ДОБАВЛЕНИЕ ДАННЫХ
try:
    dataID = server.addData(auth, dataType, dataID, data)
    print 'Add:', dataID, data
except xmlrpclib.Fault as error:
    print 'Add ERROR:', error.faultString
finally:
    print '\n'
    
print dataID

# ПОЛУЧЕНИЕ ДАННЫХ
try:
    response = server.getData(auth, 'file', '[]')
    data = json.loads(response)[0][1]
    print 'Get:', len(data), type(data), data
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'

# ПОЛУЧЕНИЕ ДАННЫХ
try:
    response = server.getData(auth, dataType, dataID)
    data = json.loads(response)[0][1]
    print 'Get:', len(data), type(data), data
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'

#print server.getData('template',json.dumps({'title':u'ММЭ_ММ1'}),'')
#print json.loads(server.getData('template',{},''))

# ПОЛУЧЕНИЕ ВСЕХ ДАННЫХ
try:
    response = server.getData(auth, dataType)
    print type(response)
    data = json.loads(response)
    print 'Get:', len(data), type(data), data
    for entry in data:
        print 'ID:', entry[0], type(entry[1])
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'


# ОТПРАВКА ФАЙЛА
fileName = 'send.zip'
fileData = open(fileName, 'rb').read()
fileInfo = {'name': fileName}
fileInfo['modified'] = os.stat(fileName).st_mtime
print time.strftime("%d.%m.%Y %H:%M:%S",time.localtime(fileInfo['modified']))
fileInfo = json.dumps(fileInfo)
#print 'b64', b64encode(fileData)
#print 'xml', xmlrpclib.Binary(fileData)
try:
    fileID = server.addFile(auth, dataType, dataID, xmlrpclib.Binary(fileData), fileInfo)
    print 'Add File:', fileID, u'файл отправлен'
except xmlrpclib.Fault as error:
    print 'Add File ERROR:', error.faultString
finally:
    print '\n'

#ИНФОРМАЦИЯ О ФАЙЛАХ
fileFilter = {}
fileFilter = json.dumps(fileFilter)
try:
    fileInfo = server.infFile(auth, fileFilter)
    fileInfo = json.loads(fileInfo)
    print 'Info Files:', len(fileInfo), fileInfo
except xmlrpclib.Fault as error:
    print 'Info Files ERROR:', error.faultString
finally:
    print '\n'

#ИНФОРМАЦИЯ О ФАЙЛЕ
fileFilter = json.dumps(fileID)
try:
    response = server.infFile(auth, fileFilter)
    fileInfo = json.loads(response)
    print 'Info File:', fileInfo
except xmlrpclib.Fault as error:
    print 'Info File ERROR:', error.faultString
finally:
    print '\n'

#СКАЧИВАНИЕ ФАЙЛА
try:
    response = server.getFile(auth, fileID)
    open('receive.zip','wb').write(response.data)
    print 'Get File:', u'файл сохранён'
except xmlrpclib.Fault as error:
    print 'Get File ERROR:', error.faultString
finally:
    print '\n'

#УДАЛЕНИЕ ФАЙЛА
try:
    response = server.delFile(auth, fileID)
    print 'Del File:', u'файл удалён'
except xmlrpclib.Fault as error:
    print 'Del File ERROR:', error.faultString
finally:
    print '\n'

#УДАЛЕНИЕ ФАЙЛА
try:
    response = server.delFile(auth, fileID)
    print 'Del File:', u'файл удалён'
except xmlrpclib.Fault as error:
    print 'Del File ERROR:', error.faultString
finally:
    print '\n'


dataNew = json.dumps({"title2": "Person2"})

try:
    response = server.setData(auth, 'test2', dataID, dataNew)
    print 'Set:', dataNew, response
except xmlrpclib.Fault as error:
    print 'Set ERROR:', error.faultString
finally:
    print '\n'
    
#print 'Set3:', dataNew, server.setData('test3', dataID, dataNew , '')

try:
    response = server.getData(auth, dataType, dataID)
    data = json.loads(response)[0][1]
    print 'Get:', data, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'

try:
    response = server.getData(auth, 'test2', dataID)
    data = json.loads(response)[0][1]
    print 'Get:', data, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'

try:
    response = server.getData(auth, 'test3', dataID)
    data = json.loads(response)[0][1]
    print 'Get:', data, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'


try:
    response = server.getData(auth, 'test3', 2423423)
    data = json.loads(response)[0][1]
    print 'Get:', data, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'


try:
    response = server.getData(auth, 'test4', dataID)
    data = json.loads(response)[0][1]
    print 'Get:', data, type(data)
except xmlrpclib.Fault as error:
    print 'Get ERROR:', error.faultString
finally:
    print '\n'

try:
    data = json.loads(server.getData(auth, dataType))
    dataIDs = []
    for entry in data:
        dataIDs.append(entry[0])
    print dataIDs
    response = server.delData(auth, dataType, dataIDs)
    print 'Del All:', response, 'items'
except xmlrpclib.Fault as error:
    print 'Del All ERROR:', error.faultString
finally:
    print '\n'

try:
    response = server.delData(auth, dataType, dataID)
    print 'Del:', response, 'items'
except xmlrpclib.Fault as error:
    print 'Del ERROR:', error.faultString
finally:
    print '\n'

print 'List:', server.getType(auth).keys()

try:
    print 'DelType:', 'test3', server.delType(auth, 'test3')
except xmlrpclib.Fault as error:
    print 'DelType ERROR:', error.faultString
finally:
    print '\n'

try:
    print 'DelType:', dataType, server.delType(auth, dataType)
except xmlrpclib.Fault as error:
    print 'DelType ERROR:', error.faultString
finally:
    print '\n'

print 'DONE!!!'