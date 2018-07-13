#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json, sip
import xmlrpclib
import time
from PyQt4 import QtCore, QtGui
from victorynox import VictoryNox
import icons
from cfg import Server
Server = Server()

class Threading(QtCore.QTimer):
  def __init__(self):
    super(Threading, self).__init__()
    self.ans = False
    self.timeout.connect(self.checker)
    self.start(500)
  def checker(self):
    try:
      self.domain_list = json.loads(Server.getDomains())
      if self.domain_list:
        self.ans = True
      else:
        self.ans = False
      self.start(500)
    except Exception, exp:
      self.ans = False
      self.start(500)
    print self.ans

class StartThread(QtCore.QThread):
  def __init__(self, parent):
    super(StartThread, self).__init__()
    self.parent = parent
  def __del__(self):
    self.wait()
  def run(self):
    A = Threading()

class MdiArea(QtGui.QMdiArea):
  def __init__(self):
    super(MdiArea, self).__init__()
    self.resize(500, 300)
    self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
  def addSubWin(self, widget):
    win = self.addSubWindow(SubWin(self, widget))
    win.setWindowTitle(widget.windowTitle())
    win.setWindowIcon(widget.windowIcon())
    win.showMaximized()

class SubWin(QtGui.QMdiSubWindow):
  def __init__(self, parent, widget):
    super(SubWin, self).__init__(parent)
    self.parent = parent
    self.setWidget(widget)
  def closeEvent(self, event):
    if self.widget().save_btn.isEnabled():
      reply = QtGui.QMessageBox.question(self, u'Внимание!',
          u'Отменить ВСЕ изменения и закрыть?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if reply == QtGui.QMessageBox.Yes:
        self.parent.removeSubWindow(self)
      else:
        event.ignore()
    else:
      self.parent.removeSubWindow(self)

class Widget(QtGui.QWidget):
  def __init__(self):
    super(Widget, self).__init__()

class Frame(QtGui.QFrame):
  def __init__(self):
    super(Frame, self).__init__()
    #self.setFrameShape(QtGui.QFrame.StyledPanel)
    #self.setFrameShadow(QtGui.QFrame.Plain)
    #self.setLineWidth(0)
    #self.setMidLineWidth(0)
    self.setObjectName("myObject")
    self.setStyleSheet("#myObject { border: 1px solid lightgrey; }")
    #self.setStyleSheet("#myObject { border: 1px solid lightblue; }")

class Splitter(QtGui.QSplitter):
  def __init__(self, o):
    super(Splitter, self).__init__()
    if o == 'h':
      self.setOrientation(QtCore.Qt.Horizontal)
    elif o == 'v':
      self.setOrientation(QtCore.Qt.Vertical)

class VLayout(QtGui.QVBoxLayout):
  def __init__(self):
    super(VLayout, self).__init__()

class HLayout(QtGui.QHBoxLayout):
  def __init__(self):
    super(HLayout, self).__init__()

class TreeWidget2(QtGui.QTreeWidget):
  def __init__(self, parent=None):
    super(TreeWidget2, self).__init__()
    self.parent = parent
    self.setRootIsDecorated(False)
    self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.setAlternatingRowColors(True)
    self.setHeaderLabels(QtCore.QStringList([u'Параметр', u'Значение']))
    self.header().resizeSection(0, 200)
    self.setStyle(QtGui.QStyleFactory.create('cleanlooks'))
    self.setStyleSheet(''' QTreeWidget::item:hover { background-color: none;}
                        QTreeWidget::item:selected { background-color: none;} ''')
    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)
    # actions
    self.addStrAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Bubble.png'), u"&Строка",
        self, statusTip=u"Строка", triggered=self.addStrParam)
    self.addTextAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Comment.png'), u"&Текст",
        self, statusTip=u"Текст", triggered=self.addTextParam)
    self.addDateAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Calendar.png'), u"&Дата",
        self, statusTip=u"Дата", triggered=self.addDateParam)
    self.addMenuAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Down.png'), u"&Меню",
        self, statusTip=u"Меню", triggered=self.addMenuParam)
    self.addIntAct = QtGui.QAction(u"&Целое число", self, statusTip=u"Целое число", triggered=self.addIntParam)
    self.addFloatAct = QtGui.QAction(u"&Число с плавающей точкой", self, statusTip=u"Число с плавающей точкой", triggered=self.addFloatParam)
    self.addLinkAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Sync.png'), u"&Ссылка",
        self, statusTip=u"Ссылка", triggered=self.addLinkParam)
    self.comboAddAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/plus.png'), u"&Добавить в меню",
        self, statusTip=u"Добавить новый элемент в меню", triggered=self.comboAdd)
    self.comboAddAct.setVisible(False)
    self.comboDelAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/minus.png'), u"&Удалить из меню",
        self, statusTip=u"Удалить выбранный элемент из меню", triggered=self.comboDel)
    self.comboDelAct.setVisible(False)
    self.delAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Delete.png'), u"&Удалить параметр",
        self, statusTip=u"Удалить параметр", triggered=self.delParam)
    self.copyAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Copy.png'), u"&Копировать",
        self, statusTip=u"Копировать выделенные параметры", triggered=self.copyParam)
    self.pasteAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Paste.png'), u"&Вставить",
        self, statusTip=u"Вставить скопированные параметры", triggered=self.pasteParam)
  def actRefresh(self):
    self.comboAddAct.setVisible(False)
    self.comboDelAct.setVisible(False)
    if len(self.selectedItems()) == 0:
      self.delAct.setEnabled(False)
      self.copyAct.setEnabled(False)
    elif len(self.selectedItems()) > 0:
      yes = True
      for i in self.selectedItems():
        if type(i.type) is not int:
          yes = False
      if yes:
        self.delAct.setEnabled(True)
        self.copyAct.setEnabled(True)
      else:
        self.delAct.setEnabled(False)
        self.copyAct.setEnabled(False)
      if len(self.selectedItems()) == 1:
        if self.selectedItems()[0].type1 == 'QComboBox':
          self.comboAddAct.setVisible(True)
          self.comboDelAct.setVisible(True)
    if self.parent.parent2.parent.ParamClipBoard:
      self.pasteAct.setEnabled(True)
    else:
      self.pasteAct.setEnabled(False)
  def openMenu(self, position):
    addMenu = QtGui.QMenu(u'Новый параметр')
    addMenu.addAction(self.addStrAct)
    addMenu.addAction(self.addTextAct)
    addMenu.addAction(self.addIntAct)
    addMenu.addAction(self.addFloatAct)
    addMenu.addAction(self.addDateAct)
    addMenu.addAction(self.addMenuAct)
    addMenu.addAction(self.addLinkAct)
    menu = QtGui.QMenu()
    menu.aboutToShow.connect(self.actRefresh)
    menu.addMenu(addMenu)
    menu.addAction(self.copyAct)
    menu.addAction(self.pasteAct)
    menu.addSeparator()
    menu.addAction(self.delAct)
    menu.addSeparator()
    menu.addAction(self.comboAddAct)
    menu.addAction(self.comboDelAct)
    menu.exec_(self.viewport().mapToGlobal(position))
  def comboAdd(self):
    self.selectedItems()[0].type2.setEditable(True)
    self.selectedItems()[0].type2.addItem(u'Новый элемент')
    #self.selectedItems()[0].type2.insertItem(0, u'Новый элемент')
    self.selectedItems()[0].type2.setCurrentIndex(self.selectedItems()[0].type2.count()-1)
  def comboDel(self):
    self.selectedItems()[0].type2.removeItem(self.selectedItems()[0].type2.currentIndex())
  def delParam(self):
    c_item = self.parent.parent2.tree.currentItem()
    id_list = []
    for i in self.selectedItems():
      id_list.append(i.type)
    for i in sorted(id_list, reverse=True):
      del c_item.data['params'][i]
    c_item.changed = True
    self.parent.parent2.tree.showClicked()
    self.parent.parent2.notSaved(c_item)
  def copyParam(self):
    copy = []
    for i in self.selectedItems():
      copy.append(self.parent.parent2.tree.currentItem().data['params'][self.indexOfTopLevelItem(i)])
    self.parent.parent2.parent.ParamClipBoard = copy
  def pasteParam(self):
    c_item = self.parent.parent2.tree.currentItem()
    for i in self.parent.parent2.parent.ParamClipBoard:
      c_item.data['params'].append(i)
    self.parent.parent2.tree.showClicked()
    c_item.changed = True
    self.parent.parent2.notSaved(c_item)
  def addStrParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['QLineEdit'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QLineEdit', '{}'.format(param_name), ''])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addTextParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['QTextEdit'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QTextEdit', '{}'.format(param_name), ''])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addDateParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['QDateEdit'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QDateEdit', '{}'.format(param_name), ''])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addMenuParam(self, title):
    ok, param_name, vals = ParamDialog(self).comboParam(self.parent.parent2.PARAMS['QComboBox'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QComboBox', '{}'.format(param_name), vals[0]])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addIntParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['QSpinBox'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QSpinBox', '{}'.format(param_name), 0])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addFloatParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['QDoubleSpinBox'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['QDoubleSpinBox', '{}'.format(param_name), 0])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)
  def addLinkParam(self, title):
    ok, param_name = ParamDialog(self).paramEdit(self.parent.parent2.PARAMS['Link'])
    if ok:
      c_item = self.parent.parent2.tree.currentItem()
      c_item.data['params'].append(['Link', '{}'.format(param_name), []])
      self.parent.parent2.tree.showClicked()
      c_item.changed = True
      self.parent.parent2.notSaved(c_item)

class ParamDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(ParamDialog, self).__init__()
    self.parent = parent
    self.setWindowTitle(u'Выберите название параметра')
    self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
    self.setMinimumSize(300, 0)
    self.setMaximumSize(500, 0)
    self.buttons = QtGui.QDialogButtonBox(
      QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
      QtCore.Qt.Horizontal, self)
    self.buttons.accepted.connect(self.accept)
    self.buttons.rejected.connect(self.reject)
    self.layout = QtGui.QVBoxLayout(self)
  def paramEdit(self, params):
    combo = QtGui.QComboBox()
    combo.setEditable(True)
    combo.addItems(params)
    combo.insertItem(0, '')
    combo.setCurrentIndex(0)
    self.layout.addWidget(combo)
    self.layout.addWidget(self.buttons)
    combo.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    result = self.exec_()
    return (result == QtGui.QDialog.Accepted,
            unicode(combo.currentText().split(' => ')[0]))
  def comboParam(self, params):
    combo = QtGui.QComboBox()
    combo.setEditable(True)
    combo.setInsertPolicy(0)
    vals = []
    for i in params:
      combo.addItem(i[0])
      vals.append(i[1])
    combo.insertItem(0, '')
    vals.insert(0, [[],0])
    combo.setCurrentIndex(0)
    self.layout.addWidget(combo)
    self.layout.addWidget(self.buttons)
    combo.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    result = self.exec_()
    return (result == QtGui.QDialog.Accepted,
            unicode(combo.currentText().split(' => ')[0]),
          [vals[combo.currentIndex()], combo.currentIndex()])

class TypeEditor(QtGui.QDialog):
  def __init__(self, dialType, dialTitle, dialIcon, parent=None):
    super(TypeEditor, self).__init__()
    self.parent = parent
    self.setWindowTitle(u'Параметры выбранного типа')
    self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
    self.comboMetaType = TypeEditorComboBox([u'Изделия', u'Экземпляры'])
    self.comboType = TypeEditorComboBox([u'ТКО', u'Стойка'])
    self.layout = QtGui.QVBoxLayout(self)
    self.layout.addWidget(self.comboMetaType)
    self.layout.addWidget(self.comboType)

class TypeEditorComboBox(QtGui.QComboBox):
  def __init__(self, vals, parent=None):
    super(TypeEditorComboBox, self).__init__()
    self.parent = parent
    #self.setEditable(True)
    #self.setInsertPolicy(0)
    #self.currentIndexChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.blockSignals(True)
    #self.addItems(v[2][0])
    self.addItems(vals)
    #self.setCurrentIndex(v[2][1])
    self.blockSignals(False)

class TypeDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(TypeDialog, self).__init__()
    self.parent = parent
    self.setWindowTitle(u'Параметры выбранного типа')
    self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
    self.setMinimumSize(300, 0)
    self.setMaximumSize(500, 0)
    self.buttons = QtGui.QDialogButtonBox(
      QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
      QtCore.Qt.Horizontal, self)
    self.buttons.accepted.connect(self.accept)
    self.buttons.rejected.connect(self.reject)
    self.layout = QtGui.QVBoxLayout(self)
    self.layout2 = QtGui.QHBoxLayout()
  def typeEdit(self, name, c_icon):
    icons = QtGui.QComboBox()
    icon_list = []
    for i in xrange(0, 33):
      icon = ':/icons/icons/{}.png'.format(i)
      icon_list.append(icon)
      icons.addItem(QtGui.QIcon(icon), '')
    if c_icon != '':
      icons.setCurrentIndex(icon_list.index(c_icon))
    line = QtGui.QLineEdit()
    line.setText(unicode(name))
    self.layout2.addWidget(icons)
    self.layout2.addWidget(line)
    self.layout.addLayout(self.layout2)
    self.layout.addWidget(self.buttons)
    result = self.exec_()
    return (result == QtGui.QDialog.Accepted,
            unicode(line.text()),
            icon_list[icons.currentIndex()])

class TreeWidget(QtGui.QTreeWidget):
  def __init__(self, parent=None):
    super(TreeWidget, self).__init__()
    self.parent = parent
    self.setAlternatingRowColors(True)
    self.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
    # bold text
    self.bold = QtGui.QFont()
    self.bold.setBold(True)
    self.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)
    self.setSortingEnabled(True)
    self.sortItems(0, QtCore.Qt.AscendingOrder)
    self.setColumnCount(2)
    self.setHeaderLabels(QtCore.QStringList([u'Наименование', u'Описание']))
    self.header().resizeSection(0, 250)
    #self.header().resizeSection(1, 100)
    self.setStyle(QtGui.QStyleFactory.create('cleanlooks'))
    self.setStyleSheet(''' QTreeWidget::item:hover { background-color: #e0e0e0;}
                            QTreeWidget::item:selected { background-color: none;} ''')
    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)
    self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.itemSelectionChanged.connect(self.showClicked)
    self.itemChanged.connect(self.editFinished)
    self.itemExpanded.connect(self.expanded)
    self.itemCollapsed.connect(self.collapsed)
    # actions
    self.addAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Create.png'), u"&Добавить",
        self, statusTip=u"Добавить", triggered=parent.addItem)
    self.delAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Delete.png'), u"&Удалить",
        self, statusTip=u"Удалить", triggered=lambda: parent.delItem(self.selectedItems()))
    self.copyAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Copy.png'), u"&Копировать",
        self, statusTip=u"Копировать", triggered=self.copyItem)
    self.cutAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Cut.png'), u"&Переместить",
        self, statusTip=u"Переместить", triggered=self.cutItem)
    self.pasteAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Paste.png'), u"&Вставить",
        self, statusTip=u"Вставить", triggered=self.pasteItem)
    self.copyLinkAct = QtGui.QAction(u"&Копировать ссылку",
        self, statusTip=u"Копировать ссылки на выделенные элементы", triggered=self.copyLinks)
    self.goToThisTypeAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/filter.png'), u"&Показать все",
        self, statusTip=u"Показать все элементы данного типа", triggered=self.toThisType)
    self.pasteAct.setEnabled(False)
  def toThisType(self):
    item = self.selectedItems()[0]
    self.parent.type_filter.setCurrentIndex(self.parent.type_filter.findText(item.data['type']))
  def expanded(self, item):
    self.blockSignals(True)
    item.data['expand'] = 1
    self.blockSignals(False)
    self.parent.notSaved(item)
  def collapsed(self, item):
    self.blockSignals(True)
    item.data['expand'] = 0
    self.blockSignals(False)
    self.parent.notSaved(item)
  def copyLinks(self):
    copy_data = []
    for i in self.parent.tree.selectedItems():
      item_data = [i.data['type'], i.data['typeIcon'], unicode(i.data['title']), unicode(i.data['description'])]
      copy_data.append([self.parent.type, i.id, item_data])
    self.parent.parent.LinkClipBoard = copy_data
  def copyItem(self):
    copy_data = []
    for i in self.parent.tree.selectedItems():
      item_list = self.parent.recExport(i, filesDrop=True, pathDrop=True)
      data = {}
      data['copy'] = item_list
      data['type'] = self.parent.type
      data['id'] = i.id
      copy_data.append(data)
    self.parent.parent.ClipBoard = copy_data
    self.parent.parent.COPY = True
    self.pasteAct.setEnabled(True)
  def cutItem(self):
    copy_data = []
    for i in self.parent.tree.selectedItems():
      item_list = self.parent.recExport(i, pathDrop=True)
      data = {}
      data['copy'] = item_list
      data['type'] = self.parent.type
      data['id'] = i.id
      copy_data.append(data)
      for e in self.parent.DATA:
        ID, DATA = e
        if i.id in DATA['composition']:
          DATA['composition'].remove(i.id)
          Server.setData(self.parent.parent.auth, self.parent.type, ID, json.dumps(DATA))
      try:
        i.parent().data['composition'].remove(i.id)
        i.parent().changed = True
      except:
        pass
      sip.delete(i)
    self.parent.parent.ClipBoard = copy_data
    self.parent.parent.COPY = False
    self.pasteAct.setEnabled(True)
  def pasteItem(self):
    if len(self.parent.tree.selectedItems()) == 1:
      c_item = self.parent.tree.selectedItems()[0]
    else:
      c_item = False
    self.blockSignals(True)
    for cb in self.parent.parent.ClipBoard:
      self.parent.DATA = cb['copy']
      tree_vals = VictoryNox.getData2(cb['copy'], id_=cb['id'])
      if len(self.parent.tree.selectedItems()) == 1:
        added_item = self.parent.refreshDisp(tree_vals, c_item)
        if self.parent.parent.COPY:
          self.parent.freeUp(added_item)
        self.parent.notSaved(added_item)
        c_item.changed = True
        c_item.data['composition'].append(added_item.id)
        self.parent.notSaved(c_item)
      else:
        added_item = self.parent.refreshDisp(tree_vals)
        if self.parent.parent.COPY:
          self.parent.freeUp(added_item)
        self.parent.notSaved(added_item)
    if not self.parent.parent.COPY:
      self.parent.parent.ClipBoard = False
      self.pasteAct.setEnabled(False)
    self.blockSignals(False)
  def editFinished(self, item):
    self.blockSignals(True)
    item.changed = True
    item.data['title'] = VictoryNox.cl(str(item.text(0)))
    item.data['description'] = VictoryNox.cl(str(item.text(1)))
    self.blockSignals(False)
    self.parent.notSaved(item)
  def actRefresh(self):
    if len(self.selectedItems()) == 0:
      self.delAct.setEnabled(False)
      self.copyAct.setEnabled(False)
      self.cutAct.setEnabled(False)
      self.copyLinkAct.setEnabled(False)
      self.goToThisTypeAct.setEnabled(False)
    elif len(self.selectedItems()) == 1:
      self.delAct.setEnabled(True)
      self.copyAct.setEnabled(True)
      self.cutAct.setEnabled(True)
      self.copyLinkAct.setEnabled(True)
      self.goToThisTypeAct.setEnabled(True)
    else:
      self.delAct.setEnabled(True)
      self.copyAct.setEnabled(True)
      self.cutAct.setEnabled(True)
      self.copyLinkAct.setEnabled(True)
      self.goToThisTypeAct.setEnabled(False)
    if self.parent.parent.ClipBoard:
      self.pasteAct.setEnabled(True)
    else:
      self.pasteAct.setEnabled(False)
  def openMenu(self, position):
    menu = QtGui.QMenu()
    menu.aboutToShow.connect(self.actRefresh)
    menu.aboutToShow.connect(self.parent.parent.updateFileMenu)
    menu.addAction(self.goToThisTypeAct)
    menu.addSeparator()
    menu.addAction(self.addAct)
    menu.addSeparator()
    menu.addAction(self.copyAct)
    menu.addAction(self.cutAct)
    menu.addAction(self.pasteAct)
    menu.addSeparator()
    menu.addAction(self.delAct)
    menu.addSeparator()
    menu.addAction(self.copyLinkAct)
    menu.addSeparator()
    menu.addAction(self.parent.parent.exportAct)
    menu.addAction(self.parent.parent.importAct)
    menu.exec_(self.viewport().mapToGlobal(position))
  def showClicked(self):
    self.parent.info_forma_frame.setEnabled(False)
    self.parent.info_forma_frame.titleLab.setText(u'')
    self.parent.info_forma.clear()
    self.parent.info_forma_frame.pathLine.clear()
    self.parent.info_forma_frame.typeCombo.blockSignals(True)
    self.parent.info_forma_frame.typeCombo.clear()
    self.parent.info_forma_frame.typeCombo.blockSignals(False)
    if len(self.selectedItems()) == 1:
      self.parent.info_forma_frame.setEnabled(True)
      self.parent.info_forma.clear()
      c_item = self.selectedItems()[0]
      self.parent.info_forma_frame.manager()
  def add(self, c_item, data, ID=0, changed=False, edit=False, expand=False):
    self.blockSignals(True)
    if c_item:
      item = QtGui.QTreeWidgetItem(c_item)
      if expand:
        self.expandItem(c_item)
    else:
      item = QtGui.QTreeWidgetItem(self)
    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
    item.type = data['type']
    item.changed = changed
    item.id = ID
    item.data = data
    if data['typeIcon'] != '':
      item.setIcon(0, QtGui.QIcon(data['typeIcon']))
    item.setText(0, unicode(data['title']))
    item.setToolTip(0, VictoryNox.ttCut(unicode(item.text(0))))
    item.setText(1, unicode(data['description']))
    item.setToolTip(1, VictoryNox.ttCut(unicode(item.text(1))))
    if len(item.data['path']) == 0:
      if c_item:
        item.data['path'] = list(c_item.data['path'])
        item.data['path'].append(ID)
      else:
        item.data['path'] = [ID]
    item.setFont(0, self.bold)
    if data['expand']:
      self.expandItem(item)
    if edit:
      self.editItem(item, 0)
    self.blockSignals(False)
    return item
  def getFullItemPath(self, item):
    path = []
    while item is not None:
      path.append(item.id)
      item = item.parent()
    return list(reversed(path))

class PushButton(QtGui.QPushButton):
  def __init__(self):
    super(PushButton, self).__init__()
    self.setIcon(QtGui.QIcon(':/icons/icons/Create.png'))
    self.setToolTip(u'<b>Добавить</b>')

class TableWidget(QtGui.QTableWidget):
  def __init__(self, parent=None):
    super(TableWidget, self).__init__()
    self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
    self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.verticalHeader().setVisible(False)
    self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
  def contract(self):
    self.setColumnCount(3)
    self.setHorizontalHeaderLabels(['', u'Номер контракта', u'Наименование'])
  def partner(self):
    self.setColumnCount(4)
    self.setHorizontalHeaderLabels(['', u'Наименование', u'Электронная почта', u'Телефон'])
  def location(self):
    self.setColumnCount(5)
    self.setHorizontalHeaderLabels(['',
                                  u'Населенный пункт',
                                  u'Наименование',
                                  u'Условный номер',
                                  u'Ведомство'])
  def link(self):
    self.setColumnCount(3)
    self.horizontalHeader().setVisible(False)

class LineEdit(QtGui.QLineEdit):
  def __init__(self, v, parent=None):
    super(LineEdit, self).__init__()
    self.parent = parent
    reg_ex = QtCore.QRegExp(u"[а-яА-Яa-zA-Z0-9 -_.()\",/@]+")
    _validator = QtGui.QRegExpValidator(reg_ex, self)
    self.setValidator(_validator)
    #self.textEdited.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    #self.blockSignals(True)
    self.setText(u"{}".format(v[2]))
    self.setToolTip(VictoryNox.ttCut(v[2]))
    #self.blockSignals(False)
    self.editingFinished.connect(lambda: self.parent.formChanged(self, v[0], v[1]))

class TextEdit(QtGui.QTextEdit):
  def __init__(self, v, parent=None):
    super(TextEdit, self).__init__()
    self.parent = parent
    self.v = v
    #self.textChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.setMaximumHeight(70)
    self.blockSignals(True)
    self.setText(u"{}".format(v[2]))
    self.setToolTip(VictoryNox.ttCut(v[2]))
    self.blockSignals(False)
  def focusOutEvent(self, event):
    self.parent.formChanged(self, self.v[0], self.v[1])

class DateEdit(QtGui.QDateEdit):
  def __init__(self, v, parent=None):
    super(DateEdit, self).__init__()
    self.parent = parent
    self.setCalendarPopup(True)
    self.calendarWidget().setFirstDayOfWeek(QtCore.Qt.Monday)
    self.dateChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    cur_date = v[2].split('.')
    if len(cur_date) > 2:
      self.blockSignals(True)
      self.setDate(QtCore.QDate(int(cur_date[0]), int(cur_date[1]), int(cur_date[2])))
      self.blockSignals(False)

class SpinBox(QtGui.QSpinBox):
  def __init__(self, v, parent=None):
    super(SpinBox, self).__init__()
    self.parent = parent
    #self.setMaximum(9999)
    #self.setMinimum(0)
    self.valueChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.blockSignals(True)
    self.setValue(v[2])
    self.blockSignals(False)

class DoubleSpinBox(QtGui.QDoubleSpinBox):
  def __init__(self, v, parent=None):
    super(DoubleSpinBox, self).__init__()
    self.parent = parent
    self.valueChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.blockSignals(True)
    self.setValue(v[2])
    self.blockSignals(False)

class ComboBox(QtGui.QComboBox):
  def __init__(self, v, parent=None):
    super(ComboBox, self).__init__()
    self.parent = parent
    #self.setEditable(True)
    self.setInsertPolicy(0)
    self.currentIndexChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    #self.editTextChanged.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.blockSignals(True)
    self.addItems(v[2][0])
    self.setCurrentIndex(v[2][1])
    if self.count() > 0:
      self.setEditable(True)
      self.lineEdit().editingFinished.connect(lambda: self.parent.formChanged(self, v[0], v[1]))
    self.blockSignals(False)

class Link(QtGui.QTableWidget):
  def __init__(self, v, parent=None):
    super(Link, self).__init__()
    self.parent = parent
    self.data = v
    self.setMaximumHeight(130)
    self.setAlternatingRowColors(True)
    self.setSortingEnabled(True)
    self.sortItems(0, QtCore.Qt.AscendingOrder)
    self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)
    #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.verticalHeader().setVisible(False)
    self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.setColumnCount(4)
    self.setHorizontalHeaderLabels([u'Средство', u'Тип', u'Наименование', u'Описание'])
    #self.itemChanged.connect(lambda: self.parent.formChanged(self, self.data[0], self.data[1]))
    # actions
    self.pasteAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Paste.png'), u"&Вставить",
        self, statusTip=u"Вставить скопированные ссылки", triggered=self.pasteLink)
    self.delAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Delete.png'), u"&Удалить",
        self, statusTip=u"Удалить выделенные ссылки", triggered=self.delLink)
    self.goAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Down.png'), u"&Перейти",
        self, statusTip=u"Перейти по ссылке", triggered=self.goLink)
    self.refreshAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Refresh.png'), u"&Обновить",
        self, statusTip=u"Обновить данные ссылок", triggered=self.refreshLink)
    #self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
    self.loadLink()
  def resizeNow(self):
    self.resizeColumnsToContents()
    self.resizeRowsToContents()
    self.setFixedSize(
      self.horizontalHeader().length()+self.verticalHeader().width()+2,
      self.verticalHeader().length()+self.horizontalHeader().height()+2)
  def actRefresh(self):
    if len(self.selectedItems()) == 0:
      self.goAct.setEnabled(False)
      self.delAct.setEnabled(False)
    elif len(self.selectedItems()) == 4:
      self.goAct.setEnabled(True)
      self.delAct.setEnabled(True)
    else:
      self.goAct.setEnabled(False)
      self.delAct.setEnabled(True)
    if self.parent.parent2.parent.LinkClipBoard:
      self.pasteAct.setEnabled(True)
    else:
      self.pasteAct.setEnabled(False)
  def openMenu(self, position):
    menu = QtGui.QMenu()
    menu.aboutToShow.connect(self.actRefresh)
    menu.addAction(self.goAct)
    menu.addAction(self.pasteAct)
    menu.addAction(self.refreshAct)
    menu.addSeparator()
    menu.addAction(self.delAct)
    menu.exec_(self.viewport().mapToGlobal(position))
  def loadLink(self):
    self.blockSignals(True)
    self.setRowCount(0)
    for i in reversed(self.data[2]):
      item1 = QtGui.QTableWidgetItem(i[0]) #средство
      #item1.setIcon(QtGui.QIcon(i[2][1])) #icon средства
      item2 = QtGui.QTableWidgetItem(i[2][0]) #type
      item2.setIcon(QtGui.QIcon(i[2][1])) #icon
      item2.link = i
      item3 = QtGui.QTableWidgetItem(i[2][2]) #title
      item4 = QtGui.QTableWidgetItem(i[2][3]) #description
      self.insertRow(0)
      self.setItem(0, 0, item1)
      self.setItem(0, 1, item2)
      self.setItem(0, 2, item3)
      self.setItem(0, 3, item4)
    self.blockSignals(False)
  def pasteLink(self):
    for i in self.parent.parent2.parent.LinkClipBoard:
      self.data[2].append(i)
    self.parent.formChanged(self, self.data[0], self.data[1])
    self.loadLink()
  def delLink(self):
    for i in self.selectedItems():
      if i.column() == 0:
        del self.data[2][i.row()]
    self.parent.formChanged(self, self.data[0], self.data[1])
    self.loadLink()
  def goLink(self):
    linkTo = self.selectedItems()[1].link
    self.parent.parent2.parent.openWindow(linkTo[0])
    widget = self.parent.parent2.parent.mdiArea.activeSubWindow().widget()
    widget.type_filter.setCurrentIndex(widget.TYPES.index(linkTo[2][0]))
    widget.showLink(linkTo[1])
  def refreshLink(self):
    refresh_data = []
    for i in self.data[2]:
      data = VictoryNox.getData(self.parent.parent2.parent.auth, i[0], i[1])
      if data:
        data = data[0][1]
        refresh_link = [i[0], i[1], [data['type'], data['typeIcon'], data['title'], data['description']]]
        refresh_data.append(refresh_link)
    self.data[2] = refresh_data
    self.parent.parent2.tree.blockSignals(True)
    c_item = self.parent.parent2.tree.currentItem()
    c_item.changed = True
    self.parent.parent2.tree.blockSignals(False)
    self.parent.formChanged(self, self.data[0], self.data[1])
    self.parent.parent2.notSaved(c_item)
    self.loadLink()

class Files(QtGui.QTableWidget):
  def __init__(self, parent=None):
    super(Files, self).__init__()
    self.parent = parent
    self.setAlternatingRowColors(True)
    self.setSortingEnabled(True)
    self.sortItems(0, QtCore.Qt.AscendingOrder)
    self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)
    self.verticalHeader().setVisible(False)
    self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.setColumnCount(4)
    self.setHorizontalHeaderLabels([u'Имя', u'Дата изменения', u'Тип', u'Размер (КБ)'])
    # actions
    self.uploadFileAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Create.png'), u"&Добавить",
        self, statusTip=u"Добавить новый файл", triggered=self.uploadFile)
    self.downloadFileAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Download.png'), u"&Сохранить",
        self, statusTip=u"Сохранить выделенные файлы (скачать)", triggered=self.downloadFile)
    #self.copyFileAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Copy.png'), u"&Копировать",
    #    self, statusTip=u"Копировать выделенные файлы", triggered=self.copyFile)
    #self.pasteFileAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Paste.png'), u"&Вставить",
    #    self, statusTip=u"Вставить скопированные файлы", triggered=self.pasteFile)
    self.delFileAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Delete.png'), u"&Удалить",
        self, statusTip=u"Удалить выделенные файлы", triggered=self.delFile)
  def actRefresh(self):
    if len(self.selectedItems()) == 0:
      self.downloadFileAct.setEnabled(False)
      #self.copyFileAct.setEnabled(False)
      self.delFileAct.setEnabled(False)
    else:
      self.downloadFileAct.setEnabled(True)
      #self.copyFileAct.setEnabled(True)
      self.delFileAct.setEnabled(True)
    #if self.parent.parent2.parent.FileClipBoard:
    #  self.pasteFileAct.setEnabled(True)
    #else:
    #  self.pasteFileAct.setEnabled(False)
  def openMenu(self, position):
    menu = QtGui.QMenu()
    menu.aboutToShow.connect(self.actRefresh)
    menu.addAction(self.uploadFileAct)
    menu.addAction(self.downloadFileAct)
    #menu.addAction(self.copyFileAct)
    #menu.addAction(self.pasteFileAct)
    menu.addSeparator()
    menu.addAction(self.delFileAct)
    menu.exec_(self.viewport().mapToGlobal(position))
  def icons(self, f_type):
    if f_type == 'doc' or f_type == 'docx':
      return ':/icons/icons/doc.png'
    elif f_type == 'pdf':
      return ':/icons/icons/pdf.png'
    elif f_type == 'xls' or f_type == 'xlsx':
      return ':/icons/icons/excel.png'
    elif f_type == 'txt':
      return ':/icons/icons/text-plain.png'
    elif f_type == 'py':
      return ':/icons/icons/python.png'
    elif f_type == 'zip' or f_type == 'rar':
      return ':/icons/icons/rar.png'
    else:
      return ':/icons/icons/How-to.png'
  def loadFile(self):
    c_item = self.parent.parent2.tree.currentItem()
    self.setRowCount(0)
    self.blockSignals(True)
    try:
      file_info = json.loads(Server.infFile(self.parent.parent2.parent.auth, json.dumps({"dataType": self.parent.parent2.type, "dataID":c_item.id})))
    except Exception, exp:
      file_info = False
    if file_info:
      for f_id, f_data in file_info:
        item1 = QtGui.QTableWidgetItem(f_data['name'])
        item1.setIcon(QtGui.QIcon(self.icons(f_data['type'])))
        item1.id = f_id
        item1.type = f_data['type']
        m_time = time.strftime("%d.%m.%Y %H:%M:%S",time.localtime(f_data['modified']))
        item2 = QtGui.QTableWidgetItem(m_time)
        item3 = QtGui.QTableWidgetItem(f_data['type'])
        item4 = QtGui.QTableWidgetItem()
        item4.setData(QtCore.Qt.EditRole, f_data['size']/1000)
        self.insertRow(0)
        self.setItem(0, 0, item1)
        self.setItem(0, 1, item2)
        self.setItem(0, 2, item3)
        self.setItem(0, 3, item4)
    self.blockSignals(False)
  def uploadFile(self):
    c_item = self.parent.parent2.tree.currentItem()
    f_dial = QtGui.QFileDialog()
    file_names = f_dial.getOpenFileNames(self, u'Добавить файл...', '/')
    if len(file_names) > 0:
      for f_path in file_names:
        f_path = unicode(f_path)
        #filename, file_extension = os.path.splitext('/path/to/somefile.ext')
        f_name, f_type = self.nameType(f_path)
        modified = os.stat(f_path).st_mtime
        #f_size = os.stat(f_path).st_size
        #f_added = str(QtCore.QDateTime.currentDateTime().toString('yyyy.MM.dd.HH.mm.ss'))
        #file_data = {'name':f_name, 'type':f_type, 'path':f_path, 'modified':modified, 'size':f_size, 'added':f_added}
        file_data = {'name':f_name, 'type':f_type, 'path':f_path, 'modified':modified}
        with open(f_path, "rb") as handle:
          bin_file_data = xmlrpclib.Binary(handle.read())
        f_id = Server.addFile(self.parent.parent2.parent.auth, self.parent.parent2.type, c_item.id, bin_file_data, json.dumps(file_data))
    c_item.changed = True
    self.parent.parent2.notSaved(c_item)
    self.loadFile()
  def nameType(self, f_path):
    F1 = f_path.split('.')
    F2 = ''
    for i in F1[:-1]:
      F2 = F2+i+'.'
    if sys.platform == 'win32':
      F3 = F2.split('\\')
    else:
      F3 = F2.split('/')
    F4 = F3[-1]+F1[-1]
    f_name = F3[-1][:-1]
    f_type = F1[-1]
    return (f_name, f_type)
  def downloadFile(self):
    f_dial = QtGui.QFileDialog()
    folder = f_dial.getExistingDirectory(self, u'Сохранить файлы в папку...')
    for i in self.selectedItems():
      if i.column() == 0:
        title = u'{}.{}'.format(unicode(i.text()), i.type)
        bFile = Server.getFile(self.parent.parent2.parent.auth, i.id)
        with open(u"{}/{}".format(folder, title), "wb") as handle:
          handle.write(bFile.data)
  def copyFile(self):
    pass
  def pasteFile(self):
    pass
  def delFile(self):
    c_item = self.parent.parent2.tree.currentItem()
    for i in self.selectedItems():
      if i.column() == 0:
        Server.delFile(self.parent.parent2.parent.auth, i.id)
    self.parent.parent2.notSaved(c_item)
    self.loadFile()

