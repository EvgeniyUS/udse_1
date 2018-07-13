#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json, sip
from PyQt4 import QtCore, QtGui

from gui import Splitter, TreeWidget, Frame, TypeDialog
from cfg import Server
Server = Server()
from infoforma import InfoForma
from victorynox import VictoryNox
from search import Search
from buttons import Buttons

class Basic(QtGui.QWidget):
  def __init__(self, parent, winType, winTitle, winIcon, defaultType):
    super(Basic, self).__init__()
    self.parent = parent
    self.progress = self.parent.progress
    self.type = winType
    self.setWindowTitle(winTitle)
    self.setWindowIcon(QtGui.QIcon(winIcon))
    self.defaultType = defaultType

    # fonts
    self.bold = QtGui.QFont()
    self.bold.setBold(True)
    self.bold.setPointSize(12)

    self.tree_widget = Frame()
    self.tree = TreeWidget(self)

    dev_vbox = QtGui.QVBoxLayout()
    dev_vbox.addLayout(Buttons(self, winTitle))
    dev_vbox.addWidget(self.tree)
    dev_vbox.addLayout(Search(self))
    self.tree_widget.setLayout(dev_vbox)

    self.type_filter.setHidden(False)

    self.splitter = Splitter('h')
    self.splitter.addWidget(self.tree_widget)

    self.info_forma_frame = InfoForma(self.splitter, self)
    self.info_forma = self.info_forma_frame.info_forma

    main_hbox = QtGui.QHBoxLayout()
    main_hbox.addWidget(self.splitter)

    self.setLayout(main_hbox)
    #self.splitter.setStretchFactor(0, 1)
    #self.splitter.setStretchFactor(1, 1)

    self.refresh(tree=True)

  def notSaved(self, item=False):
    #self.save_btn.setEnabled(True)
    #self.type_filter.setEnabled(False)
    if item:
      self.saveAndGetId(item)
    self.refresh(tree=False)

  def saved(self):
    self.save_btn.setEnabled(False)
    self.type_filter.setEnabled(True)

  def delItem(self, delList, trueDel=0, fakeDel=0):
    reply = QtGui.QMessageBox.question(self, u'Внимание!',
      u'Удалить все выделенные элементы?',
      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
      toDelete = []
      for c_item in delList:
        if c_item.parent():
          c_item.data['path'] = [c_item.id]
          self.notSaved(c_item)
          #Server.setData(self.parent.auth, self.type, c_item.id, json.dumps(c_item.data))
          if c_item.parent() is not None:
            c_item.parent().data['composition'].remove(c_item.id)
            c_item.parent().changed = True
            self.notSaved(c_item.parent())
            #Server.setData(self.parent.auth, self.type, c_item.parent().id, json.dumps(c_item.parent().data))
        else:
          toDelete.append(c_item.id)
          #print Server.delData(self.parent.auth, self.type, '{}'.format(c_item.id)), u"удалено", c_item.type
        sip.delete(c_item)
      if len(toDelete) > 0:
        Server.delData(self.parent.auth, self.type, toDelete)
      self.refresh()

  def typeParams(self):
    if len(self.TYPES) != 0:
      cur_index = self.type_filter.currentIndex()
      ok, name, icon = TypeDialog(self).typeEdit(unicode(self.type_filter.currentText()),
                self.TYPEICONS[cur_index])
      if ok:
        for i in xrange(self.tree.topLevelItemCount()):
          item = self.tree.topLevelItem(i)
          item.data['type'] = name
          item.data['typeIcon'] = icon
          item.setIcon(0, QtGui.QIcon(icon))
          item.changed = True
          self.notSaved(item)
        self.TYPEICONS[cur_index] = icon
        self.TYPES[cur_index] = name
        #self.notSaved()

  def refreshDisp(self, tree_vals, par_item=0):
    self.progress.setVisible(True)
    self.pb_step = 100 / float(len(tree_vals))
    self.pb_value = 0
    self.progress.setValue(self.pb_value)
    self.start_item = tree_vals[0][1]['type']
    return self.itemRead(par_item, tree_vals)

  def paramsAndTypes(self):
    self.PARAMS = {
                    'QLineEdit':[],
                    'QTextEdit':[],
                    'QSpinBox':[],
                    'QDoubleSpinBox':[],
                    'QDateEdit':[],
                    'Link':[],
                    'File':[],
                    'QComboBox':[],
                    }
    self.TYPES = []
    self.TYPEICONS = []
    self.IdAndTitle = {}
    if self.DATA:
      for ID, data in self.DATA:
        self.IdAndTitle[ID] = [data['title'], data['type']]
        if data['type'] not in self.TYPES:
          self.TYPES.append(data['type'])
          self.TYPEICONS.append(data['typeIcon'])
        for v in data['params']:
          if v[0] in self.PARAMS.keys():
            if v[0] == 'QLineEdit':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'QTextEdit':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'QSpinBox':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'QDoubleSpinBox':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'QDateEdit':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'Link':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'File':
              self.PARAMS[v[0]].append(v[1])
            elif v[0] == 'QComboBox':
              comboName = u'{} => {}'.format(v[1], data['title'])
              existNames = []
              for i in self.PARAMS[v[0]]:
                existNames.append(i[0])
              if comboName not in existNames:
                self.PARAMS[v[0]].append([comboName, v[2]])
      for k, v in self.PARAMS.items():
        #if k != 'QComboBox':
        #  self.PARAMS[k] = list(set(v))
        if k == 'QComboBox':
          pass
        elif k == 'Link':
          pass
        else:
          self.PARAMS[k] = list(set(v))
    self.param_filter.blockSignals(True)
    self.param_filter.clear()
    self.param_filter.addItems([u'Наименование', u'Описание'])
    self.param_filter.addItems(self.PARAMS['QLineEdit'])
    self.param_filter.addItems(self.PARAMS['QTextEdit'])
    self.param_filter.addItems(self.PARAMS['QSpinBox'])
    self.param_filter.addItems(self.PARAMS['QDoubleSpinBox'])
    self.param_filter.blockSignals(False)

  def refresh(self, tree=False):
    self.DATA = VictoryNox.getData(self.parent.auth, self.type, [])
    self.paramsAndTypes()
    self.tree.blockSignals(True)
    self.type_filter.blockSignals(True)
    cur_type_text = self.type_filter.currentText()
    self.type_filter.clear()
    for i in self.TYPES:
      icon = self.TYPEICONS[self.TYPES.index(i)]
      if icon != '':
        self.type_filter.addItem(QtGui.QIcon(icon), i)
      else:
        self.type_filter.addItem(i)
    if self.type_filter.findText(self.defaultType) >= 0:
      self.type_filter.setCurrentIndex(self.type_filter.findText(self.defaultType))
    self.type_filter.blockSignals(False)
    self.tree.blockSignals(False)
    if self.type_filter.findText(cur_type_text) != -1:
      self.type_filter.setCurrentIndex(self.type_filter.findText(cur_type_text))
    if tree:
      self.refreshTree()

  def refreshTree(self):
    self.tree.blockSignals(True)
    if self.DATA:
      self.tree.clear()
      tree_vals = VictoryNox.getData2(self.DATA, type_=str(self.type_filter.currentText()))
      if tree_vals:
        self.info_forma.clear()
        self.info_forma_frame.setEnabled(False)
        self.tree.clearSelection()
        self.saved()
        self.refreshDisp(tree_vals)
    else:
      self.info_forma.clear()
    self.tree.blockSignals(False)

  def showLink(self, ID):
    self.tree.blockSignals(True)
    for i in xrange(self.tree.topLevelItemCount()):
      item = self.tree.topLevelItem(i)
      if item.id == ID:
        item.setBackground(0, QtGui.QColor(100, 0, 100, 50))
        item.setBackground(1, QtGui.QColor(100, 0, 100, 50))
      else:
        item.setBackground(0, QtGui.QColor(255, 255, 255, 0))
        item.setBackground(1, QtGui.QColor(255, 255, 255, 0))
    self.tree.blockSignals(False)

  def progressBarFunc(self, Type):
    if Type == self.start_item:
      self.pb_value += self.pb_step
      if self.pb_value >= 99.6:
        self.progress.setValue(100)
        self.progress.setVisible(False)
      else:
        self.progress.setValue(self.pb_value)

  def itemRead(self, c_item, data):
    for _id, _dict in data:
      item_ = self.tree.add(c_item, _dict, ID=_id)
      if 'composition' in item_.data.keys():
        self.recursionRead(item_)
      self.progressBarFunc(_dict['type'])
    return item_

  def itemSave(self, c_item):
    c_item.data['title'] = VictoryNox.cl(str(c_item.text(0)))
    c_item.data['description'] = VictoryNox.cl(str(c_item.text(1)))
    if 'composition' in c_item.data.keys():
      c_item.data['composition'] = self.recursionSave(c_item)
    self.saveAndGetId(c_item)
    return c_item.id

  def recExport(self, i, filesDrop=False, pathDrop=False):
    item_list = []
    def func(i):
      if i.id > 0:
        data = dict(i.data)
        if filesDrop:
          data['files'] = []
        if pathDrop:
          data['path'] = []
        item_list.append([i.id, data])
      if i.childCount() > 0:
        for e in xrange(i.childCount()):
          func(i.child(e))
    func(i)
    return item_list

  def export_(self):
    f_dial = QtGui.QFileDialog()
    f_name = f_dial.getExistingDirectory(self, u'Экспорт...')
    for i in self.tree.selectedItems():
      title = str(self.windowTitle()) + '-' + i.data['title']
      item_list = self.recExport(i, filesDrop=True, pathDrop=True)
      json_data = {}
      json_data['export'] = item_list
      json_data['type'] = self.type
      json_data['id'] = i.id
      with open(u"{}/{}.{}".format(f_name, title, 'json'), "wb") as handle:
        handle.write(json.dumps(json_data))

  def import_(self):
    f_dial = QtGui.QFileDialog()
    f_name = f_dial.getOpenFileNames(self, u'Импорт...')
    self.tree.blockSignals(True)
    if len(f_name) > 0:
      for i in f_name:
        DATA = json.load(open(i, 'r'))
        self.DATA = DATA['export']
        tree_vals = VictoryNox.getData2(self.DATA, id_=DATA['id'])
        if DATA['type'] == self.type:
          if len(self.tree.selectedItems()) == 1:
            added_item = self.refreshDisp(tree_vals, self.tree.selectedItems()[0])
            self.tree.selectedItems()[0].changed = True
            self.freeUp(added_item)
            self.notSaved(added_item)
          else:
            added_item = self.refreshDisp(tree_vals)
            self.freeUp(added_item)
            self.notSaved(added_item)
        else:
          wt = i.split('-')[0]
          QtGui.QMessageBox.warning(
            self, u'Ошибка', u'Неверный файл...(')
    self.tree.blockSignals(False)

  def saveAndGetId(self, c_item):
    self.tree.blockSignals(True)
    if c_item.data['type'] != '':
      if c_item.id == 0:
        try:
          new_id = Server.addData(self.parent.auth, self.type, '', json.dumps(c_item.data, sort_keys=True))
          c_item.id = new_id
        except Exception as exp:
          message = u"Не удалось сохранить в базе: {} - {} ".format(c_item.data['type'],
                                                      c_item.data['title']), str(exp).encode()
          print message
          #self.parent.statusBar().showMessage(message)
      else:
        try:
          Server.setData(self.parent.auth, self.type, c_item.id, json.dumps(c_item.data, sort_keys=True))
        except Exception as exp:
          message = u"Не удалось сохранить в базе: {} - {} ".format(c_item.data['type'],
                                                      c_item.data['title']), exp
          print message
          #self.parent.statusBar().showMessage(message)
    else:
      QtGui.QMessageBox.warning(
        self, u'Ошибка', u'Не указан тип элемента')
    self.tree.blockSignals(False)

  def saveItems(self, repl=1):
    if repl == 1:
      reply = QtGui.QMessageBox.question(self, u'Внимание!',
          u'Сохранить ВСЕ изменения изделий?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if reply == QtGui.QMessageBox.Yes:
        self.rootSave()
      else:
        pass
    else:
      self.rootSave()
    self.refresh(True)

  def recursionSave(self, item):
    item_list = []
    for i in xrange(item.childCount()):
      c_item = item.child(i)
      _id = self.itemSave(c_item)
      item_list.append(_id)
    return item_list

  def recursionRead(self, item):
    for i in item.data['composition']:
      try:
        self.itemRead(item, VictoryNox.getData2(self.DATA, id_=i))
      except:
        item.data['composition'].remove(i)
        print u'Ups, We lost an item. id={}'.format(i)
        item.changed = True
        self.notSaved(item)

  def rootSave(self):
    self.pb_step = 100 / float(self.tree.topLevelItemCount())
    self.pb_value = 0
    self.progress.setValue(self.pb_value)
    self.start_item = str(self.type_filter.currentText())
    for i in xrange(self.tree.topLevelItemCount()):
      c_item = self.tree.topLevelItem(i)
      c_item.data['title'] = VictoryNox.cl(str(c_item.text(0)))
      c_item.data['description'] = VictoryNox.cl(str(c_item.text(1)))
      c_item.data['composition'] = self.recursionSave(c_item)
      self.saveAndGetId(c_item)
      self.progressBarFunc('root')

  def freeUp(self, item):
    item.id = 0
    item.changed = True
    #item.data['link'] = []
    if item.childCount() > 0:
      for i in xrange(item.childCount()):
        self.freeUp(item.child(i))

  def addItem(self):
    if len(self.tree.selectedItems()) == 1:
      c_item = self.tree.selectedItems()[0]
      #c_item.changed = True
    else:
      c_item = False

    if len(self.TYPES) != 0:
      if c_item:
        icon = ''
        Type = u'По умолчанию'
        #Type = ''
      else:
        icon = self.TYPEICONS[self.type_filter.currentIndex()]
        Type = unicode(self.type_filter.currentText())
    else:
      icon = ''
      Type = u'По умолчанию'
      #Type = ''

    data = {
           'type':Type,
           'typeIcon':icon,
           'title':u'Новый элемент',
           'description':'',
           'path':[],
           'composition':[],
           'params':[],
           'expand':1,
           }
    new_id = Server.addData(self.parent.auth, self.type, '', json.dumps(data))

    if c_item:
      self.tree.blockSignals(True)
      c_item.data['composition'].append(new_id)
      self.saveAndGetId(c_item)
      self.tree.blockSignals(False)

    self.tree.add(c_item, data, ID=new_id, expand=True, changed=True, edit=True)

