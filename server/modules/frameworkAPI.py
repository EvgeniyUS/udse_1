# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, QThread, QFile, pyqtSignal
from PyQt4.QtGui import QLabel, QIcon, QMenu, QCursor, QSystemTrayIcon, QAction, QProgressBar
from importlib import import_module
from time import sleep
import os, sys

class Thread(QThread):
    paused = pyqtSignal()
    resumed = pyqtSignal()
    stepped = pyqtSignal(object)
    def __init__(self, run=lambda:None):
        super(Thread, self).__init__()
        self.method = run
        self.isPaused = False
    def addStep(self, sleep=0, send=None):
        self.stepped.emit(send)
        self.sleep(sleep)
        while self.isPaused:
            self.sleep(1)
    def run(self):
        self.method()
    def pause(self):
        self.paused.emit()
        self.isPaused = True
    def resume(self):
        self.resumed.emit()
        self.isPaused = False

class ProgressBar(QProgressBar):
    def __init__(self):
        super(ProgressBar, self).__init__()
        def showMenu():
            self.menu.exec_(QCursor.pos())
        self.menu = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(showMenu)
    def setContextMenu(self, menu):
        if self.menu:
            self.menu.clear()
        if menu is not None:
            self.menu = menu

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super(SystemTrayIcon, self).__init__()
        self.parent = parent
    def showMessage(self, title, text, icon=QSystemTrayIcon.Information, delay=10000, run=None):
        def pause():
            sleep(0.1)
        def show():
            super(SystemTrayIcon, self).showMessage(title, text, icon, delay)
        addThread(self, run=pause, onFinish=show).start()
        if not run:
            run = self.parent.show
        try:
            self.messageClicked.disconnect()
        except Exception:
            pass
        finally:
            self.messageClicked.connect(run)

def addThread(parent, run=lambda:None, onStart=lambda:None, onStep=lambda:None, onPause=lambda:None, onResume=lambda:None, onTerminate=lambda:None, onFinish=lambda:None):
    parent.thread = Thread(run)
    parent.thread.started.connect(onStart)
    parent.thread.stepped.connect(onStep)
    parent.thread.paused.connect(onPause)
    parent.thread.resumed.connect(onResume)
    parent.thread.terminated.connect(onTerminate)
    parent.thread.finished.connect(onFinish)
    return parent.thread

# Получение готового объекта вкладки от плагина
def getPlugin(parent, plugin):
    # Вычисляем путь к папке плагина со слешем на конце [realpath() позволяет проходить по ссылкам]
    pluginPath = os.path.realpath(u'plugins/{0}/{0}'.format(plugin)).rstrip(plugin)
    # Добавляем папку плагина в начало списка путей для загрузки модулей из неё в первую очередь
    sys.path.insert(0, pluginPath)
    try:
        # Импортируем класс плагина и создаём из него объект, сообщая путь к его ресурсам
        plugin = import_module('plugins.{0}.{0}'.format(plugin)).Plugin(parent, pluginPath)
    except Exception as error:
        plugin = None
        print str(error)
    # Возвращаем созданный объект
    return plugin

# Получение объекта типового окна по имени
def getWindow(parent, window, dialog=False):
    # Импортируем класс окна и создаём из него объект
    window = import_module('windows.{}'.format(window)).Window(parent, dialog)
    # Закрывать дочерние окна при уничтожении главного окна
    parent.destroyed.connect(window.close)
    # Возвращаем созданный объект
    return window

# Создание меню
def genMenu(items={}, menu=None):
    # Если не передан объект меню...
    if not menu:
        # Создаём объект меню
        menu = QMenu()
    # Для каждого пункта...
    for item in items:
        # Если является словарём...
        if isinstance(items[item], dict):
            # Создаём подменю
            genMenu(items=items[item], menu=menu.addMenu(item))
        # Иначе...
        else:
            # Добавляем пункт меню
            menu.addAction(item, items[item])
    # Возвращаем созданный объект
    return menu

# Создание иконки
def genIcon(path=u''):
    # Если файл иконки не существует...
    if not QFile(path).exists():
        # Заменяем путь на пустой (необходимо для проверки .isNull())
        path = u''
    # Создаём объект иконки из изображения
    icon = QIcon(path)
    # Возвращаем созданный объект
    return icon

def addTrayIcon(parent ,icon=u'', tip=u'', contextMenu={}, run=None, visible=False):
    def onClick(QEvent):
        if QEvent == QSystemTrayIcon.DoubleClick: # 2 == QSystemTrayIcon.DoubleClick
            sleep(0.1)
            run()
    # Если иконка не в нужном формате...
    if not isinstance(icon, QIcon):
        # Создаём иконку
        icon = genIcon(path=icon)
    # Если иконка пустая...
    if icon.isNull():
        # Используем стандартную иконку плагина
        icon = genIcon(path=u'icons/plugin.png')
    if isinstance(contextMenu, QMenu):
        menu = contextMenu
    else:
        menu = genMenu(items=contextMenu)
    tray = SystemTrayIcon(parent)
    tray.setIcon(icon)
    tray.setContextMenu(menu)
    if not run:
        run = parent.show
    tray.activated.connect(onClick)
    tray.setToolTip(tip)
    if visible:
        tray.show()
    return tray

def addStatusIcon(parent, icon=u'', tip=u'', contextMenu={}):
    statusBar = parent.statusBar
    # Если иконка не в нужном формате...
    if not isinstance(icon, QIcon):
        # Создаём иконку
        icon = genIcon(path=icon)
    # Если иконка пустая...
    if icon.isNull():
        # Используем стандартную иконку плагина
        icon = genIcon(path=u'icons/plugin.png')
    if isinstance(contextMenu, QMenu):
        menu = contextMenu
    else:
        menu = genMenu(items=contextMenu)
    def showMenu():
        menu.exec_(QCursor.pos())
    icon = icon.pixmap(statusBar.height()/2)
    button = QLabel()
    button.setPixmap(icon)
    button.setToolTip(tip)
    button.setStatusTip(tip)
    button.setContextMenuPolicy(Qt.CustomContextMenu)
    button.customContextMenuRequested.connect(showMenu)
    statusBar.addPermanentWidget(button)
    return button

def addProgressBar(parent, width=200, tip=u'', visible=False):
    statusBar = parent.statusBar
    progressBar = ProgressBar()
    progressBar.setMaximumHeight(statusBar.height()/2)
    progressBar.setMaximumWidth(width)
    progressBar.setAlignment(Qt.AlignCenter)
    progressBar.setTextVisible(False)
    progressBar.setVisible(visible)
    progressBar.setToolTip(tip)
    progressBar.setStatusTip(tip)
    statusBar.insertPermanentWidget(0, progressBar)
    return progressBar

# Добавление действия в главное меню, которое может быть размещено на панели инструментов и в системном меню
def addAction(parent, run=lambda:None, icon=u'', text=u'', tip=u'', shortcut=u'', submenu='', toolbar=False, trayMenu=False):
    # Если иконка не в нужном формате...
    if not isinstance(icon, QIcon):
        # Создаём иконку
        icon = genIcon(path=icon)
    # Если иконка пустая...
    if icon.isNull():
        # Создаём объект действия без иконки
        action = QAction(text, parent)
    # Иначе...
    else:
        # Создаём объект действия с иконкой
        action = QAction(icon, text, parent)
    # Назначаем горячуие клавиши
    action.setShortcut(shortcut)
    # Добавляем описание в статусной строке
    action.setStatusTip(tip)
    # Связываем с методом
    action.triggered.connect(run)
    # Если целью указано главное меню...
    if submenu:
        # Ищем подменю по имени объекта
        submenu = parent.mainMenu.findChild(QMenu, submenu)
        # Если целевое подменю существует...
        if submenu:
            # Добавляем в него действие
            submenu.addAction(action)
        # Иначе...
        else:
            # Добавляем действие в подменю "Дополнения"
            parent.pluginMenu.addAction(action)
    # Если целью указана панель инструментов...
    if toolbar:
        # Добавляем действие на панель инструментов
        parent.toolbar.addAction(action)
    # Если целью указано системное меню...
    if trayMenu:
        # Добавляем действие в системное меню
        parent.trayMenu.addAction(action)
    # Возвращаем созданный объект
    return action

