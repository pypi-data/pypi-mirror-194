import time
import traceback
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtCore import *
try:
    from Ui.mkdirUi import Ui_Mkdier
    from Ui.MaskWin import MaskWidget
    from Function.MkdirFunction import MkdirObject
except:
    from Ui.mkdirUi import Ui_Mkdier
    from Ui.MaskWin import MaskWidget
    from Function.MkdirFunction import MkdirObject

#创建文件夹的主函数

from clazz import demo
class Mkdirs(QMainWindow, Ui_Mkdier, demo.TableObject):
    #文件路径的信号
    filePathsignal  = pyqtSignal(str)
    #路径错误的信号
    filePathErrorsignal = pyqtSignal(str, str)
    style = '''
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
    #更新底稿目录的信号
    updateTableSigal = pyqtSignal(list)
    #连接界面中进度条的信号
    ProcessBarSignal = pyqtSignal(float)

    def __init__(self,communication = None, token = ""):
        super(Mkdirs, self).__init__(communication)
        self.communication = communication
        if token:
            self.token = token
        else:
            print("自动化处理界面初始化的token值为空")
            self.token = token
        print("这是创建文件夹界面所输出的Token")
        print(self.token)
        self.isMakeDir  = 1
        self.setupUi(self)
        self.setStyleSheet(self.style)
        self.nowNum = 0
        self.titleOldY = self.title.pos().y()
        self.pathNamePos = self.pathName.pos()
        self.pathNameEditPos = self.pathNameEdit.pos()
        self.filePathBtnPos = self.filePathBtn.pos()
        self.fileDeepEditPos = self.fileDeepEdit.pos()
        self.SeparatorEditPos = self.SeparatorEdit.pos()
        self.CreateBtnPos = self.CreateBtn.pos()
        self.fileDeepPos = self.fileDeep.pos()
        self.SeparatorPos = self.Separator.pos()
        self.setMinimumSize(860, 571)
        self.oldWindowY = self.height()
        self.oldWindowX = self.width()
        #文件深度输入框以及分隔符进行输入内容的限制，并设置默认内容
        self.fileDeepEdit.setValidator(QRegExpValidator(QtCore.QRegExp("[1-9]{1}\d{0,2}"), self))
        self.SeparatorEdit.setValidator(QRegExpValidator(QtCore.QRegExp('[^"/\\\\:*?<>|]{,}'), self))
        self.SeparatorEdit.setPlaceholderText("默认为分隔符'  '。分隔符不能包含：/\\\\:*?<>|")
        self.fileDeepEdit.setPlaceholderText("默认为3")
        #创建文件夹时索引与后面关键字的分隔符
        self.SeparatorWord = "  "
        if self.fileDeepEdit.text():
            self.DefaultDeep = self.fileDeepEdit.text()
        else:
            #默认文件夹的深度
            self.DefaultDeep = 3
        #将创建开始创建文件夹按钮与创建文件夹的函数连接
        self.CreateBtn.clicked.connect(self.makeDirs)
        #文件路径信号
        self.filePathsignal.connect(self.PathWaring)
        #文件路径按钮连接对应的槽函数
        self.filePathBtn.clicked.connect(self.file_cho)
        #路径名错误连接的槽函数
        self.filePathErrorsignal.connect(self.updatepath)
        #进度条连接的槽函数
        self.processBarPos = self.processBar.pos()
        #创建文件夹的列表
        # self.updateTableSigal.connect(self.updateTable)
        #主页传递过来的名字列表
        self.MainnameList = []
        #主页传递过来的索引列表
        self.MainIndexList = []
        #将进度条信号连接的槽函数
        self.ProcessBarSignal.connect(self.ProcessBarFuntion)
        self.FunctionName = "创建文件夹"
        self.describetion = '''
=================================================
这是创建文件夹的功能
=================================================
'''
    #界面进度条函数
    def ProcessBarFuntion(self, num):
        if num < 1.1:
            self.processBar.setValue(num * 100)
        else:
            self.processBar.setValue(100)

    # 创建文件夹的主函数
    def makeDirs(self):
        # 判断分隔符输入框的内容是否为空
        if self.SeparatorEdit.text():
            self.SeparatorWord = self.SeparatorEdit.text()
        # 判断文件夹深度输入框内容是否为空
        if self.fileDeepEdit.text():
            self.DefaultDeep = int(self.fileDeepEdit.text())

        #输入文件框中的内容
        filePath = self.pathNameEdit.text()

        #如果保存文件的为空
        if not filePath:
            self.nowNum += 1
            word = "请输入保存文件夹的位置!"
            print("我是主函数创建文件夹名字列表:  ", end= "")
            print(self.MainnameList)
            print("我是主函数创建文件夹索引列表:  ", end="")
            print(self.MainIndexList)
            print("分隔符为：", end = "")
            print(self.SeparatorWord)
            print("文件夹的深度为: ", end = "")
            print(self.DefaultDeep)

            self.pathErrorThread = Errorthreadc(self, self.nowNum, word)
            self.pathErrorThread.start()
            return

        #如果输出文件夹的位置不存在
        if not os.path.exists(filePath):
            self.nowNum += 1
            word = "文件路径不存在!"
            self.pathErrorThread = Errorthreadc(self, self.nowNum, word)
            self.pathErrorThread.start()
            return

        #创建建文件夹的线程
        self.mkDirthread = mkDirThread(self, self.DefaultDeep, filePath, self.SeparatorWord, self.isMakeDir, self.MainnameList, self.MainIndexList)
        self.mkDirthread.start()

    #修改警告框内容的槽函数，当警告框已经处于可见状态修改，如果类型为
    def updatepath(self, type, word):

        if type == "visible":
            print("设置可见", end="")
            print(word)
            self.filePathWaring.setText(word)
            self.filePathWaring.setVisible(True)

        elif type == "disvisible":
            print("不可见")
            if int(word) == self.nowNum:
                self.filePathWaring.setVisible(False)


    #获取文件路径
    def file_cho(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if dirPath:
            self.pathNameEdit.setText(dirPath)

    #显示警告框
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


    #路径警告函数
    def PathWaring(self, word):
        self.showDialog(word)


    def resizeEvent(self, event):
        try:
            #移动标题位置的代码
            title_x = (self.width() - self.title.size().width()) / 2
            title_y = self.titleOldY
            self.title.move(int(title_x), int(title_y))
            #文件名的位置的代码
            pathName_x = (self.width() - self.oldWindowX) / 2 + self.pathNamePos.x()
            pathName_y = self.pathNamePos.y()
            self.pathName.move(int(pathName_x), int(pathName_y))
            pathName_x = (self.width() - self.oldWindowX) / 2 + self.pathNameEditPos.x()
            pathName_y = self.pathNameEditPos.y()
            self.pathNameEdit.move(int(pathName_x), int(pathName_y))
            filePathBtn_x = (self.width() - self.oldWindowX) / 2 + self.filePathBtnPos.x()
            filePathBtn_y = self.filePathBtnPos.y()
            self.filePathBtn.move(int(filePathBtn_x), int(filePathBtn_y))
            fileDeepEdit_x = (self.width() - self.oldWindowX) / 2 + self.fileDeepEditPos.x()
            fileDeepEdit_y = self.fileDeepEditPos.y()
            self.fileDeepEdit.move(int(fileDeepEdit_x), int(fileDeepEdit_y))
            SeparatorEdit_x = (self.width() - self.oldWindowX) / 2 + self.SeparatorEditPos.x()
            SeparatorEdit_y = self.SeparatorEditPos.y()
            self.SeparatorEdit.move(int(SeparatorEdit_x), int(SeparatorEdit_y))
            fileDeep_x = (self.width() - self.oldWindowX) / 2 + self.fileDeepPos.x()
            fileDeep_y = self.fileDeepPos.y()
            self.fileDeep.move(int(fileDeep_x), int(fileDeep_y))
            Separator_x = (self.width() - self.oldWindowX) / 2 + self.SeparatorPos.x()
            Separator_y = self.SeparatorPos.y()
            self.Separator.move(int(Separator_x), int(Separator_y))
            CreateBtn_x = (self.width() - self.oldWindowX) / 2 + self.CreateBtnPos.x()
            CreateBtn_y = self.CreateBtnPos.y()
            self.CreateBtn.move(int(CreateBtn_x), int(CreateBtn_y))

            processBar_x = (self.width() - self.oldWindowX) / 2 + self.processBarPos.x()
            processBar_y = self.processBarPos.y()
            self.processBar.move(int(processBar_x), int(processBar_y))

        except:
            traceback.print_exc()


#创建文件夹的主线程
class mkDirThread(QThread):
    #     kDirThread(self, self.fileDeepEdit, filePath, self.SeparatorEdit, isMakeDir, self.MainnameList, self.MainIndexList)
    def __init__(self, communication, deepNum, filePath, Separator, isMakeDir, NameList, IndexList):
        super(mkDirThread, self).__init__()
        self.communication = communication
        self.deepNum = deepNum
        self.filePath = filePath
        self.Separator = Separator
        self.isMakeDir = isMakeDir
        self.NameList = NameList
        self.IndexList  = IndexList

    #文件夹执行运行主函数
    def run(self):
        print("创建文件夹")
        print( self.NameList)
        OneNameList = []
        for i in self.NameList:
            deep = len(str(i[0]).split("-"))
            if deep <= self.deepNum:
                OneNameList.append(i)
        NameListLen = len(OneNameList)
        print(self.IndexList)
        print(self.filePath, self.isMakeDir, self.Separator, self.deepNum, self.communication)
        partListIndex = []
        NameListCopy = self.NameList.copy()
        for i in NameListCopy:
            if "部分" in i[0]:
                partListIndex.append(NameListCopy.index(i))
                NameListCopy[NameListCopy.index(i)] = ""
        if partListIndex != len(self.NameList)-1:
            partListIndex.append(len(self.NameList))
        PartListLen = len(partListIndex)
        print("输出要建文件夹的名字的长度")
        print(NameListLen)
        print(PartListLen)
        MkDirLen = NameListLen - PartListLen
        StartIndex = 0

        for i in range(PartListLen):
            if i == 0:
                #第一个索引
                firstIndex = partListIndex[0]
                if firstIndex != 0:
                    # pass
                    namelist = self.NameList[:firstIndex]
                    indexList = self.IndexList[:firstIndex]
                    self.MkDirFun = MkdirObject(namelist, indexList, self.filePath, self.isMakeDir,self.Separator, self.deepNum, self.communication, "", MkDirLen, 0)
                    self.MkDirFun.getMakeDict()
                    UseNameList = []
                    for i in namelist:
                        deep = len(str(i[0]).split("-"))
                        if deep <= self.deepNum:
                            UseNameList.append(i)

                    print(UseNameList)
                    StartIndex += len(UseNameList)
            # else:
            #     pass
            else:
                namelist = self.NameList[partListIndex[i-1] + 1 : partListIndex[i]]
                indexList = self.IndexList[partListIndex[i-1] + 1 : partListIndex[i]]
                print("--------------------------------------------------------------------------------")
                print(namelist)
                print(indexList)
                print("======================================================================================")

                self.MkDirFun = MkdirObject( namelist, indexList, self.filePath, self.isMakeDir, self.Separator, self.deepNum, self.communication, self.NameList[partListIndex[i-1]][0], MkDirLen, StartIndex)
                self.MkDirFun.getMakeDict()
                UseNameList = []
                for i in namelist:
                    deep = len(str(i[0]).split("-"))
                    if deep <= self.deepNum:
                        UseNameList.append(i)
                print(UseNameList)
                StartIndex += len(UseNameList)
        print("运行完成")

#路径错误的线程
class Errorthreadc(QThread):
    def __init__(self, communication, num, word):
        super(Errorthreadc, self).__init__()
        self.communication = communication
        self.num = num
        self.word = word

    def run(self):
        self.communication.filePathErrorsignal.emit("visible", self.word)
        time.sleep(5)
        self.communication.filePathErrorsignal.emit("disvisible", str(self.num))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Mkdirs()
    myWin.show()
    sys.exit(app.exec_())
