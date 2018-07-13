#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Search(QtGui.QHBoxLayout):
  def __init__(self, parent):
    super(Search, self).__init__()

    self.parent = parent

    self.parent.param_filter = QtGui.QComboBox()
    self.parent.param_filter.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
    self.parent.param_filter.setToolTip(u'<b>Параметры поиска</b>')

    self.parent.line_filter = QtGui.QLineEdit()
    self.parent.line_filter.setToolTip(u'<b>Поиск</b>')
    self.parent.line_filter.setPlaceholderText(u'Поиск')
    self.parent.line_filter.textEdited.connect(lambda: self.filter())

    self.parent.find_btn = QtGui.QPushButton(QtGui.QIcon(':/icons/icons/Find.png'), u'')
    self.parent.find_btn.setToolTip(u'<b>Повторить поиск</b>')
    self.connect(self.parent.find_btn, QtCore.SIGNAL('clicked()'), self.filter)

    self.parent.changed_btn = QtGui.QPushButton(QtGui.QIcon(':/icons/icons/Back.png'), u'')
    self.parent.changed_btn.setToolTip(u'<b>Найти измененные элементы</b>')
    self.connect(self.parent.changed_btn, QtCore.SIGNAL('clicked()'), self.showChanged)

    self.addWidget(self.parent.param_filter)
    self.addWidget(self.parent.line_filter)
    self.addWidget(self.parent.find_btn)
    self.addWidget(self.parent.changed_btn)

  def showChanged(self):
    self.parent.tree.blockSignals(True)
    self.parent.tree.collapseAll()
    self.search_list = []
    for i in xrange(self.parent.tree.topLevelItemCount()):
      c_item = self.parent.tree.topLevelItem(i)
      self.findChanged(c_item)
    for i in self.search_list:
      while i.parent() is not None:
        self.parent.tree.expandItem(i.parent())
        i = i.parent()
    self.parent.tree.blockSignals(False)

  def findChanged(self, item):
    if item.changed:
      item.setBackground(0, QtGui.QColor(0, 100, 200, 50))
      self.search_list.append(item)
    else:
      item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
    if item.childCount() > 0:
      for i in xrange(item.childCount()):
        self.findChanged(item.child(i))

  def filter(self):
    self.parent.tree.blockSignals(True)
    self.parent.tree.collapseAll()
    filter_value = str(self.parent.line_filter.text()).decode().lower()
    search_param = str(self.parent.param_filter.currentText())
    self.search_list = []
    for i in xrange(self.parent.tree.topLevelItemCount()):
      c_item = self.parent.tree.topLevelItem(i)
      self.search(c_item, filter_value, search_param)
    for i in self.search_list:
      while i.parent() is not None:
        self.parent.tree.expandItem(i.parent())
        i = i.parent()
      #c_item.setHidden(True)
      #if filter_value in str(c_item.text(0)):
      #  c_item.setHidden(False)
    self.parent.tree.blockSignals(False)

  def search(self, item, filter_value, search_param):
    if filter_value != '':
      if search_param == u'Наименование':
        if filter_value in item.data['title'].lower():
          item.setBackground(0, QtGui.QColor(0, 100, 100, 150))
          item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
          self.search_list.append(item)
        else:
          item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
          item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
      #elif search_param == u'Описание':
      if search_param == u'Описание':
        if filter_value in item.data['description'].lower():
          item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
          item.setBackground(1, QtGui.QColor(0, 100, 100, 150))
          self.search_list.append(item)
        else:
          item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
          item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
      #else:
      for val in item.data['params']:
        if val[1] == search_param:
          try:
            value = val[2].lower()
          except:
            value = str(val[2])
          if filter_value in value:
            item.setBackground(0, QtGui.QColor(0, 100, 100, 150))
            item.setBackground(1, QtGui.QColor(0, 100, 100, 150))
            self.search_list.append(item)
          else:
            item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
            item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
    else:
      item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
      item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
    if item.childCount() > 0:
      for i in xrange(item.childCount()):
        self.search(item.child(i), filter_value, search_param)
