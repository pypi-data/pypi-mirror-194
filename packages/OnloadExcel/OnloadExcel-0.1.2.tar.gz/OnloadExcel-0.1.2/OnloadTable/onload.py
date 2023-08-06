import traceback
from PyQt5.QtWidgets import *
import sys
try:
    from Ui.onloadUi import *
    from Function.mysqlexcel import SqlResultWin
    from Function.optionDb import getOption, InsertDb
except:
    from .Ui.onloadUi import *
    from .Function.mysqlexcel import SqlResultWin
    from .Function.optionDb import getOption, InsertDb
from PyQt5.QtCore import *
import pandas as pd
from PyQt5.QtGui import *
import os, re
import PyQt5
from PyQt5.QtGui import *
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"E:\000工作\NewPDfSplit\pyhton3864\Lib\site-packages\PyQt5\Qt5\plugins"
from clazz import demo
#创建遮罩层
class MaskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(255,255,255, 100);')
        self.setAttribute(Qt.WA_DeleteOnClose)

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        if self.parent() is None:
            return
        parent_rect = self.parent().geometry()
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()

#创建执行代码的线程
# class runThread(QThread):
#     def __init__(self, communication):
#         self.communication = communication
#
#     def run(self):
#         pass

class OnLoadWin(QMainWindow, Ui_Onload, demo.TableObject):
    style = '''
QPushButton{
background-color:rgb(217, 217, 217)
}  
QMessageBox::button::hover{
    color:#fff;
}
 QPushButton#btn1 {
    height: 50px;
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #8a9195, stop: 1 balck);
    color: white;
    border-radius: 5px;
    font-size: 20px;
    font-weight:bold;
}

QPushButton#btn1:hover {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #7d8488, stop: 1 balck);
}

QPushButton#btn1:pressed {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #6a7073, stop: 1 balck);
}

QPushButton#btn2 {
    height: 50px;
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #47a7ed, stop: 1 #a967b2);
    color: white;
    border-radius: 25px;
    font-size: 20px;
    font-weight:bold;

}

QPushButton#btn2:hover {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #459ee0, stop: 1 #995da1);
}

QPushButton#btn2:pressed {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #4093d1, stop: 1 #87538e);
}
    '''
    #更新表格的信号
    updateTableSignal = pyqtSignal(PyQt5.QtWidgets.QTableWidget)
    def __init__(self, parent=None):
        super(OnLoadWin, self).__init__()
        #隐藏标题
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.header = None
        #获取Excel数据的内容
        self.table = ""
        #主窗口对象
        self.MainWin = parent
        self.defualtSheetName = "Sheet1"
        self.setMinimumSize(360, 271)
        self.setMaximumSize(960, 271)
        self.setupUi(self)
        self.table = QTableWidget()
        # 标题的之前的Y坐标
        self.TitleOldY = self.title.pos().y()
        # 获取之前窗口高度
        self.oldWindowY = self.height()
        self.oldWindowX = self.width()
        # 获取文件路径的位置
        self.filepathPos = self.filepath.pos()
        # 获取开始行数的位置
        self.startColPos = self.startCol.pos()
        # 获取总行数的位置
        self.sumColPos = self.sumCol.pos()
        # 获取模式的位置
        self.modelPos = self.model.pos()
        # 获取文件路径的输入框位置
        self.filepathEditPos = self.filepathEdit.pos()
        self.startColEditPos = self.startColEdit.pos()
        #设置开始列输入框可以输入的内容
        self.startColEdit.setValidator(QRegExpValidator(QtCore.QRegExp("[0-9]{1,4}"), self))
        self.sumColEditPos = self.sumColEdit.pos()
        #设置总列数输入框可以输入框的内容
        self.sumColEdit.setValidator(QRegExpValidator(QtCore.QRegExp("[0-9]{1,4}"), self))
        self.pushButtonPos = self.pushButton.pos()
        self.checkBoxPos = self.checkBox.pos()
        self.sureButtonPos = self.sureButton.pos()
        self.SheetNamePos = self.SheetName.pos()
        self.SheetNameEditPos = self.SheetNameEdit.pos()
        self.setStyleSheet(self.style)
        self.sureButton.clicked.connect(self.startExcel)
        self.pushButton.clicked.connect(self.file_cho)
        #更新表格的信号量
        self.updateTableSignal.connect(self.updateTable)
        self.UiInit()
        self.checkBox.clicked.connect(self.DefaultOrCustomize)
        self.DefaultOrCustomize()
        self.DefaultCode = True
        self.sumColTip.setVisible(False)
        self.startColTip.setVisible(False)
        self.filepathTip.setVisible(False)
        self.Frist = True
        self.FunctionName = "上传底稿目录"
        self.describetion = '''
=================================================
这是上传底稿目录的功能
=================================================
        '''

    #默认模式或者是自定义模式
    def DefaultOrCustomize(self):
        print("验证CheckBox的点击事件")
        if self.checkBox.isChecked():
            self.defaultRead()
            self.DefaultCode = True
        else:
            self.customizeRead()
            self.DefaultCode = False

    #默认读取模式
    def defaultRead(self):
        self.sumColTip.setVisible(False)
        self.startColTip.setVisible(False)
        self.SheetName.setVisible(False)
        self.SheetNameEdit.setVisible(False)
        self.startCol.setVisible(False)
        self.startColEdit.setVisible(False)
        self.sumCol.setVisible(False)
        self.sumColEdit.setVisible(False)
        self.filepathTip.setVisible(False)

        self.model.setGeometry(QtCore.QRect(200, 160, 61, 20))
        self.checkBox.setGeometry(QtCore.QRect(300, 160, 61, 20))
        self.sureButton.setGeometry(QtCore.QRect(460, 160, 121, 20))

    #自定义模式
    def customizeRead(self):
        self.sumColTip.setVisible(False)
        self.startColTip.setVisible(False)
        self.SheetName.setVisible(True)
        self.SheetNameEdit.setVisible(True)
        self.startCol.setVisible(True)
        self.startColEdit.setVisible(True)
        self.sumCol.setVisible(True)
        self.sumColEdit.setVisible(True)
        self.filepathTip.setVisible(False)
        self.model.setGeometry(QtCore.QRect(200, 230, 61, 20))
        self.checkBox.setGeometry(QtCore.QRect(300, 230, 61, 20))
        self.sureButton.setGeometry(QtCore.QRect(460, 230, 121, 20))


    def UiInit(self):
        ui_list = getOption("Tablepath")
        # 判断类型
        if isinstance(ui_list, list):
            if len(ui_list) == 1:
                ui_tuple = ui_list[0]
                self.filepathEdit.setText(ui_tuple[1])
                self.SheetNameEdit.setText(ui_tuple[2])
                self.startColEdit.setText(ui_tuple[3])
                self.sumColEdit.setText(ui_tuple[4])
                if not ui_tuple[5]:
                    self.checkBox.setChecked(True)
                else:
                    if not int(ui_tuple[5]):
                        self.checkBox.setChecked(True)
                    else:
                        self.checkBox.setChecked(False)
        elif isinstance(ui_list, str):
            pass
        else:
            self.textEdit.setText(str(ui_list))

    #更新数据表的数据
    def updateTable(self, table):
        self.table = table
        # print(table)
        symbolpattern = re.compile('["/\\\\:*?<>|]')
        #判断表格内容中是否包含特殊符号
        ContainSymbol = 0
        colscount = self.table.columnCount()
        # 表格的行数
        rowcount = self.table.rowCount()
        model = self.table.model()
        for row in range(rowcount):
            for col in range(4):
                word = model.data(model.index(row, col))
                # print(word)
                # print(type(word))
                if word:
                    result = re.findall(symbolpattern, word)
                    if len(result):
                        ContainSymbol = 1

        #从Excel获取返回的内容
        print("onload返回内容")
        #如果不包含特殊符号，并且是由主窗口打开
        print(self.MainWin)
        print(ContainSymbol)
        if self.MainWin and not ContainSymbol:
            print("更新表格函数")
            #将底稿目录的内容传递到主窗口内
            self.MainWin.tableSignal.emit(table, self.filePath)
            #上传底稿成功显示成功的提示框，并将底稿目录的文件位置进行设置
            # QMessageBox.question(self, "information", "上传底稿目录成功", QMessageBox.Ok)
            self.MainWin.MessageSignal.emit("information", "\n上传底稿目录成功")
            #底稿目录上传成功后，关闭加载表格的界面。
            self.mw.close()

        else:
            # print("asdasdasdas")
            #底稿目录中包含有特殊符号信息提示框
            self.MainWin.MessageSignal.emit("warning", "\n底稿目录中包含特殊符号")

    def file_cho(self):
        self.file_name1 = QFileDialog.getOpenFileName(self, "选取文件", "./", "Excel Files (*.xlsx)")[0]
        if self.file_name1:
            self.filepathEdit.setText(self.file_name1)

    #警告框
    def showDialog(self, word):
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(QLabel('<font color="red">{}</font>'.format(word)))
        dialog.setLayout(dialog_layout)
        mask = MaskWidget(self)
        mask.show()
        dialog.exec()
        mask.close()
        self.show()

    def startExcel(self):
        # 获取文件路径输入内容
        # self.filePath = self.filepathEdit.text()
        # #判断文件路径是否存在
        # if not os.path.isfile(self.filePath):
        #     print("文件路径不存在")
        #     return
        self.sumColTip.setVisible(False)
        self.filepathTip.setVisible(False)
        self.startColTip.setVisible(False)
        if self.checkBox.isChecked():
            self.CheckStatu = "0"
        else:
            self.CheckStatu = '1'
        checkTuple = ("Tablepath", self.filepathEdit.text(), self.SheetNameEdit.text(), self.startColEdit.text(), self.sumColEdit.text(), self.CheckStatu)
        g = InsertDb(checkTuple)
        #警告框
        SheetName = self.SheetNameEdit.text()
        TablePath = self.filepathEdit.text()
        if self.filepathEdit.text() == "":
            self.filepathTip.setText("请输入底稿目录文件位置!")
            self.filepathTip.setVisible(True)
            return
        if not os.path.isfile(self.filepathEdit.text()):
            self.filepathTip.setText("底稿目录文件不存在!")
            self.filepathTip.setVisible(True)
            return
        if not self.filepathEdit.text().endswith(".xlsx"):
            self.filepathTip.setText("底稿目录文件后缀名不正确!")
            self.filepathTip.setVisible(True)
            return
        print("TablePath为：", end ="")
        print(TablePath)
        # 判断复选款的选择状态。
        if self.checkBox.isChecked():
            defualt = 1
            colindex = 0
            colcount = 3
            if not TablePath:
                self.filePath = r"C:\Users\wangsa\Desktop\表\斯菱股份底稿目录1.xlsx"
            else:
                self.filePath = TablePath
            undostep = 10
        else:
            defualt = 0
            if len(self.startColEdit.text()) == 0:
                self.startColTip.setVisible(True)
                return
            if len(self.sumColEdit.text()) == 0:
                self.sumColTip.setVisible(True)
                return
            colindex = int(self.startColEdit.text())
            colcount = int(self.sumColEdit.text())
            print(colindex, colcount)
            if not TablePath:
                self.filePath = r"C:\Users\wangsa\Desktop\表\斯菱股份底稿目录1.xlsx"
            else:
                self.filePath = TablePath
            print(self.filePath)
            undostep = 10
        try:
            if SheetName:
                self.SheetIsExist(self.filePath, SheetName)
                self.mw = SqlResultWin(self.filePath, undostep, colindex, colcount, defualt, self ,SheetName)
                self.mw.show()
            else:
                self.SheetIsExist(self.filePath)
                self.mw = SqlResultWin(self.filePath, undostep, colindex, colcount, defualt, self)
                self.mw.show()

        except Exception as e:
            if "not found" in str(e):
                self.MainWin.MessageSignal.emit("warning", "\nExcel文件中表不存在")
                print("判断Excel文件中表是否存在")
            print(str(e))
            traceback.print_exc()
        # print(self.table.columnCount())
        print(22222222222222222222222222)
        print(self.table)
        #表格的列数
        colscount = self.table.columnCount()
        #表格的行数
        rowcount = self.table.rowCount()
        # for row in rowcount:
        #     for col in colscount:

    # 判断Sheet是否存在
    def SheetIsExist(self, filepath, sheet_name="Sheet1"):
        df = pd.read_excel(filepath, sheet_name=sheet_name, engine="openpyxl", header=self.header)

    def resizeEvent(self, event):
        # 重置标题的位置
        if not self.Frist :
            title_x = (self.width() - self.title.size().width()) / 2
            title_y = self.TitleOldY
            self.title.move(int(title_x), int(title_y))

            # 设置文件路径位置位置
            filepath_x = (self.width() - self.oldWindowX) / 2 + self.filepathPos.x()
            filepath_y = self.filepathPos.y()
            self.filepath.move(int(filepath_x), int(filepath_y))

            # 设置开始行数文本位置
            startCol_x = (self.width() - self.oldWindowX) / 2 + self.startColPos.x()
            # startCol_y = self.height() / self.oldWindowY * self.startColPos.y()
            startCol_y = self.startColPos.y()
            self.startCol.move(int(startCol_x), int(startCol_y))

            # 设置总行数文本位置
            sumCol_x = (self.width() - self.oldWindowX) / 2 + self.sumColPos.x()
            sumCol_y = self.sumColPos.y()
            self.sumCol.move(int(sumCol_x), int(sumCol_y))

            # 设置模式文本位置
            model_x = (self.width() - self.oldWindowX) / 2 + self.modelPos.x()
            model_y = self.modelPos.y()
            self.model.move(int(model_x), int(model_y))

            filepathEdit_x = (self.width() - self.oldWindowX) / 2 + self.filepathEditPos.x()
            filepathEdit_y = self.filepathEditPos.y()
            self.filepathEdit.move(int(filepathEdit_x), int(filepathEdit_y))

            startColEdit_x = (self.width() - self.oldWindowX) / 2 + self.startColEditPos.x()
            startColEdit_y = self.startColEditPos.y()
            self.startColEdit.move(int(startColEdit_x), int(startColEdit_y))

            sumColEdit_x = (self.width() - self.oldWindowX) / 2 + self.sumColEditPos.x()
            sumColEdit_y = self.sumColEditPos.y()
            self.sumColEdit.move(int(sumColEdit_x), int(sumColEdit_y))

            pushButton_x = (self.width() - self.oldWindowX) / 2 + self.pushButtonPos.x()
            pushButton_y = self.pushButtonPos.y()
            self.pushButton.move(int(pushButton_x), int(pushButton_y))

            checkBox_x = (self.width() - self.oldWindowX) / 2 + self.checkBoxPos.x()
            checkBox_y = self.checkBoxPos.y()
            self.checkBox.move(int(checkBox_x), int(checkBox_y))

            sureButton_x = (self.width() - self.oldWindowX) / 2 + self.sureButtonPos.x()
            sureButton_y = self.sureButtonPos.y()
            self.sureButton.move(int(sureButton_x), int(sureButton_y))

            SheetName_x = (self.width() - self.oldWindowX) / 2 + self.SheetNamePos.x()
            SheetName_y = self.SheetNamePos.y()
            self.SheetName.move(int(SheetName_x), int(SheetName_y))

            SheetNameEdit_x = (self.width() - self.oldWindowX) / 2 + self.SheetNameEditPos.x()
            SheetNameEdit_y = self.SheetNameEditPos.y()
            self.SheetNameEdit.move(int(SheetNameEdit_x), int(SheetNameEdit_y))
        else:
            self.Frist = False

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = OnLoadWin()
    myWin.show()
    sys.exit(app.exec_())