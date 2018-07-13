# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import pyqtSignal, QObject
from frameworkAPI import addThread, getWindow, addAction, addTrayIcon, genIcon, genMenu
from SecureXMLRPCServer import ThreadingSecureXMLRPCServer
from api import API
from settings import srvIP, srvPort, certFile, keyFile
from code import InteractiveConsole

class PrintLog(QObject):
    printed = pyqtSignal(object)
    def __init__(self, out=sys.stdout):
        super(PrintLog, self).__init__()
        if out == sys.stdout:
            self._stdout = True
            self._stream = out
            sys.stdout = self
        else:
            self._stdout = False
            self._stream = out
            sys.stderr = self
    def write(self, text):
        self._stream.write(text)
        self.printed.emit(text)
    def __getattr__(self, name):
        return getattr(self._stream, name)
    def __del__(self):
        try:
            if self._stdout:
                sys.stdout = self._stream
            else:
                sys.stderr = self._stream
        except AttributeError:
            pass

class Plugin:
    def __init__(self, parent, path):
        self.tab = True
        self.path = path
        self.name = u'Сервер ПК "Горыныч"'
        self.icon = u'{}icons/main.png'.format(path)
        self.iconTrue = genIcon(u'{}icons/main.png'.format(path))
        self.iconFalse = genIcon(u'{}icons/false.png'.format(path))
        self.iconStart = genIcon(u'{}icons/start.png'.format(path))
        self.iconStop = genIcon(u'{}icons/stop.png'.format(path))
        self.progressBar = None
        self.tray = parent.tray
        self.trayMenu = parent.trayMenu
        self.task = None
        self.main = getWindow(parent, 'window')
        self.main.setButton1(text=u'СТОП', action=self.terminate)
        self.main.setButton2(text=u'ОЧИСТИТЬ', action=self.clear)

        self.actionStart = addAction(parent, run=self.run, icon=self.iconStart, text=u'&Пуск', tip=u'Запустить сервер', trayMenu=True)
        self.actionStop = addAction(parent, run=self.terminate, icon=self.iconStop, text=u'&Стоп', tip=u'Остановить сервер')

        self.main.setTextInput1(action=self.interact)
        self.main.setTextEdit1(write=False)

        #### БЕЗ ЭТОЙ ЧУШИ РАБОТАЕТ ТОЛЬКО ПОСЛЕДНЯЯ ВКЛАДКА ####
        self.fix = self.isTab

        def textAppend(text):
            self.main.setTextEdit1(text=text, write=False, append=True)
        stdout = PrintLog(sys.stdout)
        stdout.printed.connect(textAppend)
        #stderr = PrintLog(sys.stderr)
        #stderr.printed.connect(textAppend)


        self.shell = InteractiveConsole()
        self.shell.push("import json, xmlrpclib")
        self.shell.push("cfg = xmlrpclib.ServerProxy('https://127.0.0.1:{}')".format(srvPort))

        self.start()

    def start(self):
        def run():
            try:
                self.server = ThreadingSecureXMLRPCServer((srvIP, srvPort), certFile, keyFile)
                self.server.register_instance(API())
                self.server.serve_forever()
            except Exception as error:
                print str(error).decode('utf8')
        def onStart():
            print u'Сервер принимает безопасные подключения {}...'.format(self.server.server_address)
            self.trayMenu.removeAction(self.actionStart)
            self.trayMenu.addAction(self.actionStop)
            self.tray.setIcon(self.iconTrue)
            #self.contextMenu.clear()
            #genMenu(items={u'Остановка':self.terminate}, menu=self.contextMenu)
            self.main.setButton1(text=u'СТОП', action=self.terminate)
        def onTerminate():
            self.server.server_close()
            print u'Сервер остановлен!'
            self.trayMenu.removeAction(self.actionStop)
            self.trayMenu.addAction(self.actionStart)
            self.tray.setIcon(self.iconFalse)
            #self.contextMenu.clear()
            #genMenu(items={u'Запуск':self.run}, menu=self.contextMenu)
            self.main.setButton1(text=u'ПУСК', action=self.run)

        self.state = None
        #self.contextMenu = genMenu()
        #self.tray = addTrayIcon(self, icon=self.iconFalse, tip=self.name, contextMenu=self.contextMenu, run=self.show, visible=True)
        self.task = addThread(self, run=run, onStart=onStart, onTerminate=onTerminate)
        self.task.start()

    def isTab(self):
        if self.tab:
            return True
        else:
            return False

    def getProgressBar(self):
        return self.progressBar

    def getTab(self):
        return self.main

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def show(self):
        self.showWindow()

    def clear(self):
        self.main.setTextEdit1(text=u'', write=False)

    def run(self):
        self.task.start()

    def terminate(self):
        self.task.terminate()

    def interact(self):
        query =  u"try:\n"
        query += u"  print u'''Выполняется команда \"{}\"...'''\n".format(self.main.getTextInput1())
        query += u"  {}\n".format(self.main.getTextInput1())
        query += u"except xmlrpclib.Fault as error:\n"
        query += u"  print error.faultString.decode('utf8')\n"
        query += u"except Exception as error:\n"
        query += u"  print str(error).decode('utf8')\n"
        self.shell.push(query)

    def showWindow(self):
        self.main.setWindow(title=self.name, icon=self.icon)
