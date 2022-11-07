# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PopUp_InsertarID.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PopUp_InsertarID(object):
    def setupUi(self, PopUp_InsertarID):
        if not PopUp_InsertarID.objectName():
            PopUp_InsertarID.setObjectName(u"PopUp_InsertarID")
        PopUp_InsertarID.resize(354, 234)
        self.label = QLabel(PopUp_InsertarID)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 80, 121, 16))
        self.ln_id = QLineEdit(PopUp_InsertarID)
        self.ln_id.setObjectName(u"ln_id")
        self.ln_id.setGeometry(QRect(220, 80, 113, 22))
        self.label_2 = QLabel(PopUp_InsertarID)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 140, 151, 16))
        self.lb_idRestantes = QLabel(PopUp_InsertarID)
        self.lb_idRestantes.setObjectName(u"lb_idRestantes")
        self.lb_idRestantes.setGeometry(QRect(220, 140, 111, 16))
        self.lb_idRestantes.setAlignment(Qt.AlignCenter)
        self.bt_confirmar = QPushButton(PopUp_InsertarID)
        self.bt_confirmar.setObjectName(u"bt_confirmar")
        self.bt_confirmar.setGeometry(QRect(140, 190, 93, 28))
        self.label_3 = QLabel(PopUp_InsertarID)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 30, 131, 16))
        self.lb_modeloSeleccionado = QLabel(PopUp_InsertarID)
        self.lb_modeloSeleccionado.setObjectName(u"lb_modeloSeleccionado")
        self.lb_modeloSeleccionado.setGeometry(QRect(210, 30, 131, 16))
        self.lb_modeloSeleccionado.setAlignment(Qt.AlignCenter)

        self.retranslateUi(PopUp_InsertarID)

        QMetaObject.connectSlotsByName(PopUp_InsertarID)
    # setupUi

    def retranslateUi(self, PopUp_InsertarID):
        PopUp_InsertarID.setWindowTitle(QCoreApplication.translate("PopUp_InsertarID", u"ID NUEVAS CAMARAS", None))
        self.label.setText(QCoreApplication.translate("PopUp_InsertarID", u"Introduzca ID:", None))
        self.label_2.setText(QCoreApplication.translate("PopUp_InsertarID", u"N\u00famero de ID restantes:", None))
        self.lb_idRestantes.setText(QCoreApplication.translate("PopUp_InsertarID", u"0", None))
        self.bt_confirmar.setText(QCoreApplication.translate("PopUp_InsertarID", u"Confirmar", None))
        self.label_3.setText(QCoreApplication.translate("PopUp_InsertarID", u"Modelo seleccionado:", None))
        self.lb_modeloSeleccionado.setText(QCoreApplication.translate("PopUp_InsertarID", u"-", None))
    # retranslateUi

