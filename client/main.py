#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

from PyQt4 import QtCore, QtGui
import icons
import xmlrpclib
from passlib.hash import lmhash, nthash
from datetime import datetime
import time
import threading

from gui import MdiArea, StartThread, TypeEditor
from terminal import Terminal

from basic import Basic

from cfg import Server
Server = Server()

class Login(QtGui.QDialog):
  def __init__(self, parent=None):
    super(Login, self).__init__(parent)
    self.setFixedSize(200, 170)
    self.setWindowTitle(u'Авторизация')
    self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
    self.setWindowIcon(QtGui.QIcon(':/icons/icons/Key.png'))
    self.lab = QtGui.QLabel(self)
    self.lab.setText(u'Ваш домен:')
    self.combo = QtGui.QComboBox(self)
    self.textName = QtGui.QLineEdit(self)
    self.textName.setPlaceholderText(u'Логин')
    self.textName.setText(u'root')
    self.textPass = QtGui.QLineEdit(self)
    self.textPass.setEchoMode(QtGui.QLineEdit.Password)
    self.textPass.setPlaceholderText(u'Пароль')
    self.textPass.setText(u'12345678')
    self.buttonLogin = QtGui.QPushButton(u'Войти', self)
    self.buttonLogin.clicked.connect(self.handleLogin)

    layout2 = QtGui.QHBoxLayout()
    layout2.addStretch(1)
    layout2.addWidget(self.buttonLogin)
    layout2.addStretch(1)

    layout = QtGui.QVBoxLayout(self)
    layout.addWidget(self.lab)
    layout.addWidget(self.combo)
    layout.addStretch(1)
    layout.addWidget(self.textName)
    layout.addWidget(self.textPass)
    layout.addSpacing(10)
    layout.addLayout(layout2)
    self.try_num = 1

    # timer
    self.ans = 'start'
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.check_thread)
    self.timer.timeout.connect(self.indicator)
    self.timer.start(500)
    self.combo.setEnabled(False)
    self.buttonLogin.setEnabled(False)

  def checker(self, t):
    try:
      self.domain_list = json.loads(Server.getDomains())
      if self.domain_list:
        self.ans = 'ok'
      else:
        self.ans = 'not_ok'
    except Exception, exp:
      self.ans = 'not_ok'
    time.sleep(t)

  def check_thread(self):
    D = threading.Thread(target=self.checker, args=(1,))
    D.deamon = True
    D.start()

  def indicator(self):
    if self.ans == 'ok':
      self.combo.setEnabled(True)
      self.buttonLogin.setEnabled(True)
      self.local_name = u'Локальный пользователь'
      self.domain_list.insert(0, self.local_name)
      self.combo.addItems(self.domain_list)
      self.timer.stop()
      #print "Connected to server"
    elif self.ans == 'not_ok':
      self.combo.setEnabled(False)
      self.buttonLogin.setEnabled(False)
      self.timer.start(10000)
      #print "Server unavailable"
    elif self.ans == 'start':
      pass

  def handleLogin(self):
    login = unicode(self.textName.text())
    password = str(self.textPass.text())
    pass_hash = lmhash.hash(password)+':'+nthash.hash(password)
    if unicode(self.combo.currentText()) == self.local_name:
      self.auth = login, pass_hash
    else:
      domain = unicode(self.combo.currentText())
      self.auth = login, pass_hash, domain
    try:
      Server.getAuth(self.auth)
      self.accept()
    except xmlrpclib.Fault, exp:
      print exp.faultString
      QtGui.QMessageBox.warning(
        self, u'Ошибка', u'Неправильный логин или пароль\n\nПопытка №{}'.format(self.try_num))
      self.try_num += 1

class MainWindow(QtGui.QMainWindow):
  def __init__(self, auth):
    super(MainWindow, self).__init__()

    self.auth = auth

    self.ClipBoard = False
    self.LinkClipBoard = False
    self.ParamClipBoard = False
    #self.FileClipBoard = False

    self.setWindowIcon(QtGui.QIcon(':/icons/icons/gorynych.png'))
    self.setWindowTitle(u'Клиент ПК "Горыныч"')

    self.mdiArea = MdiArea()
    self.mdiArea.subWindowActivated.connect(self.updateMenus)
    self.setCentralWidget(self.mdiArea)

    self.windowMapper = QtCore.QSignalMapper(self)
    self.windowMapper.mapped[QtGui.QWidget].connect(self.setActiveSubWindow)

    self.progress = QtGui.QProgressBar()
    self.progress.setStyleSheet('''QProgressBar::chunk {background-color: lightgrey;}
                                          QProgressBar{text-align: center}''')
    self.progress.setMaximumSize(100, 16)
    self.progress.setVisible(False)

    self.createActions()
    self.createMenus()
    self.createStatusBar()
    self.updateMenus()

    self.readSettings()

  def closeEvent(self, event):
    unsaved = []
    for win in self.mdiArea.subWindowList():
      if win.widget().save_btn.isEnabled():
        unsaved.append(win)
    if len(unsaved) == 0:
      self.writeSettings()
      event.accept()
    else:
      reply = QtGui.QMessageBox.question(self, u'Внимание!',
          u'Отменить ВСЕ изменения и выйти?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if reply == QtGui.QMessageBox.Yes:
        self.writeSettings()
        event.accept()
      else:
        event.ignore()

  def about(self):
    QtGui.QMessageBox.about(self, u'О программе',
        u'ПК "Система учетно-документального сопровождения продукции '
        u'находящейся в технической эксплуатации" (шифр - "Горыныч")')

  def updateMenus(self):
    hasMdiChild = (self.activeMdiChild() is not None)
    self.closeAct.setEnabled(hasMdiChild)
    self.closeAllAct.setEnabled(hasMdiChild)
    self.tileAct.setEnabled(hasMdiChild)
    self.cascadeAct.setEnabled(hasMdiChild)
    self.nextAct.setEnabled(hasMdiChild)
    self.previousAct.setEnabled(hasMdiChild)
    self.separatorAct.setVisible(hasMdiChild)

  def updateFileMenu(self):
    windows = self.mdiArea.subWindowList()
    self.importAct.setVisible(len(windows) != 0)
    self.exportAct.setVisible(len(windows) != 0)
    if len(windows) != 0:
      if len(self.mdiArea.activeSubWindow().widget().tree.selectedItems()) == 0:
        self.exportAct.setEnabled(False)
        self.importAct.setEnabled(True)
      elif len(self.mdiArea.activeSubWindow().widget().tree.selectedItems()) == 1:
        if self.mdiArea.activeSubWindow().widget().tree.selectedItems()[0].id != 0:
          self.exportAct.setEnabled(True)
          self.importAct.setEnabled(True)
        else:
          self.exportAct.setEnabled(False)
          self.importAct.setEnabled(False)
      else:
        self.exportAct.setEnabled(True)
        self.importAct.setEnabled(False)

  def updateWindowMenu(self):
    self.windowMenu.clear()
    self.windowMenu.addAction(self.closeAct)
    self.windowMenu.addAction(self.closeAllAct)
    self.windowMenu.addSeparator()
    self.windowMenu.addAction(self.tileAct)
    self.windowMenu.addAction(self.cascadeAct)
    self.windowMenu.addSeparator()
    self.windowMenu.addAction(self.nextAct)
    self.windowMenu.addAction(self.previousAct)
    self.windowMenu.addAction(self.separatorAct)

    windows = self.mdiArea.subWindowList()
    self.separatorAct.setVisible(len(windows) != 0)

    for i, window in enumerate(windows):
      child = window.widget()

      text = "%d %s" % (i + 1, child.title)
      if i < 9:
        text = '&' + text

      action = self.windowMenu.addAction(text)
      action.setCheckable(True)
      action.setChecked(child is self.activeMdiChild())
      action.triggered.connect(self.windowMapper.map)
      self.windowMapper.setMapping(action, window)

  def exist(self, Type):
    exist = False
    for i in self.mdiArea.subWindowList():
      if i.widget().type == Type:
        self.mdiArea.setActiveSubWindow(i)
        exist = True
    return exist

  def openWindow(self, winType):
    if winType == 'product':
      self.openProduct()
    elif winType == 'release':
      self.openRelease()
    elif winType == 'contract':
      self.openContract()
    elif winType == 'partner':
      self.openPartner()
    elif winType == 'location':
      self.openLocation()
    elif winType == 'order':
      self.openOrder()
    elif winType == 'service':
      self.openService()
    elif winType == 'verify':
      self.openVerify()

  def openProduct(self):
    if not self.exist('product'):
      product = Basic(self, 'product', u'Изделия', ':/icons/icons/Globe.png', u'Изделие')
      product.title = u'Изделия'
      self.mdiArea.addSubWin(product)

  def openRelease(self):
    if not self.exist('release'):
      release = Basic(self, 'release', u'Экземпляры', ':/icons/icons/exemplar.png', u'Экземпляр')
      release.title = u'Экземпляры'
      self.mdiArea.addSubWin(release)

  def openContract(self):
    if not self.exist('contract'):
      contr = Basic(self, 'contract', u'Контракты', ':/icons/icons/Text.png', u'Контракт')
      contr.title = u'Контракты'
      self.mdiArea.addSubWin(contr)

  def openPartner(self):
    if not self.exist('partner'):
      partn = Basic(self, 'partner', u'Контрагенты', ':/icons/icons/partner.png', u'Контрагент')
      partn.title = u'Контрагенты'
      self.mdiArea.addSubWin(partn)

  def openLocation(self):
    if not self.exist('location'):
      location = Basic(self, 'location', u'Объекты эксплуатации', ':/icons/icons/Green pin.png', u'Объект')
      location.title = u'Объекты эксплуатации'
      self.mdiArea.addSubWin(location)

  def openOrder(self):
    if not self.exist('order'):
      order = Basic(self, 'order', u'Заказы', ':/icons/icons/List.png', u'Заказ')
      order.title = u'Заказы'
      self.mdiArea.addSubWin(order)

  def openService(self):
    if not self.exist('service'):
      service = Basic(self, 'service', u'Сервисное обслуживание', ':/icons/icons/service.png', u'Сервисное обслуживание')
      service.title = u'Сервисное обслуживание'
      self.mdiArea.addSubWin(service)

  def openVerify(self):
    if not self.exist('verify'):
      verify = Basic(self, 'verify', u'Входной контроль', ':/icons/icons/Yes.png', u'Входной контроль')
      verify.title = u'Входной контроль'
      self.mdiArea.addSubWin(verify)

  def openTypeEditor(self):
    #if not self.exist('typeEditor'):
    typeEditorWin = TypeEditor(self, 'typeEditor', u'Настройка типов', ':/icons/icons/Green pin.png')
      #typeEditorWin.title = u'Настройка типов'
      #self.mdiArea.addSubWin(typeEditorWin)
    typeEditorWin.exec_()


  def openTerminal(self):
    terminal = Terminal(self)
    terminal.title = u'Терминал'
    self.mdiArea.addSubWin(terminal)

  def export_(self):
    self.mdiArea.activeSubWindow().widget().export_()

  def import_(self):
    self.mdiArea.activeSubWindow().widget().import_()

  def createActions(self):
    self.products = QtGui.QAction(QtGui.QIcon(':/icons/icons/Globe.png'), u"&Изделия",
        self, statusTip=u"Изделия", triggered=self.openProduct)

    self.releases = QtGui.QAction(QtGui.QIcon(':/icons/icons/exemplar.png'), u"&Экземпляры",
        self, statusTip=u"Экземпляры", triggered=self.openRelease)

    self.contrs = QtGui.QAction(QtGui.QIcon(':/icons/icons/Text.png'), u"&Контракты",
        self, statusTip=u"Контракты", triggered=self.openContract)

    self.partns = QtGui.QAction(QtGui.QIcon(':/icons/icons/partner.png'), u"&Контрагенты",
        self, statusTip=u"Контрагенты", triggered=self.openPartner)

    self.locations = QtGui.QAction(QtGui.QIcon(':/icons/icons/Green pin.png'), u"&Объекты эксплуатации",
        self, statusTip=u"Объекты эксплуатации", triggered=self.openLocation)
    self.orders = QtGui.QAction(QtGui.QIcon(':/icons/icons/List.png'), u"&Заказы",
        self, statusTip=u"Заказы", triggered=self.openOrder)
    self.services = QtGui.QAction(QtGui.QIcon(':/icons/icons/service.png'), u"&Сервисное обслуживание",
        self, statusTip=u"Сервисное обслуживание", triggered=self.openService)
    self.verify_ = QtGui.QAction(QtGui.QIcon(':/icons/icons/Yes.png'), u"&Входной контроль",
        self, statusTip=u"Входной контроль", triggered=self.openVerify)

    self.terminal = QtGui.QAction(QtGui.QIcon(':/icons/icons/Terminal.png'), u"&Терминал",
        self, statusTip=u"Терминал (для администратора)", triggered=self.openTerminal)
    self.terminal.setEnabled(False)

    self.exitAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Exit.png'), u"Выход", self,
        shortcut=QtGui.QKeySequence.Quit,
        statusTip=u"Закрыть программу",
        triggered=QtGui.qApp.closeAllWindows)

    self.closeAct = QtGui.QAction(u"Закрыть", self,
        statusTip=u"Закрыть активное окно",
        triggered=self.mdiArea.closeActiveSubWindow)

    self.closeAllAct = QtGui.QAction(u"Закрыть все", self,
        statusTip=u"Разкрыть все окна",
        triggered=self.mdiArea.closeAllSubWindows)

    self.tileAct = QtGui.QAction(u"&Плитка", self,
        statusTip=u"Разположить окна плиткой (замостить)",
        triggered=self.mdiArea.tileSubWindows)

    self.cascadeAct = QtGui.QAction(u"Каскад", self,
        statusTip=u"Расположить окна каскадом",
        triggered=self.mdiArea.cascadeSubWindows)

    self.nextAct = QtGui.QAction(u"Следующее окно", self,
        shortcut=QtGui.QKeySequence.NextChild,
        statusTip=u"Сделать активным следующее окно",
        triggered=self.mdiArea.activateNextSubWindow)

    self.previousAct = QtGui.QAction(u"Предыдущее окно", self,
        shortcut=QtGui.QKeySequence.PreviousChild,
        statusTip=u"Сделать активным предыдущее окно",
        triggered=self.mdiArea.activatePreviousSubWindow)

    self.typeEditorAct = QtGui.QAction(u"Настройки типов", self,
        statusTip=u"Настройка типов",
        triggered=self.openTypeEditor)

    self.separatorAct = QtGui.QAction(self)
    self.separatorAct.setSeparator(True)

    self.aboutAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/Info.png'), u"&О программе", self,
        statusTip=u"Открыть описание программы",
        triggered=self.about)

    self.exportAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/export.ico'), u"&Экспорт", self,
        statusTip=u"Экспортировать выделенные элементы в файл",
        triggered=self.export_)

    self.importAct = QtGui.QAction(QtGui.QIcon(':/icons/icons/import.png'), u"&Импорт", self,
        statusTip=u"Импортировать файл",
        triggered=self.import_)

  def createMenus(self):
    self.fileMenu = self.menuBar().addMenu(u"&Файл")
    self.fileMenu.addAction(self.exportAct)
    self.fileMenu.addAction(self.importAct)
    self.fileMenu.addSeparator()
    self.fileMenu.addAction(self.terminal)
    self.fileMenu.addSeparator()
    self.fileMenu.addAction(self.exitAct)
    self.fileMenu.aboutToShow.connect(self.updateFileMenu)

    self.settingsMenu = self.menuBar().addMenu(u"&Настройки")
    self.settingsMenu.addAction(self.typeEditorAct)

    self.editMenu = self.menuBar().addMenu(u"&Средства")
    self.editMenu.addAction(self.products)
    self.editMenu.addAction(self.releases)
    self.catalogs = self.editMenu.addMenu(u"&Справочники")
    self.catalogs.addAction(self.contrs)
    self.catalogs.addAction(self.partns)
    self.catalogs.addAction(self.locations)
    self.catalogs.addAction(self.orders)
    self.catalogs.addAction(self.services)
    self.catalogs.addAction(self.verify_)

    self.windowMenu = self.menuBar().addMenu(u"&Окно")
    self.updateWindowMenu()
    self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

    self.menuBar().addSeparator()

    self.helpMenu = self.menuBar().addMenu(u"&Помощь")
    self.helpMenu.addAction(self.aboutAct)

  def createStatusBar(self):
    self.statusBar().addPermanentWidget(self.progress)

    # status bar
    self.form_data = '%H:%M:%S %d.%m.%Y'
    self.T = datetime.today().strftime(self.form_data)
    self.diod = QtGui.QLabel(u'{}'.format(self.T))
    self.diod.setStyleSheet("color: black")
    self.diod.setPixmap(QtGui.QPixmap(":/icons/icons/circle-red.png"))
    self.statusBar().addPermanentWidget(self.diod)

    # timer
    self.ans = 'start'
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.ping_thread)
    self.timer.timeout.connect(self.indicator)
    self.timer.start(2000) #trigger every minute - 60000.

  def pinger(self, t):
    try:
      ping = Server.ping()
      if ping:
        self.ans = 'ok'
      else:
        self.ans = 'not_ok'
    except Exception, exp:
      #print "Can't connect to server", exp
      self.ans = 'not_ok'
    time.sleep(t)

  def ping_thread(self):
    D = threading.Thread(target=self.pinger, args=(1,))
    D.deamon = True
    D.start()

  def indicator(self):
    if self.ans == 'ok':
      self.T = datetime.today().strftime(self.form_data)
      self.diod.setStyleSheet("color: black")
      self.diod.setPixmap(QtGui.QPixmap(":/icons/icons/circle-green.png"))
      self.diod.setToolTip(u'Связь с сервером установлена')
      self.timer.start(6000)
    elif self.ans == 'not_ok':
      self.diod.setStyleSheet("color: red")
      self.diod.setPixmap(QtGui.QPixmap(":/icons/icons/circle-red.png"))
      self.diod.setToolTip(u'Сервер не доступен с {}'.format(self.T))
      self.timer.start(6000)
    elif self.ans == 'start':
      pass

  def readSettings(self):
    settings = QtCore.QSettings('Rubin', 'Gorynych')
    if settings.value('size').toString() == 'max':
      self.showMaximized()
    else:
      self.move(settings.value('pos').toPoint())
      self.resize(settings.value('size').toSize())

  def writeSettings(self):
    settings = QtCore.QSettings('Rubin', 'Gorynych')
    if self.isMaximized():
      settings.setValue('size', 'max')
    else:
      settings.setValue('pos', self.pos())
      settings.setValue('size', self.size())

  def activeMdiChild(self):
    activeSubWindow = self.mdiArea.activeSubWindow()
    if activeSubWindow:
      return activeSubWindow.widget()
    return None

  def setActiveSubWindow(self, window):
    if window:
      self.mdiArea.setActiveSubWindow(window)

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  login = Login()

  if login.exec_() == QtGui.QDialog.Accepted:
    mainWin = MainWindow(login.auth)
    mainWin.show()
    sys.exit(app.exec_())
