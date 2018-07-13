import xmlrpclib
from passlib.hash import lmhash, nthash

print 'Starting...'

server = xmlrpclib.ServerProxy('https://127.0.0.1:41724')

login = 'root'
password = '12345678'
domain = ''
pwdHash = lmhash.hash(password)+':'+nthash.hash(password)
auth = login, pwdHash
print server.getAuth(auth)
print server.getUser(auth)
