# -*- coding: utf-8 -*-

import os, sys
from ConfigParser import SafeConfigParser
modulesPath = os.path.realpath(u'modules')
# Добавляем папку модулей в начало списка путей поиска импортируемых модулей
sys.path.insert(0, modulesPath)

from modules.frameworkAPI import genIcon, genMenu, getPlugin, addTrayIcon, addAction
from PyQt4.QtGui import QApplication, QMainWindow, QTabWidget, QMessageBox
from PyQt4.QtCore import Qt, QTranslator, QLocale, QLibraryInfo


# Класс главного окна
class GUI(QMainWindow):
    # Инициализация состояния главного окна
    def __init__(self):
        super(GUI, self).__init__()
        # Запрещаем завершать приложение с закрытием последнего дочернего окна при скрытом (свёрнутом в трей) главном окне
        app.setQuitOnLastWindowClosed(False)
        # Чтобы главное окно уничтожалось после закрытия и отправлялся сиграл "destroyed()"
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        # Установка заголовка главного окна
        self.setWindowTitle(settings.get('DEFAULT', 'name').decode('utf8'))
        # Преобразуем изображение в формат QT-иконки
        self.icon = genIcon(path=settings.get('DEFAULT', 'icon').decode('utf8'))
        # Создаём список для учёта плагинов, связанных со вкладками
        self.tabs = []
        # Создаём переменную с номером текущей вкладки
        self.currentTab = 0
        # Используем виджет со вкладками в качестве основного
        self.main = QTabWidget()
        # Размещаем основной виджет в центральном виджете главного окна
        self.setCentralWidget(self.main)
        # Добавляем отступ слева, чтобы он визуально соответствовал отступу справа
        self.setContentsMargins(2,0,0,0)

        # Создаём панель главного меню
        self.mainMenu = self.menuBar()
        # Добавдяем подменю "Файл"
        self.mainMenu.addMenu(u'&Файл').setObjectName('file')
        # Добавдяем подменю "Правка"
        self.mainMenu.addMenu(u'&Правка').setObjectName('edit')
        # Добавдяем подменю "Вид"
        self.mainMenu.addMenu(u'&Вид').setObjectName('view')
        # Добавдяем подменю "Настройки"
        self.mainMenu.addMenu(u'&Настройки').setObjectName('preferences')
        # Добавдяем подменю "Дополнения"
        self.pluginMenu = self.mainMenu.addMenu(u'&Дополнения')
        # Добавдяем подменю "Справка"
        self.mainMenu.addMenu(u'&Справка').setObjectName('help')

        # Создаём панель инструментов "Стандартная"
        self.toolbar = self.addToolBar(u'Стандартная')
        # Закрепляем панель инструментов
        self.toolbar.setMovable(False)

        
        # Создаём статусную строку
        self.statusBar = self.statusBar()

        # Создаём меню для иконки в системной области
        self.trayMenu = genMenu()

        # Добавляем иконку с контекстным меню в системную область
        self.tray = addTrayIcon(self, icon=self.icon, tip=self.windowTitle(), contextMenu=self.trayMenu)

        # Получаем список папок в папке plugins
        plugins = next(os.walk('plugins'))[1]
        # Для каждого плагина из списка...
        for plugin in plugins:
            # Создаём объект плагина
            self.plugin = getPlugin(self, plugin)
            # Если плагин использует вкладку...
            if self.plugin and self.plugin.isTab():
                # Получаем виджет вкладки
                tab = self.plugin.getTab()
                # Получаем иконку вкладки
                icon = genIcon(path=self.plugin.getIcon())
                # Получаем имя вкладки
                name = self.plugin.getName()
                # Создаём объект вкладки
                self.main.addTab(tab, icon, name)
                # Добавляем с список ссылку на объект плагина, связанный со вкладкой (индексы совпадают) 
                self.tabs.append(self.plugin)
        # Если у приложения одна вкладка...
        if self.main.count() == 1:
            # Скрыть панель вкладок
            self.main.tabBar().setVisible(False)
            # Сделать заголовком главного окна имя вкладки
            self.setWindowTitle(self.main.tabText(0))
            # Сделать подсказкой иконки в трее имя вкладки
            self.tray.setToolTip(self.main.tabText(0))
            # Если у вкладки есть иконка...
            if not self.main.tabIcon(0).isNull():
                # Сохраняем иконку из вкладки
                self.icon = self.main.tabIcon(0)
        # Если у приложения несколько вкладок...
        elif self.main.count() > 1:
            # Связываем смену вкладки с действием
            self.main.currentChanged.connect(self.setCurrentTab)
            # Выполняем действия при активации вкладки
            self.setCurrentTab()
        # Меняем иконку в системной области
        self.tray.setIcon(self.icon)
        # Меняем иконку главного окна
        self.setWindowIcon(self.icon)
        # Меняем иконку приложения
        app.setWindowIcon(self.icon)

        # Добавляем действие выхода из приложения на панель инструментов, в главное и системное меню
        addAction(self, run=self.close, icon='icons/exit.png', text=u'Вы&ход', tip=u'Выйти из приложения', shortcut=u'Ctrl+Q', submenu='file', trayMenu=True)

        # Если у приложения нет вкладок...
        if self.isTrayed() or self.main.count() == 0:
            # Только отображаем иконку в системной области
            self.hide()
        # Иначе...
        else:
            self.show()

    def isTrayed(self):
        return settings.getboolean('DEFAULT', 'trayed')

    def isClosable(self):
        return settings.getboolean('DEFAULT', 'closable')

    def isCentred(self):
        return settings.getboolean('DEFAULT', 'centred')

    # Действия при активации вкладки
    def setCurrentTab(self):
        progressBar = self.tabs[self.currentTab].getProgressBar()
        if progressBar:
            progressBar.setVisible(False)
        self.currentTab = self.main.currentIndex()
        progressBar = self.tabs[self.currentTab].getProgressBar()
        if progressBar:
            progressBar.setVisible(True)

    def resizeEvent(self, *args, **kwargs):
        if not self.isMaximized() and not self.isMinimized() and not self.isTrayed():
            settings.set('DEFAULT', 'width', str(self.width()))
            settings.set('DEFAULT', 'height', str(self.height()))
            settings.set('DEFAULT', 'screen', str(app.desktop().screenNumber(self)))
            return super(GUI, self).resizeEvent(*args, **kwargs)

    def moveEvent(self, *args, **kwargs):
        if not self.isMaximized() and not self.isMinimized() and not self.isTrayed():
            settings.set('DEFAULT', 'x', str(self.x()))
            settings.set('DEFAULT', 'y', str(self.y()))
            settings.set('DEFAULT', 'screen', str(app.desktop().screenNumber(self)))
            return super(GUI, self).moveEvent(*args, **kwargs)

    def show(self, parent=None):
        if parent:
            try:
                tab = self.tabs.index(parent)
                self.main.setCurrentIndex(tab)
            except Exception:
                pass
        width = settings.getint('DEFAULT', 'width')
        height = settings.getint('DEFAULT', 'height')
        self.resize(width, height)
        x = settings.getint('DEFAULT', 'x')
        y = settings.getint('DEFAULT', 'y')
        self.move(x, y)
        screen = app.desktop().availableGeometry(app.desktop().screenNumber(self.frameGeometry().topLeft()))
        if self.isCentred() or (x+width < 0) or (y < 0) or (x > screen.x()+screen.width()) or (y > screen.y()+screen.height()):
            screen = settings.getint('DEFAULT', 'screen')
            center = app.desktop().availableGeometry(screen).center()
            geometry = self.frameGeometry()
            geometry.moveCenter(center)
            self.move(geometry.topLeft())
        if settings.getboolean('DEFAULT', 'maximized'):
            super(GUI, self).showMaximized()
        else:
            super(GUI, self).showNormal()
        # Поднимаем наверх
        self.raise_()
        # Делаем активным
        self.activateWindow()
        settings.set('DEFAULT', 'trayed', 'False')
        self.tray.hide()

    def hide(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.SplashScreen)
        self.tray.show()
        self.tray.showMessage(title=self.windowTitle(), text=u'Приложение свёрнуто в системную панель.', icon=1, delay=2000, run=lambda:None)
        settings.set('DEFAULT', 'trayed', 'True')
        return super(GUI, self).hide()

    def event(self, QEvent):
        if (QEvent.type() == QEvent.WindowStateChange):
            if self.isMinimized():
                self.hide()
            elif self.isMaximized():
                settings.set('DEFAULT', 'maximized', 'True')
            else:
                settings.set('DEFAULT', 'maximized', 'False')
        return super(GUI, self).event(QEvent)

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()
        if self.isClosable():
            self.close()
        else:
            self.hide()

    def close(self):
        if QMessageBox.Yes == QMessageBox.question(app.desktop(), self.windowTitle(), u'Хотите закрыть приложение?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            app.setQuitOnLastWindowClosed(True)
            settings.write(open('settings.ini', 'w'))
            #sys.stdout.close()
            #sys.stderr.close()
            app.quit()


if __name__ == '__main__':
    settings = {}
    settings['name'] = 'appFramework'
    settings['icon'] = 'icons/main.png'
    settings['maximized'] = 'False'
    settings['trayed'] = 'False'
    settings['closable'] = 'True'
    settings['centred'] = 'False'
    settings['width'] = '640'
    settings['height'] = '480'
    settings['x'] = '-7'
    settings['y'] = '-1'
    settings['screen'] = '-1'
    settings['locale'] = 'System'
    settings = SafeConfigParser(settings)
    settings.read('settings.ini')
    locale = settings.get('DEFAULT', 'locale')
    if locale  == 'System':
        # Получаем имя локали при помощи QLocale
        locale = QLocale.system().name()
    app = QApplication(sys.argv)
    # Создаём локализатор (делаем переведёнными стандартные системные диалоги и кнопки)
    translator = QTranslator()
    # Если не удалось подгрузить локализованные ресурсы из локальной папки...
    if not translator.load('qt_{}'.format(locale), os.path.realpath(u'locale/QT')):
        # Грузим ресурсы из расположения QT
        translator.load('qt_{}'.format(locale), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    # Подключаем локализатор к приложению
    app.installTranslator(translator)
    # Создаём объект главного окна
    main = GUI()
    sys.exit(app.exec_())
