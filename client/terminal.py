#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sip, json
from PyQt4 import QtCore, QtGui
import icons

from cfg import Server
Server = Server()

import sys

class Terminal(QtGui.QWidget):
  def __init__(self, parent):
    super(Terminal, self).__init__()
    self.parent = parent
    self.setWindowTitle(u'Терминал')
    self.setWindowIcon(QtGui.QIcon(':/icons/icons/Terminal.png'))

    self.cb = QtGui.QComboBox()
    self.cb.addItems([
                      'getData',
                    ])
    self.le = QtGui.QLineEdit()
    self.te = QtGui.QTextEdit()
    self.te.setReadOnly(True)

    layoutH = QtGui.QHBoxLayout()
    layoutH.addWidget(self.cb)
    layoutH.addWidget(self.le)

    layoutV = QtGui.QVBoxLayout(self)
    layoutV.addWidget(self.te)
    layoutV.addLayout(layoutH)
    self.setLayout(layoutV)

    self.connect(self.le, QtCore.SIGNAL("returnPressed(void)"),
                 self.disp)

  def disp(self):
    cmd = str(self.le.text())
    if self.cb.currentText() == 'getData':
      self.getData(cmd)

  def getData(self, cmd):
    table_, filter_ = cmd.split(',')
    if '\'' in filter_:
      filter_ = filter_.replace('\'', '\"')
    self.te.setText(Server.getData(self.parent.auth, '{}'.format(table_.strip()), '{}'.format(filter_.strip())))

