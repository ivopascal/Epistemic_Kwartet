# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kwartetsimple.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import main
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_NextTurnButton(object):
    def setupUi(self, NextTurnButton):
        NextTurnButton.setObjectName(_fromUtf8("NextTurnButton"))
        NextTurnButton.resize(1117, 879)
        self.gridLayout = QtGui.QGridLayout(NextTurnButton)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Player3Label = QtGui.QLabel(NextTurnButton)
        self.Player3Label.setObjectName(_fromUtf8("Player3Label"))
        self.gridLayout.addWidget(self.Player3Label, 4, 1, 1, 1)
        self.Player1Label = QtGui.QLabel(NextTurnButton)
        self.Player1Label.setMaximumSize(QtCore.QSize(16777215, 71))
        self.Player1Label.setObjectName(_fromUtf8("Player1Label"))
        self.gridLayout.addWidget(self.Player1Label, 4, 8, 1, 1)
        self.Plyr3_cards = QtGui.QLabel(NextTurnButton)
        self.Plyr3_cards.setObjectName(_fromUtf8("Plyr3_cards"))
        self.gridLayout.addWidget(self.Plyr3_cards, 4, 2, 1, 1)
        self.NextPointbttn = QtGui.QPushButton(NextTurnButton)
        self.NextPointbttn.setObjectName(_fromUtf8("NextPointbttn"))
        self.gridLayout.addWidget(self.NextPointbttn, 4, 9, 1, 1)
        self.StartBttn = QtGui.QPushButton(NextTurnButton)
        self.StartBttn.setObjectName(_fromUtf8("StartBttn"))
        self.gridLayout.addWidget(self.StartBttn, 4, 0, 1, 1)
        self.Plyr4_cards = QtGui.QLabel(NextTurnButton)
        self.Plyr4_cards.setObjectName(_fromUtf8("Plyr4_cards"))
        self.gridLayout.addWidget(self.Plyr4_cards, 5, 6, 1, 1)
        self.Plyr2_cards = QtGui.QLabel(NextTurnButton)
        self.Plyr2_cards.setObjectName(_fromUtf8("Plyr2_cards"))
        self.gridLayout.addWidget(self.Plyr2_cards, 1, 6, 1, 1)
        self.Plyr1_cards = QtGui.QLabel(NextTurnButton)
        self.Plyr1_cards.setObjectName(_fromUtf8("Plyr1_cards"))
        self.gridLayout.addWidget(self.Plyr1_cards, 4, 7, 1, 1)
        self.Player4Label = QtGui.QLabel(NextTurnButton)
        self.Player4Label.setObjectName(_fromUtf8("Player4Label"))
        self.gridLayout.addWidget(self.Player4Label, 6, 6, 1, 1)
        self.Player2Label = QtGui.QLabel(NextTurnButton)
        self.Player2Label.setObjectName(_fromUtf8("Player2Label"))
        self.gridLayout.addWidget(self.Player2Label, 0, 6, 1, 1)
        self.actionssn = QtGui.QAction(NextTurnButton)
        self.actionssn.setObjectName(_fromUtf8("actionssn"))

        self.retranslateUi(NextTurnButton)
        QtCore.QObject.connect(self.StartBttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr3_cards.update)
        QtCore.QObject.connect(self.StartBttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr2_cards.update)
        QtCore.QObject.connect(self.StartBttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr1_cards.update)
        QtCore.QObject.connect(self.StartBttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr4_cards.update)
        QtCore.QObject.connect(self.NextPointbttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr2_cards.update)
        QtCore.QObject.connect(self.NextPointbttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr1_cards.update)
        QtCore.QObject.connect(self.NextPointbttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr3_cards.update)
        QtCore.QObject.connect(self.NextPointbttn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Plyr4_cards.update)
        QtCore.QMetaObject.connectSlotsByName(NextTurnButton)

    def retranslateUi(self, NextTurnButton):
        NextTurnButton.setWindowTitle(_translate("NextTurnButton", "Form", None))
        self.Player3Label.setText(_translate("NextTurnButton", "<html><head/><body><p><span style=\" font-size:14pt; color:#0000ff;\">Player 3</span></p></body></html>", None))
        self.Player1Label.setText(_translate("NextTurnButton", "<html><head/><body><p><span style=\" font-size:14pt; color:#ff0000;\">Player 1</span></p></body></html>", None))
        self.Plyr3_cards.setText(_translate("NextTurnButton", "Player 3 Cards", None))
        self.NextPointbttn.setText(_translate("NextTurnButton", "Next Point", None))
        self.StartBttn.setText(_translate("NextTurnButton", "Start", None))
        self.Plyr4_cards.setText(_translate("NextTurnButton", "Player 4 Cards", None))
        self.Plyr2_cards.setText(_translate("NextTurnButton", "Player 2 Cards", None))
        self.Plyr1_cards.setText(_translate("NextTurnButton", "Player 1 Cards", None))
        self.Player4Label.setText(_translate("NextTurnButton", "<html><head/><body><p><span style=\" font-size:14pt; color:#ff5500;\">Player 4</span></p></body></html>", None))
        self.Player2Label.setText(_translate("NextTurnButton", "<html><head/><body><p><span style=\" font-size:14pt; color:#005500;\">Player 2</span></p></body></html>", None))
        self.actionssn.setText(_translate("NextTurnButton", "ssn", None))
        self.actionssn.setToolTip(_translate("NextTurnButton", "bg", None))

#import rsrc_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NextTurnButton = QtGui.QWidget()
    ui = Ui_NextTurnButton()
    ui.setupUi(NextTurnButton)
    NextTurnButton.show()
    NextTurnButton.update
    sys.exit(app.exec_())

