import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ExcelUi(QWidget):
    def __init__(self):
        super(ExcelUi, self).__init__()
        self.initUI()

    def initUI(self):

        self.resize(1100, 800)
        self.tableWidget = QTableWidget()
        vlayout = QVBoxLayout()
        # self.wheelEvent(self, event: QWheelEvent)
        hlayout = QHBoxLayout()
        self.UndopushButton = QPushButton()
        VSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #用于显示文本的
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("用于显示文本内容lineEdit")
        self.UndopushButton.setText("撤销")

        self.pushButton2 = QPushButton()
        self.pushButton2.setText("提交")
        hlayout.addWidget(self.UndopushButton)
        hlayout.addItem(VSpacer)
        hlayout.addWidget(self.pushButton2)
        hlayout.addItem(VSpacer)
        hlayout.addItem(VSpacer)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.lineEdit)
        vlayout.addWidget(self.tableWidget, Qt.AlignCenter)
        self.setLayout(vlayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ExcelUi()
    mw.show()
    app.exec_()