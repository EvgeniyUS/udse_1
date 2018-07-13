# -*- coding: utf-8 -*-

import sys, os, json
from PyQt4 import QtCore, QtGui
#import icons
import xmlrpclib

from cfg import Server
Server = Server()
from victorynox import VictoryNox
from gui import TreeWidget2, TableWidget, LineEdit, TextEdit, DateEdit, SpinBox, DoubleSpinBox, ComboBox, Link, Files

class InfoForma(QtGui.QTabWidget):
  def __init__(self, parent, parent2):
    QtGui.QFrame.__init__(self, parent)
    self.parent2 = parent2

    # fonts
    self.bold = QtGui.QFont()
    self.bold.setBold(True)
    self.norm_font = QtGui.QFont()
    self.norm_font.setBold(False)

    self.pathLine = QtGui.QLineEdit()
    self.pathLine.setReadOnly(True)

    self.info_forma = TreeWidget2(self)

    typeLab = QtGui.QLabel()
    typeLab.setText(u'Тип: ')
    self.titleLab = QtGui.QLabel()
    self.titleLab.setFont(self.bold)
    self.typeCombo = QtGui.QComboBox()
    self.typeCombo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
    self.typeCombo.currentIndexChanged.connect(self.typeChange)
    self.typeCombo.editTextChanged.connect(self.typeChange)
    self.typeCombo.setEditable(True)
    #self.typeCombo.lineEdit().editingFinished.connect(self.typeChange)
    typeBox = QtGui.QHBoxLayout()
    typeBox.addWidget(self.titleLab)
    typeBox.addStretch(1)
    typeBox.addWidget(typeLab)
    typeBox.addWidget(self.typeCombo)

    paramsMainBox = QtGui.QVBoxLayout()
    paramsMainBox.addLayout(typeBox)
    paramsMainBox.addWidget(self.pathLine)
    paramsMainBox.addWidget(self.info_forma)

    filesMainBox = QtGui.QVBoxLayout()
    self.file_table = Files(self)
    filesMainBox.addWidget(self.file_table)

    self.paramsTab = QtGui.QWidget()
    self.paramsTab.setLayout(paramsMainBox)
    self.filesTab = QtGui.QWidget()
    self.filesTab.setLayout(filesMainBox)
    #self.linksTab = QtGui.QWidget()
    self.addTab(self.paramsTab, u'Параметры')
    self.addTab(self.filesTab, u'Файлы')
    #self.addTab(self.linksTab, u'Связи')
    self.setStyleSheet("QTabBar{font:bold; font-size:12pt; color:grey;}")
    self.setEnabled(False)
    self.currentChanged.connect(self.manager)

  def manager(self):
    if self.currentIndex() == 0:
      self.info_forma.clear()
      self.showParams()
    elif self.currentIndex() == 1:
      self.file_table.setRowCount(0)
      self.file_table.loadFile()
    elif self.currentIndex() == 2:
      print 'inLinks'

  def formChanged(self, widget, w_type, param_title=0):
    c_item = self.parent2.tree.currentItem()
    self.parent2.tree.blockSignals(True)
    #c_item.changed = True
    if w_type == 'QLineEdit':
      c_item.data['params'][widget.type] = [w_type, param_title, str(widget.text())]
    elif w_type == 'QTextEdit':
      c_item.data['params'][widget.type] = [w_type, param_title, str(widget.toPlainText())]
    elif w_type == 'QDateEdit':
      c_item.data['params'][widget.type] = [w_type, param_title, str(widget.date().toString("yyyy.MM.dd"))]
    elif w_type == 'QSpinBox':
      c_item.data['params'][widget.type] = [w_type, param_title, widget.value()]
    elif w_type == 'QDoubleSpinBox':
      c_item.data['params'][widget.type] = [w_type, param_title, widget.value()]
    elif w_type == 'QComboBox':
      widget.blockSignals(True)
      widget.setItemText(widget.currentIndex(), widget.currentText())
      widget.blockSignals(False)
      allItems = [unicode(widget.itemText(i)) for i in range(widget.count())]
      curIndex = widget.currentIndex()
      c_item.data['params'][widget.type] = [w_type, param_title, [allItems, curIndex]]
    elif w_type == 'Link':
      c_item.data['params'][widget.type] = [w_type, param_title, widget.data[2]]
    self.parent2.tree.blockSignals(False)
    self.parent2.notSaved(c_item)

  def pathRead(self, item):
    strPath = ''
    for ID in item.data['path']:
      if ID != 0:
        try:
          strPath = u'{}/{}({})'.format(strPath, self.parent2.IdAndTitle[ID][0], self.parent2.IdAndTitle[ID][1])
        except:
          pass
      else:
        strPath = u'{}/{}'.format(strPath, item.data['title'])
    return strPath

  def typeChange(self):
    c_item = self.parent2.tree.currentItem()
    self.parent2.tree.blockSignals(True)
    c_item.data['type'] = unicode(self.typeCombo.currentText())
    if c_item.data['type'] in self.parent2.TYPES:
      icon = self.parent2.TYPEICONS[self.typeCombo.currentIndex()]
    else:
      icon = ''
    c_item.data['typeIcon'] = icon
    c_item.setIcon(0, self.typeCombo.itemIcon(self.typeCombo.currentIndex()))
    c_item.changed = True
    #try:
    #  c_item.parent().changed = True
    #except:
    #  pass
    self.parent2.tree.blockSignals(False)
    self.parent2.notSaved(c_item)

  def typeWidget(self):
    c_item = self.parent2.tree.currentItem()
    self.typeCombo.blockSignals(True)
    self.typeCombo.clear()
    for i in self.parent2.TYPES:
      icon = self.parent2.TYPEICONS[self.parent2.TYPES.index(i)]
      if icon != '':
        self.typeCombo.addItem(QtGui.QIcon(self.parent2.TYPEICONS[self.parent2.TYPES.index(i)]), i)
      else:
        self.typeCombo.addItem(i)
    if c_item.data['type'] in self.parent2.TYPES:
      self.typeCombo.setCurrentIndex(self.parent2.TYPES.index(c_item.data['type']))
    else:
      self.typeCombo.insertItem(0, c_item.data['type'])
      self.typeCombo.setCurrentIndex(0)
    self.typeCombo.blockSignals(False)

  def showParams(self):
    c_item = self.parent2.tree.currentItem()
    self.titleLab.setText(unicode(c_item.data['title']))

    self.typeWidget()

    self.pathLine.setText(unicode(self.pathRead(c_item)))
    self.pathLine.setToolTip(VictoryNox.ttCut(self.pathRead(c_item), cutter='/'))

    for k, v in enumerate(c_item.data['params']):
      info_forma_item = QtGui.QTreeWidgetItem(self.info_forma)
      info_forma_item.type = k
      info_forma_item.type1 = v[0]
      info_forma_item.setText(0, u"{}".format(v[1]))
      info_forma_item.setToolTip(0, u"{}".format(v[1]))
      reg_ex = QtCore.QRegExp(u"[а-яА-Яa-zA-Z0-9 -_.()\",/@]+")

      if v[0] == 'QLineEdit':
        info_forma_widget = LineEdit(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'QTextEdit':
        info_forma_widget = TextEdit(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'QDateEdit':
        info_forma_widget = DateEdit(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'QSpinBox':
        info_forma_widget = SpinBox(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'QDoubleSpinBox':
        info_forma_widget = DoubleSpinBox(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'QComboBox':
        info_forma_widget = ComboBox(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
      elif v[0] == 'Link':
        info_forma_widget = Link(v, self)
        info_forma_widget.type = k
        info_forma_item.type2 = info_forma_widget
        self.info_forma.setItemWidget(info_forma_item, 1, info_forma_widget)
