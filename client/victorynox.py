# -*- coding: utf-8 -*-

import json

from cfg import Server
Server = Server()

class VictoryNox(object):
  def __init__(self, parent):
    self.parent = parent

  @staticmethod
  def ttCut(uT, maxlen = 50, cut = 50, cutter=' '):
      #uT = unicode(t)
      if len(uT) <= maxlen:
          return uT.strip()
      s = uT.split(cutter)
      res = []
      tmp = s[0]
      for item in s[1:]:
          if len(tmp)+len(item)<cut:
              tmp = u'%s%s%s' % (tmp, cutter, item)
              continue
          else:
              res.append(tmp+cutter)
              tmp = item
      if tmp:
          res.append(tmp)
      return '\n'.join(res)

  @staticmethod
  def cl(arg):
    bad_symbols = ['/', '\"', '\'', '\\', '$', '%', '@', '#', '№', '!', '`', '~', '^', '&', '=', '[', ']', '{', '}', '|', '?', '<', '>', '*', ':']
    for i in bad_symbols:
      arg = arg.replace(i, '')
    return arg

  @staticmethod
  def getData(auth, table_, type_):
    if table_ == 'file':
      try:
        data = Server.infFile(auth, type_)
        return json.loads(data)
      except Exception, exp:
        #print exp.faultString
        return False
    else:
      try:
        data = Server.getData(auth, table_, type_)
        return json.loads(data)
      except Exception, exp:
        #print exp.faultString
        return False

  @staticmethod
  def getData2(data_, type_=0, id_=0):
    # id
    data = []
    if id_:
      for i in data_:
        ID, item_data = i
        if type(id_) is int or str:
          if ID == id_:
            data.append(i)
        elif type(id_) is list:
          if ID in id_:
            data.append(i)
      return data
    # type
    if type_:
      for i in data_:
        ID, item_data = i
        if type(type_) is str:
          if item_data['type'] == type_:
            data.append(i)
      return data
