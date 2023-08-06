
from itertools import product
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from openpyxl import Workbook
import re
from .Ui.ExcelUi import ExcelUi
from .settings import rows, cols
import pandas  as pd
from .settings import undostep
import traceback
from .Ui.MaskWin import MaskWidget


#导入建文件夹的类用于

class SqlResultWin(ExcelUi):
    # 生成默认dataframe。默认使用的行为0，默认使用行的数量为1, 是否使用默认判断模式
    def __init__(self, filepath, undostep=2, colindex=0, colcount=1, default=1, parent=None, sheet_name="Sheet1"):
        super(SqlResultWin, self).__init__()
        # self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        # 将父类传递过来
        self.parent = parent
        # 是否通过退格符对文本内容进行修改
        self.BackspaceCode = 0
        self.KeyBoardLocationList = []
        self.keyBoardWordList = []
        # 来自点击修改数据
        self.clickPositonCode = 0
        # 选中区域通过键盘对文本进行修改
        self.keyboardCode = 0
        # 单击的单元格行位置
        self.clickCellRow = 0
        # 单击的单元格列位置
        self.clickCellCol = 0
        # 单击的单元格的内容
        self.clickCellText = ""
        # 单元修改的内容是否来自于Ctrl+V
        self.CtrlVCode = 0
        # 设置保存撤销步骤的列表
        self.undoStepList = []
        # 撤销步骤的数量
        self.undostep = undostep
        # 最后一次操作
        self.FinalStep = ""
        # 中文索引列表
        self.chineseNumList = ['一', '二', '三', '四', '五', '六', '七', '八', "九"]
        # 需要使用的col的索引
        self.colindex = colindex
        # 默认要打开工作表的sheet名字
        self.sheet_name = sheet_name
        # 要使用索引的列的数量
        self.colcount = colcount
        # 是否使用默认模式
        self.default = default
        # 记录上一次的鼠标事件
        self.beforeButtonEvent = ''
        self.backgroundList = []
        # 剪切板对象
        self.clipboard = QApplication.clipboard()
        self.text = str()
        results = [[1, 2, 3], [11, 12, 13], [11, 12, 14], [11, 12, 13], [11, 12, 13]]
        # 头包含字符的列表
        HeaderWordList = [chr(i) for i in range(65, 91)]
        table_row = len(results)
        self.header = None
        cnt_cols = 3
        # 列数
        columnLen = cols
        rowlen = rows
        # dfcols为总列数
        self.df, dfrows, dfcols = self.getExcelDf(filepath)
        print(self.df)
        print(dfrows, dfcols)
        # 开始列的索引

        if self.colcount + self.colindex > dfcols:
            self.colcount = dfcols - self.colindex
        print(self.colcount)
        print(self.colindex)
        # 列名字列表
        list_cols = [self.xun(i, HeaderWordList) for i in range(columnLen)]
        # 设置行数
        self.tableWidget.setRowCount(dfrows)
        # self.tableWidget.setRowCount(dfrows)  # 一定要设置行数，否则不会显示出tableWidget
        # 设置列的数量
        self.tableWidget.setColumnCount(columnLen)
        # 设置控件水平的标签
        self.tableWidget.setHorizontalHeaderLabels(list_cols)  # 先设置列数后，设置表头才能生效
        # 获得QTableWidget表格控件的表格头，
        self.tableWidget.horizontalHeader().setStyleSheet("color: #00007f")
        # self.tableWidget.setAlternatingRowColors(True)  # 设置行背景颜色交替

        self.tableWidget.setStyleSheet("border: 0px; alternate-background-color: #C9E4CC")
        # 设置文本右键菜单功能
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 运行右键产生子菜单
        # 设置文本信号连接文本的右键菜单
        self.tableWidget.customContextMenuRequested.connect(self.showMenu)

        # 设置水平头连接右键菜单
        self.tableWidget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # 设置水平头连接到鼠标右键
        self.tableWidget.horizontalHeader().customContextMenuRequested.connect(self.showHHeadMenu)

        # 设置垂直标题的右键菜单
        self.tableWidget.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.verticalHeader().customContextMenuRequested.connect(self.showVMenu)

        # 文本菜单
        self.contextMenu = QMenu(self.tableWidget)
        # 文本复制所选的内容
        self.cpaction = self.contextMenu.addAction('复制所选内容Ctrl+C')
        # 文本删除行
        self.delaction = self.contextMenu.addAction('清空所选区域内容Backspace')
        # 文本导出功能
        self.expaction = self.contextMenu.addAction('导出全部Ctrl+E')
        # 文本粘贴
        self.paste = self.contextMenu.addAction("黏贴Ctrl+V")

        # 水平头菜单
        self.headMenu = QMenu(self.tableWidget)
        # 水平头部复制功能
        self.headcpaction = self.headMenu.addAction("复制(c)    Ctrl+C")
        # 水平头部删除行
        self.headcpaction = self.headMenu.addAction("清空所选区域内容Backspace")
        self.headcpaction.triggered.connect(self.bakSpace)
        # 垂直头菜单
        self.VheadMenu = QMenu(self.tableWidget)
        self.vdel = self.VheadMenu.addAction("清空所选区域内容Backspace")

        self.vdel.triggered.connect(self.bakSpace)
        # self.headcpaction.triggered.connect(self.table_copy)
        self.cpaction.triggered.connect(self.table_copy)
        self.delaction.triggered.connect(self.bakSpace)
        self.paste.triggered.connect(self.clipboard_insert)
        self.expaction.triggered.connect(lambda: self.export(list_cols))
        # self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.clicked.connect(self.click_position)

        # 匹配特殊符号
        symbolpattern = re.compile('["/\\\\:*?<>|]')
        # 匹配索引正则
        indexpattern = re.compile("(\d{0,2}-)*(\d){1,2}")
        # 匹配索引以及对应的标题
        indexTxtpattern = re.compile("(\d{0,2}-)*(\d){1,2}([^\d])?[\u4e00-\u9fa5]*")
        # 匹配包含第N章内容标题
        titlepattern = re.compile('第(\s)*([一,二,三,四,五,六,七,八,九,十]{1,3})(\s)*章')

        #
        if self.default:
            self.colcount = dfcols
            self.colindex = 0
        else:
            dfcols = self.colcount

        if self.colcount != 1:
            self.tableLists = self.df.iloc[:, self.colindex: self.colindex + self.colcount].values.tolist()
            print(self.tableLists)
            x = 0
            for row in self.tableLists:
                for y in range(dfcols):
                    # 匹配字符串中是否包含特殊符号
                    result = re.findall(symbolpattern, str(row[y]))
                    # 匹配索引正则的匹配内容
                    indexResult = re.match(indexpattern, str(row[y]))
                    # 匹配索引以及对应的标题的结果
                    indexTxtResult = re.match(indexTxtpattern, str(row[y]))
                    # 匹配包含第N章内容标题的结果
                    titleResult = re.match(titlepattern, str(row[y]))
                    # 创建TableItem
                    item = QTableWidgetItem(str(row[y]).strip())
                    # 如果包含特殊符号，那么输出特殊符号列表
                    if len(result) > 0:
                        item.setBackground(QColor(0, 255, 0))
                        # print(result)
                    # if not str(row[y]).strip():
                    #     item.setBackground(QColor(255, 0, 0))
                    # tableWidget设置值的时候需要使用setItem， 其包括三个参数，第一个参数为所在行，第二参数为要设置所在列， 第三个为所传递值， 传递值的时候需要使用到QTableWidgetItem类
                    self.tableWidget.setItem(x, y, item)

                x += 1
        else:

            # 匹配序号和行标题内容都在统一个单元格的情况
            self.tableLists = self.df.iloc[:, self.colindex].tolist()
            print(self.tableLists)
            # 生成需要表的复制表，复制表用于修改已经写入过的内容避免重复。
            self.tableListsCopy = self.tableLists.copy()
            # 创建用于生成菜单的列表的复制
            self.menutablelist = self.tableLists.copy()
            for i in self.tableLists:
                # 匹配索引以及对应的标题的结果
                print(i)
                if i:
                    # 进行匹配索引的文本的匹配判断
                    indexTxtResult = re.match(indexTxtpattern, i.strip())
                    # 匹配中文的第*章的索引
                    titleResult = re.match(titlepattern, i.strip())
                    if indexTxtResult:
                        indexResult = re.match(indexpattern, i)
                        # 匹配到的标题结果
                        tableIndex = indexResult.group()
                        item = QTableWidgetItem(tableIndex.strip())
                        # 匹配关键字所处位的索引位置
                        wordIndex = self.tableListsCopy.index(i)
                        result = re.findall(symbolpattern, i)
                        if len(result) > 0:
                            # item.setBackground(QColor(0, 255, 0))
                            pass
                        self.tableWidget.setItem(wordIndex, 0, item)
                        self.tableListsCopy[wordIndex] = ""  # 将已经保存过的内容重置为空

                        # 标题内容
                        vHead = i.replace(str(tableIndex), "")
                        print("标题内容", end = "")
                        print(vHead)
                        symbolresult = self.checkSymbol(i)
                        item = QTableWidgetItem(vHead.strip())
                        if symbolresult:
                            # print(symbolresult)
                            item.setBackground(QColor(0, 255, 0))
                        if len(vHead) < 1:
                            item.setBackground(QColor(255, 0, 0))
                        self.tableWidget.setItem(wordIndex, 1, item)

                    # 如果标题内容包含中文的第*章
                    elif titleResult:
                        # 获取第*章
                        word = titleResult.group(0)
                        # 获取中文数字
                        chineseIndex = titleResult.group(2).strip()
                        # 数字的索引
                        numIndex = self.chineseNum(chineseIndex)
                        wordIndex = self.tableListsCopy.index(i)
                        item = QTableWidgetItem(word.strip())
                        self.tableWidget.setItem(wordIndex, 0, item)
                        #
                        title = i.replace(word, "").strip()
                        item = QTableWidgetItem(title)
                        symbolresult = self.checkSymbol(title)
                        if symbolresult:
                            item.setBackground(QColor(0, 255, 0))
                            print(symbolresult)
                        self.tableWidget.setItem(wordIndex, 1, item)
                        self.tableListsCopy[wordIndex] = ""
                    else:
                        item = QTableWidgetItem(i)
                        item.setBackground(QColor(0, 255, 255))
                        wordIndex = self.tableListsCopy.index(i)
                        self.tableWidget.setItem(wordIndex, 0, item)
                        self.tableListsCopy[wordIndex] = ""

        # 单元格内容变化
        self.tableWidget.cellChanged.connect(self.wordchange)
        self.tableWidget.cellPressed.connect(self.tableCellPressed)
        # self.tableWidget.releaseMouse.connect(self.releaseEvent)
        self.tableWidget.cellDoubleClicked.connect(self.tableDoubleClicked)
        self.UndopushButton.clicked.connect(self.undoCtrlZ)
        # self.tableWidget.head

        if self.parent:
            self.pushButton2.clicked.connect(self.updateTable)

        self.getpathLong()

    #获取路径长度的函数
    def getpathLong(self):
        print("需要写路径长度的函数")

    #创建警告框的方法
    def showDialog(self, word):
        # dialog = QDialog(self)
        # dialog.setModal(True)
        # dialog_layout = QVBoxLayout()
        # dialog_layout.addWidget(QLabel('<font color="red">{}</font>'.format(word)))
        # dialog.setLayout(dialog_layout)
        #设置弹出提示警告框，
        QMessageBox.warning(self, "Warining", word, QMessageBox.Ok)
        mask = MaskWidget(self)
        mask.show()
        # dialog.exec()
        mask.close()
        self.show()

    #检查第一列数据是否为索引
    def checkColOne(self, word):
        #判断第一列中是否为数字和-的索引
        indexpattern = re.compile("(\d{0,2}-)*(\d){1,2}$")
        #判断第一列中是否为第几章类的索引
        titlepattern = re.compile('第(\s)*([一,二,三,四,五,六,七,八,九,十]{1,3})(\s)*章$')
        titleResult = re.match(titlepattern, word.strip())
        indexResult = re.match(indexpattern, word.strip())
        try:
            titleResult.group(1)
            return 1
        except:
            try:
                indexResult.group(2)
                return 1
            except:
                return 0

    #修改子页面中底稿目录的函数
    def updateTable(self):
        if self.parent:
            rows  = self.tableWidget.rowCount()
            model = self.tableWidget.model()
            #是否包含索引
            containsIndex = 0
            for row in range(rows):
                word = model.data(model.index(row, 0))
                if word:
                    containsIndex = containsIndex + self.checkColOne(word)
            if containsIndex:
                print("第一列中包含索引")
                self.parent.table = self.tableWidget
                #调用子页面中修改底稿目录的信号
                self.parent.updateTableSignal.emit(self.tableWidget)
            else:
                print('第一列中不包含索')
                self.showDialog("第一列中不包含索引")
        else:
            print("自执行")

    def tableDoubleClicked(self):
        # 当前点击行标
        row = self.tableWidget.currentRow()
        # 获取选中单元格的行
        # print(self.tableWidget.currentRow())
        # 当前点击列标
        # 获取选中单元格的列
        column = self.tableWidget.currentColumn()
        text = self.tableWidget.model().data(self.tableWidget.model().index(row, column))
        self.ClickLoctionList = [[row, column]]
        self.ClickWordList = [text]
        self.clickPositonCode = 1

    def tableCellPressed(self, row, col):
        self.clickCellCol = col
        self.clickCellRow = row
        try:
            content = self.tableWidget.item(row, col).text()
            self.clickCellText = content
        except:
            self.clickCellText = ""
        print("b")
        #输出表格的列数和行数
        print(self.tableWidget.rowCount())
        print(self.tableWidget.columnCount())

    # 匹配是否包含特殊符号，并返回匹配到的特殊符号的列表
    def checkSymbol(self, word):
        #
        symbolpattern = re.compile('["/\\\\:*?<>|]')
        #
        if word:
            # print("表格内容为：" + word)
            result = re.findall(symbolpattern, word)
            if result:
                return result

    def chineseNum(self, chineseIndex):
        # 判断中文的索引是否是以中文的十为开始
        if chineseIndex.startswith("十"):
            if chineseIndex != "十":
                wordIndex = 10 + self.chineseNumList.index(chineseIndex.replace("十", "")) + 1
            else:
                wordIndex = 10
            return wordIndex

        elif "十" in chineseIndex:
            numIndex = chineseIndex.replace("十", "")
            wordIndex = (self.chineseNumList.index(numIndex[0]) + 1) * 10 + self.chineseNumList.index(numIndex[1]) + 1
            return wordIndex

        else:
            wordIndex = self.chineseNumList.index(chineseIndex[0]) + 1
            return wordIndex

            # 获取需要用到的dataframe列表

    def getExcelDf(self, filepath):
        df = pd.read_excel(filepath, sheet_name=self.sheet_name, engine="openpyxl", header=self.header)
        df = df.fillna("")
        # print(df)
        return df, df.shape[0], df.shape[1]

    # 寻找头标题
    def xun(self, num, word_list):
        result = num // 26
        remainder = num % 26

        if 0 < result < 26:
            title = word_list[result - 1] + word_list[remainder]
            return title

        elif result == 0:
            title = word_list[remainder]
            return title

    # 显示文本菜单列表
    def showMenu(self, pos):  # 右键展示菜单，pos 为鼠标位置
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
        # row_num = -1
        # for i in self.tableWidget.selectionModel().selection().indexes():
        #     row_num = i.row()
        #
        # if row_num < 3:

    # 显示水平头菜单
    def showHHeadMenu(self, pos):
        self.headMenu.exec_(QCursor.pos())

    # 显示垂直菜单列表
    def showVMenu(self, qpoint: QPoint):
        self.tbl_item = item = self.tableWidget.itemAt(qpoint)
        self.tbl_item_pos = [item.row(), item.column()]
        rangerow, rangecol = item.row(), item.column()
        # self.tableWidget.clearSelection()
        self.tbl_selection = QTableWidgetSelectionRange(rangerow, 0, rangerow, self.tableWidget.columnCount() - 1)
        selectRect = self.tableWidget.selectedRanges()
        set_indices = set()
        for rect in selectRect:  # 获取范围边界
            for row in range(rect.topRow(), rect.bottomRow() + 1):
                set_indices.add(row)  # 获取被选中的行号（顺序是被依次选中的顺序）
                # print(row)
        # 选中的行号
        # print(set_indices)
        # if len(row)
        self.tableWidget.setRangeSelected(self.tbl_selection, True)
        self.VheadMenu.exec_(self.tableWidget.viewport().mapToGlobal(qpoint))

    # 获取当前选择的行和列
    def click_position(self):
        """
        表格控件点击信号绑定的槽函数
        :return: None
        """

        # 当前点击行标
        row = self.tableWidget.currentRow()
        # 获取选中单元格的行
        # print(self.tableWidget.currentRow())
        # 当前点击列标
        # 获取选中单元格的列
        column = self.tableWidget.currentColumn()
        # print('当前位置: (%s, %s)' % (row, column))
        text = self.tableWidget.model().data(self.tableWidget.model().index(row, column))
        symbolResult = self.checkSymbol(text)

        if symbolResult:
            text = "包含特殊字符：" + " , ".join(symbolResult) + "    " + text
        self.lineEdit.setText(text)

    def location(self):
        # print("---------------------------")
        self.keyBoardWordList = []
        self.KeyBoardLocationList = []
        try:
            model = self.tableWidget.model()
            selectRect = self.tableWidget.selectedRanges()
            # set_indices = set()
            for rect in selectRect:  # 获取范围边界
                for row in range(rect.topRow(), rect.bottomRow() + 1):
                    for col in range(rect.leftColumn(), rect.rightColumn() + 1):
                        # rect = selectRect[-1]  # 获取范围边界
                        # row = rect.bottomRow()
                        # col = rect.rightColumn()
                        word = model.data(model.index(row, col))
                        self.keyBoardWordList.append(word)
                        self.KeyBoardLocationList.append([row, col])
            # #print(cellLoctionList)
            self.keyboardCode = 1
            # print("修改区域完整坐标")
            # print(self.keyBoardWordList)
            # print(self.KeyBoardLocationList)

        except:
            traceback.print_exc()

    # 字符修改
    def wordchange(self):
        if self.BackspaceCode:
            print("BackspaceCode")
        if self.CtrlVCode:
            self.CtrlVCode = 0
            pass
        else:
            # print("文本被修改")
            if self.keyboardCode:
                model = self.tableWidget.model()
                print(self.KeyBoardLocationList)
                if len(self.KeyBoardLocationList) != 0:
                    newWord = model.data(model.index(self.KeyBoardLocationList[-1][0], self.KeyBoardLocationList[-1][1]))
                    oldWord = self.keyBoardWordList[-1]
                    # print(oldWord)
                    if not newWord == oldWord == None:
                        if not (newWord != "" and self.KeyBoardLocationList == None):
                            if newWord.strip() != oldWord:

                                print(newWord)
                                print(self.KeyBoardLocationList)
                                try:
                                    symbolpattern = re.compile('["/\\\\:*?<>|]')
                                    result = re.findall(symbolpattern, newWord)
                                    if len(result) > 0:
                                        self.tableWidget.item(self.KeyBoardLocationList[0][0],self.KeyBoardLocationList[0][1]).setBackground(QColor(0, 255, 0))
                                    else:
                                        self.tableWidget.item(self.KeyBoardLocationList[0][0],self.KeyBoardLocationList[0][1]).setBackground(QColor(255, 255, 255))
                                except:
                                    traceback.print_exc()
                                self.addDo([self.KeyBoardLocationList, self.keyBoardWordList], "update")
                    print(self.KeyBoardLocationList)
                    if len(self.KeyBoardLocationList) > 0:
                        newWord = model.data(model.index(self.KeyBoardLocationList[0][0], self.KeyBoardLocationList[0][1]))
                        # print(newWord)
                        oldWord = self.keyBoardWordList[0]
                        # print(oldWord)
                        if not newWord == oldWord == None:
                            if not (newWord != "" and self.KeyBoardLocationList == None):
                                if newWord.strip() != oldWord:
                                    self.addDo([self.KeyBoardLocationList, self.keyBoardWordList], "update")
                        self.keyboardCode = 0
                        self.KeyBoardLocationList = []
                        self.keyBoardWordList = []

            if self.clickPositonCode:
                print(self.ClickWordList)
                print(self.ClickLoctionList)
                model = self.tableWidget.model()
                word = model.data(model.index(self.ClickLoctionList[0][0],self.ClickLoctionList[0][1]))
                print(word)
                try:
                    symbolpattern = re.compile('["/\\\\:*?<>|]')
                    result = re.findall(symbolpattern, word)
                    if len(result) > 0:
                        self.tableWidget.item(self.ClickLoctionList[0][0],self.ClickLoctionList[0][1]).setBackground(QColor(0, 255, 0))
                    else:
                        self.tableWidget.item(self.ClickLoctionList[0][0],self.ClickLoctionList[0][1]).setBackground(QColor(255, 255, 255))
                except:
                    traceback.print_exc()
                self.addDo([self.ClickLoctionList, self.ClickWordList], "update")
                self.ClickWordList = []
                self.ClickLoctionList = []
                self.clickPositonCode = 0
            else:
                self.ClickWordList = []
                self.ClickLoctionList = []
                self.clickPositonCode = 0

    # 粘贴复制的excel内容
    def clipboard_insert(self):
        # 创建复制内容的列表
        cp_list = []
        # 获取剪切板的内容
        clip_data = QApplication.clipboard().text()
        # print(clip_data)
        if clip_data:
            # #print(self.tableWidget.selectedItems())

            selectRect = self.tableWidget.selectedRanges()
            # print(self.tableWidget.selectedRanges())
            # set_indices = set()
            # set_cols = set()
            # for rect in selectRect:
            #     # 获取范围边界
            #     for row in range(rect.topRow(), rect.bottomRow() + 1):
            #         set_indices.add(row)  # 获取被选中的行号（顺序是被依次选中的顺序）
            #         #print(row)
            # for col in range()
            # 设置垂直某行的标签内容
            # self.tableWidget.setVerticalHeaderItem(4, QTableWidgetItem("asdasdasd"))
            # self.tableWidget.takeItem(1,2)
            # 将剪切板中包含的\r\n 替换为\n
            # 将剪切板内容中的\r\n 全部替换为\n
            clip_data = re.sub("\r\n", "\n", clip_data)
            # print(clip_data)
            # 保存修改单元格的列表
            cellLoctionList = []
            # 保存修改前单元格旧值的列表
            cellOldWordList = []
            # 按行将数据分割为一个列表，判断复制的内容中是否包含\n。如果包含\n那么复制的内容将被转化为list进行处理，负责将会被当做字符串进行处理。判断复制的内容是否
            if "\n" in clip_data and len(clip_data.split("\n")) > 1 and clip_data.split("\n")[1]:
                if clip_data.endswith("\n"):
                    cp_data = re.split("\n", clip_data)[:-1]
                else:
                    cp_data = re.split("\n", clip_data)
                # print(cp_data)
                # 将每一行的数据进行分割
                for i in cp_data:
                    item = re.split("\t", i)
                    cp_list.append(item)

                # 粘贴信息的行
                cp_row = len(cp_list)
                # 粘贴信息的列
                cp_col = len(cp_list[0])
                # print(cp_row)
                # print(cp_col)
                # #print(cp_list)
                if cp_list[0] == [""]:
                    return
                # 当前光标所属的行
                # row = self.tableWidget.currentIndex().row()
                # #行数量
                # row_count = self.tableWidget.rowCount()
                # #当前光标所属的列
                # col = self.tableWidget.currentIndex().column()
                # 区域最左边的列当做插入开始的列
                col = selectRect[0].leftColumn()

                # 区域最上面的列当做插入开始行
                row = selectRect[0].topRow()
                #
                if row < 0:
                    row = 0
                elif col < 0:
                    col = 0
                # 写入数据
                model_ax = self.tableWidget.model()
                print("model_ax的值为： " + str(model_ax))
                row_count = model_ax.rowCount()
                print("model_ax.RowCount的值为:  " + str(row_count))
                # cp_row 为复制的内容行的数量
                if row_count - row < cp_row:
                    add_row = cp_row - (row_count - row)
                    model_ax.insertRows(row_count, add_row)
                # model_ax.insertRows()
                # 按区域修改内容
                model = self.tableWidget.model()
                symbolpattern = re.compile('["/\\\\:*?<>|]')
                for i in range(cp_row):
                    for x in range(cp_col):
                        word = str(cp_list[i][x])
                        cellOldWordList.append(model.data(model.index(i + row, x + col)))
                        self.CtrlVCode = 1
                        item = QTableWidgetItem(word)
                        result = re.findall(symbolpattern, word)
                        if len(result) > 0:
                            item.setBackground(QColor(0, 255, 0))
                        self.tableWidget.setItem(i + row, x + col, item)
                        cellLoctionList.append([i + row, x + col])
                # print(cellLoctionList)
                self.addDo([cellLoctionList, cellOldWordList], "update")

                # 为undoStack添加新的修改表格的位置以及单元格修改之前的内容，单元格操作的步骤类型为修改,保存单元格撤销操作的列表, 以及最大撤销步骤限制的数量
                # 设置选中区域的对象
                self.tableWidget.clearSelection()
                newRange = QTableWidgetSelectionRange(row, col, row + cp_row - 1, col + cp_col - 1)
                # 重置选定区域
                self.tableWidget.setRangeSelected(newRange, True)
            else:
                selectRect = self.tableWidget.selectedRanges()
                topList = []
                bottomList = []
                leftList = []
                rightList = []
                # 获取选定区域坐标的列表
                for i in selectRect:
                    # 获取
                    rangetop = i.topRow()
                    topList.append(rangetop)
                    rangebuttom = i.bottomRow()
                    bottomList.append(rangebuttom)
                    rangeleft = i.leftColumn()
                    leftList.append(rangeleft)
                    rangeRight = i.rightColumn()
                    rightList.append(rangeRight)
                # print(topList)
                # print(bottomList)
                # print(leftList)
                # print(rightList)
                model = self.tableWidget.model()
                if len(topList) == len(bottomList) == len(leftList) == len(rightList) == 1:
                    for x in range(topList[0], bottomList[0] + 1):
                        for y in range(leftList[0], rightList[0] + 1):
                            cellOldWordList.append(model.data(model.index(x, y)))
                            item = QTableWidgetItem(clip_data.strip())
                            cellLoctionList.append([x, y])
                            symbolpattern = re.compile('["/\\\\:*?<>|]')
                            self.CtrlVCode = 1
                            result = re.findall(symbolpattern, clip_data.strip())
                            if len(result) > 0:
                                item.setBackground(QColor(0, 255, 0))
                            self.tableWidget.setItem(x, y, item)
                    self.addDo([cellLoctionList, cellOldWordList], "update")
                else:
                    try:
                        for i in range(len(topList)):
                            item = QTableWidgetItem(clip_data.strip())
                            symbolpattern = re.compile('["/\\\\:*?<>|]')
                            result = re.findall(symbolpattern, clip_data.strip())
                            if len(result) > 0:
                                item.setBackground(QColor(0, 255, 0))
                            cellOldWordList.append(model.data(model.index(topList[i], leftList[i])))
                            cellLoctionList.append([topList[i], leftList[i]])
                            self.CtrlVCode = 1
                            self.tableWidget.setItem(topList[i], leftList[i], item)
                        self.addDo([cellLoctionList, cellOldWordList], "update")
                    except:
                        print("选定区域错误")
                # #print(len(selectRect))
                # top = selectRect[0].topRow()
                # left  = selectRect[0].leftColumn()
                # bottom = selectRect[-1].bottomRow()
                # right = selectRect[0].rightColumn()
                # #print(top, bottom, left, right)
                # rowscount = bottom - top + 1
                # colscount = right - left +1
                # #print(rowscount)
                # #print(colscount)
                # #print(rowscount * colscount)
                #
                # for y in range(left, right+1):
                #     for x in range(top, bottom+1):
                #         item = QTableWidgetItem(clip_data.strip())
                #         self.tableWidget.setItem(x, y, item)
                # for i in range(len(selectRect)):
                #     #print(selectRect[i].topRow())
                #     #print(selectRect[i].bottomRow())
                #     #print()
                # item = QTableWidgetItem(clip_data.strip())
                # #print(i.rowCount())
                # self.tableWidget.setItem(i.leftColumn(), i.topRow(), item)

    # 捕捉键盘的特别按键
    def keyPressEvent(self, event):
        # print(event.key())
        if (event.key() == Qt.Key_C) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            # 按键事件，ctrl+c时触发，复制。
            # self.clipboard.clear()#清空剪切板，好像没啥用
            self.table_copy()
        # elif (event.key() == Qt.Key_D) and QApplication.keyboardModifiers() == Qt.ControlModifier:
        #     # 按键事件，ctrl+d时触发，删除所在行。
        #     self.del_row()
        elif (event.key() == Qt.Key_E) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            # 按键事件，ctrl+e时触发，导出整张表。
            self.export()
        elif (event.key() == Qt.Key_V) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.clipboard_insert()
        elif (event.key() == Qt.Key_Z) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.undoCtrlZ()

        elif (event.key() == Qt.Key_Backspace):
            # print(QApplication.keyboardModifiers())
            self.bakSpace()
        else:
            self.location()

    # 实现鼠标的退格功能
    def bakSpace(self):
        self.BackspaceCode = 1
        selectRect = self.tableWidget.selectedRanges()

        model = self.tableWidget.model()
        for rect in selectRect:  # 获取范围边界
            for row in range(rect.topRow(), rect.bottomRow() + 1):
                for col in range(rect.leftColumn(), rect.rightColumn() + 1):
                    word = model.data(model.index(row, col))
                    self.keyBoardWordList.append(word)
                    self.KeyBoardLocationList.append([row, col])
                    item = QTableWidgetItem("")
                    self.tableWidget.setItem(row, col, item)
        self.BackspaceCode = 0
        print(self.KeyBoardLocationList)

        print(self.keyBoardWordList)
        self.addDo([self.KeyBoardLocationList, self.keyBoardWordList], "update")
        self.tableWidget.clearSelection()
        self.KeyBoardLocationList = []
        self.keyBoardWordList = []

    # 实现CtrlZ的撤销功能
    def undoCtrlZ(self):

        print(str(["-"] * 50))
        if self.undoStepList:
            print(self.undoStepList)
            FinalStep = self.undoStepList[-1]
            # print(self.undoStepList[-1])
            # 获取编辑表格的索引区间
            tableIndexRange = FinalStep[0][0]
            # #修改区域之前值的列表
            tablewordrange = FinalStep[0][1]
            # 修改类型为
            FinalStepType = FinalStep[1]
            if FinalStepType == "update":
                # 将每个单元格的内容修改回去
                # print(tableIndexRange)
                for cellindex in range(len(tableIndexRange)):
                    cellrow = tableIndexRange[cellindex][0]
                    cellcol = tableIndexRange[cellindex][1]
                    print(cellindex)
                    print(tablewordrange[cellindex])
                    item = QTableWidgetItem(tablewordrange[cellindex])
                    symbolpattern = re.compile('["/\\\\:*?<>|]')
                    self.CtrlVCode = 1
                    try:
                        result = re.findall(symbolpattern, tablewordrange[cellindex])
                        if len(result) > 0:
                            item.setBackground(QColor(0, 255, 0))
                    except:
                        traceback.print_exc()
                    self.tableWidget.setItem(cellrow, cellcol, item)
                    # seleRange = QItemSelectionRange(cellrow, cellcol)
                    # self.tableWidget.setRangeSelected(seleRange)
                # print(tableIndexRange)
                # print(tablewordrange)

            # print(self.tableWidget)
            # self.signalconnect()
            self.undoStepList.pop()
            # print(self.undoStepList)

    # 添加步骤记录
    def addDo(self, commit, type):
        # print(type)
        if len(self.undoStepList) > 0 and [commit, type] != self.undoStepList[-1]:
            self.undoStepList.append([commit, type])
        elif len(self.undoStepList) == 0:
            self.undoStepList.append([commit, type])
        self.undoStepListCopy = self.undoStepList.copy()
        # print(str(["*"] * 50))
        if len(self.undoStepList) > self.undostep:
            self.undoStepList = self.undoStepListCopy[-self.undostep:]
            # print(len(self.undoStepList))
            # print(self.undoStepList)
            # #print(type(self.undoStepList))
        print(1111111111)
        print(self.undoStepList)
        self.BackspaceCode = 0
        # print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    # 删除所选的行
    def del_row(self):
        # 对选取的单元格进行操作，特别是删除，记得先排序，再从最大索引，往最小索引方向进行操作。
        selectRect = self.tableWidget.selectedRanges()
        # print(selectRect)
        set_indices = set()  # 创建空set存放需要删除的行号
        for rect in selectRect:  # 获取范围边界
            for row in range(rect.topRow(), rect.bottomRow() + 1):
                set_indices.add(row)  # 获取被选中的行号（顺序是被依次选中的顺序）
                # print(row)
        set_indices = sorted(set_indices, reverse=True)  # 降序排列（默认升序）
        for row_idx in set_indices:
            self.tableWidget.removeRow(row_idx)  # 根据行号删除行
        # print(set_indices)

    # 复制区域功能
    def table_copy(self):
        selectRect = self.tableWidget.selectedRanges()
        self.text = str()
        for r in selectRect:  # 获取范围边界
            self.top = r.topRow()
            self.left = r.leftColumn()
            self.bottom = r.bottomRow()
            self.right = r.rightColumn()
            self.column_n = 0
            self.number = 0
            self.row_n = 0
            self.column_n = self.right - self.left + 1
            self.row_n = self.bottom - self.top + 1
            self.number = self.row_n * self.column_n
            self.c = []
            for i in range(self.number):
                self.c.append(' \t')  # 注意，是空格+\t
                if (i % self.column_n) == (self.column_n - 1):
                    self.c.append('\n')
                else:
                    pass
                # 这里生成了一个列表，大小是：行X（列+1），换行符占了一列。
                # 默认情况下，列表中全部是空格，
            self.c.pop()  # 删去最后多余的换行符
            range1 = range(self.top, self.bottom + 1)
            range2 = range(self.left, self.right + 1)
            for row, column in product(range1, range2):
                # 实现下面语句的功能
                # for row in range1:
                #    for column in range2:
                try:
                    data = self.tableWidget.item(row, column).text()
                    number2 = (row - self.top) * (self.column_n + 1) + (column - self.left)
                    self.c[number2] = data + '\t'
                    # 计算出单元格的位置，替换掉原来的空格。
                except:
                    pass
            for s in self.c:
                self.text = self.text + s
        self.clipboard.setText(self.text)
        self.text = str()  # 字符串归零

    # 导出功能
    def export(self, list_cols):
        # dir_selected = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        path_selected = QFileDialog.getSaveFileName(self, "导出到Excel文件", "./", "Excel文件 (*.xlsx);;All Files (*)")
        if path_selected[0] == '':  # 点击“取消”时，会返回元组('', '')
            return
        save_file = path_selected[0]
        workbook = Workbook()
        worksheet = workbook.active
        # 每个workbook创建后，默认会存在一个worksheet，对默认的worksheet进行重命名
        worksheet.title = "Sheet1"
        worksheet.append(list_cols)
        row_cnt = self.tableWidget.rowCount()
        col_cnt = self.tableWidget.columnCount()
        for i in range(row_cnt):
            row = []  # 存放每行的内容
            for j in range(col_cnt):
                try:
                    data = self.tableWidget.item(i, j).text()
                    row.append(data)
                except:
                    row.append('')
            worksheet.append(row)  # 把每一行append到worksheet中
        workbook.save(filename=save_file)

    def closeEvent(self, event):
        pass
        # self.closebut_clicked.emit() # 子窗口关闭时发送信号

    # def

if __name__ == '__main__':
    # filePath = r"C:\Users\wangsa\Desktop\表\切分模板old.xlsx"
    filePath = r"C:\Users\wangsa\Desktop\PPDF索引所用到的表格\文档处理控制表【基于OCR识别结果校验】_20221108103650.xlsx"
    # filePath = r"C:\Users\wangsa\Desktop\表\斯菱股份底稿目录.xlsx"
    # getExcelDf(filePath)
    sheet_name = "Sheet1"
    # 是否使用默认匹配模式
    defualt = 1
    colindex = 11
    colcount = 2
    app = QApplication(sys.argv)
    mw = SqlResultWin(filePath, undostep, colindex, colcount, defualt)
    mw.show()
    app.exec_()
