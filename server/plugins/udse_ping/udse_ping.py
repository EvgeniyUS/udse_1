# -*- coding: utf-8 -*-

from frameworkAPI import addThread, getWindow, addAction, addTrayIcon, genIcon, genMenu
import json, xmlrpclib


class Plugin:
    def __init__(self, parent, path):
        self.tab = False
        self.path = path
        self.name = u'Пингер'
        self.icon = u'{}icons/main.png'.format(path)
        self.iconTrue = genIcon(u'{}icons/true.png'.format(path))
        self.iconFalse = genIcon(u'{}icons/false.png'.format(path))
        self.iconPause = genIcon(u'{}icons/pause.png'.format(path))
        self.progressBar = None
        self.task = None
        self.window = getWindow(parent, 'window')
        self.windowName = u'Пингер'
        self.window.setButton1(text=u'ПАУЗА', action=self.pause)
        self.window.setButton2(text=u'ОЧИСТИТЬ', action=self.clear)
        self.window.setButton3(text=u'ЗАКРЫТЬ', action=self.windowButton3Action)
        self.window.setTextEdit1()
        addAction(parent, run=self.showWindow, icon=self.icon, text=u'&Пингер', tip=u'Запустить плагин', shortcut=u'Alt+P', submenu='plugin', toolbar=False, trayMenu=True)

        #### БЕЗ ЭТОЙ ЧУШИ РАБОТАЕТ ТОЛЬКО ПОСЛЕДНЯЯ ВКЛАДКА ####
        self.fix = self.isTab

        self.start()

    def start(self):
        def run():
            try:
                with open(u'{}settings.cfg'.format(self.path)) as file:
                    config = json.load(file)
                srvIP = config['srvIP']
                srvPort = config['srvPort']
                server = xmlrpclib.ServerProxy('https://{}:{}'.format(srvIP, srvPort))
            except Exception as error:
                raise
            while True:
                try:
                    result = server.ping()
                except Exception:
                    result = False
                self.task.addStep(sleep=1, send=result)
        def onStep(value):
            if value:
                if self.state != value:
                    self.state = value
                    self.tray.setIcon(self.iconTrue)
                    self.window.setTextEdit1(text=u'Сервер доступен!\n', append=True, write=False)
                    self.tray.showMessage(title=self.name, text=u'Сервер доступен!', run=self.show)
            else:
                if self.state != value:
                    self.state = value
                    self.tray.setIcon(self.iconFalse)
                    self.window.setTextEdit1(text=u'Сервер недоступен!\n', append=True, write=False)
                    self.tray.showMessage(title=self.name, text=u'Сервер недоступен!', icon=2, run=self.show)
        def onPause():
            self.tray.setIcon(self.iconPause)
            self.window.setTextEdit1(text=u'ПРИОСТАНОВЛЕНО\n', append=True, write=False)
            self.window.setButton1(text=u'ЗАПУСК', action=self.resume)
            self.state = None
            self.contextMenu.clear()
            genMenu(items={u'Запуск':self.resume}, menu=self.contextMenu)
        def onResume():
            self.window.setTextEdit1(text=u'ЗАПУЩЕНО\n', append=True, write=False)
            self.window.setButton1(text=u'ПАУЗА', action=self.pause)
            self.contextMenu.clear()
            genMenu(items={u'Пауза':self.pause}, menu=self.contextMenu)

        self.state = None
        self.contextMenu = genMenu(items={u'Пауза':self.pause})
        self.tray = addTrayIcon(self, icon=self.iconFalse, tip=self.name, contextMenu=self.contextMenu, run=self.show, visible=True)
        self.task = addThread(self, run=run, onStep=onStep, onPause=onPause, onResume=onResume)
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
        self.window.setTextEdit1(text=u'', write=False)

    def pause(self):
        self.task.pause()

    def resume(self):
        self.task.resume()

    def windowButton3Action(self):
        self.window.close()

    def showWindow(self):
        self.window.setWindow(title=self.windowName, icon=self.icon)
