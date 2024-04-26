# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gviewwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1015, 804)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 60, 571, 601))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 710, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.ModelcomboBox = QtWidgets.QComboBox(Form)
        self.ModelcomboBox.setGeometry(QtCore.QRect(220, 710, 81, 22))
        self.ModelcomboBox.setObjectName("ModelcomboBox")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(700, 90, 241, 421))
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.label.setText(_translate("Form", "TextLabel"))

