'''
这是切分PDF获取隔页的功能
'''
try:
    from Ui.SplitPdfUi import Ui_SplitPdf
    from Function.splite_pdf import split_pdfs_in_tb
except:
    from .Ui.SplitPdfUi import Ui_SplitPdf
    from .Function.splite_pdf import split_pdfs_in_tb
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import sqlite3
import requests
import json
import random
import traceback
import time
from PyQt5 import QtWidgets

#编辑文档处理控制表参数的界面
class SplitPdf(QWidget, Ui_SplitPdf):
    # 设置输入文本的信号
    textSignal = pyqtSignal(str)
    # 设置弹出警告窗的信号
    warningSignal = pyqtSignal(str)
    # 结束信号
    endSignal = pyqtSignal()
    # 设置执行按钮为可执行，和文本为执行
    btnEnSignal = pyqtSignal()
    # 清空信号
    clearSignal = pyqtSignal()
    child_token_signal = pyqtSignal()
    WidgetColorSignal = pyqtSignal(str)
    def __init__(self, communication = None, token = ""):
        # super(SplitPdf, self).__init__(communication)
        super().__init__(communication)
        self.setupUi(self)
        self.btn1.clicked.connect(self.setFilePath)
        # self.pushButton_3.clicked.connect(self.file_cho)
        self.btn2.clicked.connect(self.splitPdf)
        self.textSignal.connect(self.showText)
        self.endSignal.connect(self.FinishThread)
        self.warningSignal.connect(self.showWarning)
        self.btnEnSignal.connect(self.btnEn)
        if token:
            self.token = token
        else:
            print("拆分文档界面的token值为空")
            # self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiOGNjNjgxOTY4MDNkIiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.3gwm3rH-lZqR7oOLi9vpNBrypSIMuHfYQ-pEklw8A0Q"
            self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE"
        print("这是拆分文档界面的Token值")
        print(self.token)
        self.user = ""
        self.communication = communication
        self.child_token_signal.connect(self.closeMain)
        #旧PDF文件路径
        self.CutPdfOldPath = ''
        #隔页保存文件位置
        self.CutPdfSavaPath = ""
        #OCR结果表格的位置
        self.TablePath = ''
        self.PdfPathtip.setVisible(False)
        self.WidgetColorSignal.connect(self.WidgetColorFun)

    def WidgetColorFun(self, statu):
        if statu == "success":
            self.widget_5.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(32,205,32);")
        elif statu == "fail":
            self.widget_5.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(255,0,0);")
        else:
            self.widget_5.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(0,0,0);")

    def closeMain(self):
        if self.communication:
            try:
                #检测token是否过期的信号
                # self.communication.token_singal.emit()
                print("这是关闭界面的信号")
            except:
                traceback.print_exc()
        else:
            print("程序单独执行")

    def showText(self, word):
        self.plainTextEdit.insertPlainText(word)

    def showWarning(self, word):
        QMessageBox.information(self, "warning", word)

    # 选择文件
    def setFilePath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if download_path:
            self.pdfPathEdit.clear()
            self.pdfPathEdit.setText(download_path)

    # 开始获取隔页
    def splitPdf(self):
        try:
            self.PdfPathtip.setVisible(False)
            self.plainTextEdit.clear()
            self.btn2.setText("正在执行")
            self.btn2.setDisabled(True)
            SavePath = self.pdfPathEdit.text()
            if SavePath == "":
                self.PdfPathtip.setText("请输入拆分之后PDF文件的保存位置！")
                self.PdfPathtip.setVisible(True)
                self.btnEn()
                self.WidgetColorSignal.emit("fail")
                return

            if not os.path.exists(SavePath):
                self.PdfPathtip.setText("文件位置不存在，请确认后重新输入！")
                self.PdfPathtip.setVisible(True)
                self.WidgetColorSignal.emit("fail")
                self.btnEn()
                return
            self.plainTextEdit.insertPlainText("即将开始处理文档\n")
            self.thread1 = runThread(self)
            self.thread1.token = self.token
            self.thread1.user = self.user
            if self.communication:
                self.communication.CutPDfSignal.emit()
                self.thread1.oldPath = self.CutPdfOldPath
                self.thread1.savePath = self.CutPdfSavaPath
                self.thread1.filePath = self.TablePath

            if self.communication and self.thread1.filePath != "":
                self.thread1.mainStart = 0
            self.thread1.start()
        except:
            traceback.print_exc()

    def FinishThread(self):
        try:
            self.thread1.terminate()
        except:
            traceback.print_exc()

    def btnEn(self):
        self.btn2.setEnabled(True)
        self.btn2.setText("单步执行")

class runThread(QThread):
    def __init__(self, communication):
        super(runThread, self).__init__()
        self.communication = communication
        self.run_code = 1
        self.user = ""
        self.token = ""
        #是否是通过__name__ == "__main__"启动
        self.mainStart = 1
        self.oldPath = r"E:\00old"
        self.savePath = r"E:\00save"
        self.filePath = r'E:\00table\文档处理控制表【基于OCR识别结果校验】_20221025164809.xlsx'

    def get_url(self, urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    # 开始执行时传递的id，和所需要记录的文本
    def checkToken(self, id, comments):
        try:

            print(self.communication.token)
            print(self.token)
            self.urldb = os.path.join("./database", "url.db")
            if not os.path.exists(self.urldb):
                if self.communication:
                    self.communication.warningSignal.emit("保存URl表不存在")
                    self.communication.btnEnSignal.emit()
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }

            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【开始执行：】  {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                if response.status_code != 200:

                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break

                        if num == 2:
                            if self.communication:
                                self.communication.child_token_signal.emit()
                            self.run_code = 0
                        num += 1
                else:
                    print("更新成功")
        except:
            traceback.print_exc()

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self, id, comments):
        try:
            if self.communication:
                print(self.communication.token)
            self.urldb = os.path.join("./database", "url.db")
            if not os.path.exists(self.urldb):
                if self.communication:
                    self.communication.warningSignal.emit("保存URl表不存在")
                    self.communication.btnEnSignal.emit()
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【执行完成：】 {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)

                # 判断响应的状态码是否为200， 不为200会进行三次尝试
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            if self.communication:
                                self.communication.child_token_signal.emit()
                            self.run_code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    def run(self):
        # if not self.mainStart:
        self.checkToken(7, "切分隔页")
        if self.run_code:
            self.true_run()
        else:
            self.communication.textSignal.emit('请登录后使用!\n')
            self.communication.WidgetColorSignal.emit("fail")

    def true_run(self):
        oldPath = self.oldPath
        savePath = self.savePath
        filePath = self.filePath

        # # oldPath = r"E:\000old"
        # savePath = self.savePath
        # # filePath = r"C:/Users/wangsa/Desktop/文档处理控制表/文档处理控制表【基于OCR识别结果校验】_20221102172445.xlsx"
        if '"' in oldPath:
            self.communication.textSignal.emit('原PDF文件位置不能有英文双引号\n')
            self.communication.endSignal.emit()
            self.communication.btnEnSignal.emit()
            self.communication.WidgetColorSignal.emit("fail")
            return False

        if '"' in savePath:
            self.communication.textSignal.emit('保存PDF隔页的路径不能有英文双引号\n')
            self.communication.endSignal.emit()
            self.communication.btnEnSignal.emit()
            self.communication.WidgetColorSignal.emit("fail")
            return False


        if '"' in filePath:
            self.communication.textSignal.emit('表的文件路径不能有英文双引号\n')
            self.communication.endSignal.emit()
            self.communication.btnEnSignal.emit()
            self.communication.WidgetColorSignal.emit("fail")
            return False

        if self.communication.checkBox.isChecked():
            num = 1
        else:
            num = 0

        if not os.path.exists(oldPath) or not oldPath:
            self.communication.textSignal.emit("原Pdf文件位置不存在\n")
            self.communication.endSignal.emit()
            self.communication.btnEnSignal.emit()
            self.communication.WidgetColorSignal.emit("fail")
        else:
            # 判断新路径
            if not os.path.exists(savePath) or not savePath:
                self.communication.textSignal.emit("保存Pdf隔页的目标文件不存在\n")
                self.communication.endSignal.emit()
                self.communication.btnEnSignal.emit()
                self.communication.WidgetColorSignal.emit("fail")
            else:
                # 判断表是否存在
                if not os.path.isfile(filePath):
                    self.communication.textSignal.emit("表的位置不存在")
                    self.communication.endSignal.emit()
                    self.communication.btnEnSignal.emit()
                    self.communication.WidgetColorSignal.emit("fail")
                else:
                    if not str(filePath).endswith(".xlsx"):
                        self.communication.textSignal.emit("文件扩展名错误。应为.xlsx")
                        self.communication.btnEnSignal.emit()
                        self.communication.WidgetColorSignal.emit("fail")
                    else:
                        print("切分PDF文件，并保存为单个文件")
                        print(' "{oldPath}"  "{savePath}" "{filePath}" "{num}"'.format( filePath=filePath, oldPath=oldPath, savePath=savePath, num=num))
                        split_pdfs_in_tb(filePath, oldPath, savePath, num )
                        self.communication.WidgetColorSignal.emit("success")
                        # try:
                        #     main = os.path.abspath(os.path.join(os.getcwd(), "exe\splite_pdf.exe"))
                        #     if not os.path.isfile(main):
                        #         self.communication.textSignal.emit("拆分文档、加书签exe不存在\n")
                        #         self.communication.warningSignal.emit("warning", "拆分文档、加书签的exe不存在")
                        #         self.communication.textSignal.emit()
                        #     else:
                        #         print(filePath, oldPath, savePath, num)
                        #         print(num)
                        #         f = os.popen('"{main}" "{oldPath}"  "{savePath}" "{filePath}" "{num}"'.format(main=main, filePath=filePath,
                        #          oldPath=oldPath, savePath=savePath, num=num))
                        #         # self.communication.btnEnSignal.emit()
                        #         self.communication.textSignal.emit("正在处理文档\n")
                        #         data = f.readlines()
                        #         print(data)
                        #         try:
                        #             if 'start_new_file_page' in data:
                        #                 self.communication.textSignal.emit("执行保存隔页失败可能是因为Excel没有完善")
                        #                 self.communication.warningSignal.emit("执行保存隔页失败可能是因为Excel没有完善")
                        #                 self.communication.btnEnSignal.emit()
                        #             else:
                        #
                        #                 self.communication.textSignal.emit("已读取文档处理控制表，并处理完成。\n")
                        #                 self.communication.btnEnSignal.emit()
                        #
                        #         except Exception as e:
                        #             if "NoneTyp" not in str(e):
                        #                 self.communication.textSignal.emit(str(e))
                        #             self.communication.btnEnSignal.emit()
                        #             self.communication.textSignal.emit("执行完毕")
                        #
                        # except Exception as e:
                        #     if "No such file or directory" in str(e):
                        #         self.communication.textSignal.emit(str(e) + "\n")
                        #         self.communication.textSignal.emit("可能因为原路径不存在，或者路径下面没有相关文件!\n")
                        #         self.communication.btnEnSignal.emit()
                        #     else:
                        #         self.communication.textSignal.emit(str(e))
                        #         self.communication.btnEnSignal.emit()
        self.checkToken1(7, "切分隔页")
        self.communication.btnEnSignal.emit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = SplitPdf()
    myWin.show()
    sys.exit(app.exec_())
