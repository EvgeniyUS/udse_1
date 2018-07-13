# -*- coding: utf-8 -*-

import xmlrpclib
import ssl
import json
import sys

def Server():
  data = json.load(open('cfg.json'))
  ip = data['ip']
  port = data['port']
  pyVersion = sys.version.split(' ')[0].split('.')
  pyVersion[2] = pyVersion[2].translate(None, 'rc')
  if len(pyVersion) == 3:
    if int(pyVersion[2]) > 3:
      return xmlrpclib.ServerProxy("https://{}:{}".format(ip, port), context=ssl._create_unverified_context())
    elif int(pyVersion[2]) <= 8:
      return xmlrpclib.ServerProxy("https://{}:{}".format(ip, port))

