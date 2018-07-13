#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import icons

class Buttons(QtGui.QHBoxLayout):
  def __init__(self, parent, winTitle):
    super(Buttons, self).__init__()

    self.parent = parent

    self.parent.winTypeLab = QtGui.QLabel()
    self.parent.winTypeLab.setText(winTitle)
    self.parent.winTypeLab.setFont(self.parent.bold)
    self.parent.winTypeLab.setAlignment(QtCore.Qt.AlignCenter)
    self.parent.winTypeLab.setStyleSheet("QLabel { color : grey; }");

    self.parent.refresh_btn = QtGui.QPushButton(QtGui.QIcon(':/icons/icons/Refresh.png'), u'')
    self.parent.refresh_btn.setToolTip(u'<b>Обновить</b>')
    self.parent.connect(self.parent.refresh_btn, QtCore.SIGNAL('clicked()'), lambda: self.parent.refresh(tree=1))

    self.parent.type_cfg_btn = QtGui.QPushButton(QtGui.QIcon(':/icons/icons/Application.png'), u'')
    self.parent.type_cfg_btn.setToolTip(u'<b>Параметры типа</b>')
    self.parent.connect(self.parent.type_cfg_btn, QtCore.SIGNAL('clicked()'), lambda: self.parent.typeParams())

    self.parent.save_btn = QtGui.QPushButton(QtGui.QIcon(':/icons/icons/Save.png'), u'')
    self.parent.save_btn.setToolTip(u'<b>Сохранить</b>')
    self.parent.save_btn.setEnabled(False)
    self.parent.connect(self.parent.save_btn, QtCore.SIGNAL('clicked()'), self.parent.saveItems)

    self.parent.type_filter = QtGui.QComboBox()
    self.parent.type_filter.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
    self.parent.type_filter.setToolTip(u'<b>Фильтр типов</b>')
    self.parent.type_filter.setHidden(True)
    self.parent.type_filter.currentIndexChanged.connect(self.parent.refreshTree)

    self.addWidget(self.parent.winTypeLab)
    self.addSpacing(20)
    self.addWidget(self.parent.type_filter)
    self.addWidget(self.parent.type_cfg_btn)
    #self.addSpacing(20)
    #self.addWidget(self.parent.refresh_btn)
    self.addSpacing(20)
    self.addStretch(1)
    self.addWidget(self.parent.refresh_btn)
    #self.addWidget(self.parent.save_btn)

