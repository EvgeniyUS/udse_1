# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QIcon, QLineEdit, QTextCursor
from PyQt4.QtCore import Qt, pyqtSignal
import platform

class LineEdit(QLineEdit):
    keyUpPressed = pyqtSignal()
    keyDownPressed = pyqtSignal()
    def keyPressEvent(self, event):
        super(LineEdit, self).keyPressEvent(event)
        if event.key() == Qt.Key_Up:
            self.keyUpPressed.emit()
        if event.key() == Qt.Key_Down:
            self.keyDownPressed.emit()
    def __init__(self):
        super(LineEdit, self).__init__()

class Window(QWidget):
    keyEscapePressed = pyqtSignal()
    def keyPressEvent(self, event):
        super(Window, self).keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.keyEscapePressed.emit()

    def __init__(self, parent, dialog=False):
        super(Window, self).__init__()
        self.icon = parent.windowIcon()
        self.layout	= QVBoxLayout()
        self.textEdit1 = QTextBrowser()
        self.textEdit1.setVisible(False)
        self.layout.addWidget(self.textEdit1)
        self.textInput1 = LineEdit()
        self.textInput1.setVisible(False)
        self.layout.addWidget(self.textInput1)
        self.button1 = QPushButton()
        self.button1.setVisible(False)
        self.layout.addWidget(self.button1)
        self.button2 = QPushButton()
        self.button2.setVisible(False)
        self.layout.addWidget(self.button2)
        self.button3 = QPushButton()
        self.button3.setVisible(False)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)
        self.setTabOrder(self.button3, self.textEdit1)
        if dialog:
            self.setWindowModality(Qt.ApplicationModal)
            if platform.system() is 'Windows':
                self.setWindowFlags(Qt.Tool)
            self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)
            self.keyEscapePressed.connect(self.close)

    def setWindow(self, title=u'Window', icon=u''):
        self.setWindowTitle(title)
        icon = QIcon(icon)
        if icon.isNull():
            self.setWindowIcon(self.icon)
        else:
            self.setWindowIcon(icon)
        self.show()
        #self.setFixedSize(self.size())
        self.raise_()
        self.activateWindow()

    def setTextEdit1(self, text=u'', append=False, write=True, visible=True):
        textEdit = self.textEdit1
        if not write:
            textEdit.setReadOnly(True)
        if append:
            textEdit.moveCursor(QTextCursor.End)
            textEdit.insertPlainText(text)
        else:
            textEdit.setText(text)
        textEdit.setVisible(visible)
        return textEdit

    def getTextEdit1(self):
        return self.textEdit1.toPlainText()

    def setTextInput1(self, text=u'', append=False, write=True, action=lambda:None, history=5, visible=True):
        textInput = self.textInput1
        limit = history
        history = {'inputs':[''], 'current':-1}
        if not write:
            textInput.setReadOnly(True)
        if append:
            textInput.append(text)
        else:
            textInput.setText(text)
        def onReturnPressed():
            if textInput.text():
                history['inputs'].insert(0,textInput.text())
            if len(history['inputs']) == limit+2:
                history['inputs'][limit] = history['inputs'].pop(limit+1)
            history['current'] = -1
            action()
            textInput.clear()
        def onUpPressed():
            history['current'] += 1
            if history['current'] == len(history['inputs']):
                history['current'] = 0
            textInput.setText(history['inputs'][history['current']])
        def onDownPressed():
            history['current'] -= 1
            if history['current'] < 0:
                history['current'] = len(history['inputs']) - 1
            textInput.setText(history['inputs'][history['current']])
        textInput.returnPressed.connect(onReturnPressed)
        textInput.keyUpPressed.connect(onUpPressed)
        textInput.keyDownPressed.connect(onDownPressed)
        textInput.setVisible(visible)
        return textInput

    def getTextInput1(self):
        return self.textInput1.text()

    def setButton1(self, text=u'Button1', action=lambda:None, visible=True):
        button = self.button1
        button.setText(text)
        try:
            button.clicked.disconnect()
        except Exception:
            pass
        finally:
            button.clicked.connect(action)
        button.setAutoDefault(True)
        button.setVisible(visible)

    def setButton2(self, text=u'Button2', action=lambda:None, visible=True):
        button = self.button2
        button.setText(text)
        try:
            button.clicked.disconnect()
        except Exception:
            pass
        finally:
            button.clicked.connect(action)
        button.setAutoDefault(True)
        button.setVisible(visible)

    def setButton3(self, text=u'Button3', action=lambda:None, visible=True):
        button = self.button3
        button.setText(text)
        try:
            button.clicked.disconnect()
        except Exception:
            pass
        finally:
            button.clicked.connect(action)
        button.setAutoDefault(True)
        button.setVisible(visible)
