'''
设置各个功能的参数，以及界面。
设置自动化处理滚动
'''
# -*- coding: utf-8 -*-
# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import logging
import sys

from clazz import demo
try:
    from .CutPdf.CutPdf import CutPdfPic
    from .SplitPdfFun.SplitPdfFun import SplitPdf
    from .OcrFinish.OcrFinish import OcrFinish
    from .OcrPicFun.OcrPicFun import OcrParameter
    from .OcrTableFun.OcrTableFun import OcrTable
except:
    # pass
    from CutPdf.CutPdf import CutPdfPic
    from SplitPdfFun.SplitPdfFun import SplitPdf
    from OcrFinish.OcrFinish import OcrFinish
    from OcrPicFun.OcrPicFun import OcrParameter
    from OcrTableFun.OcrTableFun import OcrTable

style =  '''
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

class MainWin(QWidget):
    #获取切分隔页界面的参数
    CutPDfSignal = pyqtSignal()
    #
    OcrParamSignal = pyqtSignal()
    OcrFinishSignal = pyqtSignal()
    #返回Ocr表格的信号。
    OcrTablePathSignal = pyqtSignal(str)

    Auto_token_signal = pyqtSignal()

    #这是为所有token设置
    Fun_token_signal = pyqtSignal()

    def __init__(self, token = ""):
        self.offsetY = 0
        super().__init__()
        self.token = token
        print("这是自动化参数界面中各个界面返回token值")
        print(self.token)
        self.setMinimumSize(840, 3000)

        if token == "":
            # self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjEiLCJtYWMiOiIwMDJiNjdlMjJkNTgiLCJpcCI6IjEyNC4yMDIuMjEyLjE4In0.MD9Ielzh4bDPdgKh-fmnvUyYNp4kAGrq79DQlpRqfl0"
            self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE"
        else:
            self.token = token
        #获取隔页的界面
        self.CutPdfPicWidget = CutPdfPic(self, self.token)
        self.CutPdfPicWidget.setStyleSheet(style)
        self.CutPdfPicWidget.move(0, 50 + self.offsetY)

        #第一个向下箭头
        self.downImage(400, 510)

        #设置Ocr参数的界面
        self.OcrPWidget = OcrParameter(self, self.token)
        self.OcrPWidget.setStyleSheet(style)
        self.OcrPWidget.move(0, 600 + self.offsetY)
        self.downImage(400, 1020)
        #设置Ocr完成的界面
        self.OcrFinishWidget = OcrFinish(self, self.token)
        self.OcrFinishWidget.setStyleSheet(style)
        self.OcrFinishWidget.move(0, 1110 + self.offsetY)

        self.downImage(400, 1380)

        #设置Ocr识别结果表格的界面
        self.OcrTableWidget = OcrTable(self, self.token)
        self.OcrTableWidget.setStyleSheet(style)
        self.OcrTableWidget.move(0, 1460 + self.offsetY)

        self.downImage(400, 1890)
        
        #设置切分PDF参数的界面
        self.SplitPdfWidget = SplitPdf(self, self.token)
        self.SplitPdfWidget.setStyleSheet(style)
        self.SplitPdfWidget.move(0, 1950 + self.offsetY)
        self.CutPDfSignal.connect(self.CutPdfParams)
        self.OcrParamSignal.connect(self.GetOcrParams)
        self.OcrFinishSignal.connect(self.GetOcrFinish)
        self.OcrTablePathSignal.connect(self.SetTablePath)
        self.TablePath = ""
        self.Auto_token_signal.connect(self.AutoTokenFun)

    #判断token过期的信号
    def AutoTokenFun(self):
        print("设置参数界面的token过期信号")

    #设置表格路径
    def SetTablePath(self, tablePath):
        print("Ocr表格的保存路径")
        print(tablePath)
        self.TablePath = tablePath

    #判断OCR完成界面需要的参数
    def GetOcrFinish(self):
        savePath = self.CutPdfPicWidget.savaOnePdfEdit.text()
        self.OcrFinishWidget.OcrPath = savePath

    #Ocr隔页需要的参数
    def GetOcrParams(self):
        savePath = self.CutPdfPicWidget.savaOnePdfEdit.text()
        self.OcrPWidget.FilePath = savePath

    #传递隔页页面中的各个参数
    def CutPdfParams(self):
        print("这是从切分PDf界面中获取参数")
        OldPath = self.CutPdfPicWidget.OldPdfPathEdit.text()
        SavePath = self.SplitPdfWidget.pdfPathEdit.text()
        # TablePath =
        # print("")
        # OldPath = r"E:\00old"
        # SavePath = r"E:\000save"
        TablePath = self.TablePath

        print("返回切分PDF界面中各个参数的值")
        print(OldPath)
        print(SavePath)
        print(TablePath)
        self.SplitPdfWidget.CutPdfOldPath = OldPath
        self.SplitPdfWidget.CutPdfSavaPath = SavePath
        self.SplitPdfWidget.TablePath = TablePath

    #设置向下的街头
    def downImage(self, x, y):
        pixmap = QPixmap("../Resource/downImage.png")
        self.imageQLabel = QLabel(self)
        self.imageQLabel.setPixmap(pixmap)
        self.imageQLabel.setMinimumSize(70, 80)
        self.imageQLabel.setScaledContents(True)
        self.imageQLabel.move(x, y)

#自动化执行的滚动区域
class AutoScroll(QScrollArea, demo.TableObject):
    def __init__(self, parent=None, token = ""):
        super(AutoScroll, self).__init__(parent)
        self.token = token
        print("这是自动化参数界面的滚动区域所输出的token")
        print(self.token)
        self.MainWin = MainWin(self.token)
        self.setMinimumSize(860, 680)
        self.setWidget(self.MainWin)
        self.FunctionName = "自动化处理界面功能"
        self.describetion = '''
=================================================
这是自动化处理功能
=================================================
'''
if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = AutoScroll()
    myWin.show()
    sys.exit(app.exec_())