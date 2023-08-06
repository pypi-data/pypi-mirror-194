# coding=utf-8
'''

获取pdf中的隔页图片并保存

'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import traceback

import fitz
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import time
import os
from multiprocessing import Pool
from functools import partial
import shutil
import sqlite3
print("ccccccccccccccccccccccccccccccccccccc")
from multiprocessing import freeze_support
try:
    from .Ui.CutPdfPicUi import Ui_CutPdfPic
    from .Function.optionDb import getOption, InsertDb
    # from .Function.cut_pdF_pic import get_pdf_color_page

except:
    # pass

    from Ui.CutPdfPicUi import Ui_CutPdfPic
    from Function.optionDb import getOption, InsertDb
    from Function.cut_pdF_pic import get_pdf_color_page

import sys
import time
import sqlite3
import requests
import json
import random
from multiprocessing import cpu_count
import os
from PyQt5 import QtWidgets
import shutil
import traceback

from multiprocessing import Pool
from multiprocessing import freeze_support

class CutPdfPic(QWidget, Ui_CutPdfPic):
    #用于写入QPlainTextEidt的信号量
    signal1 = pyqtSignal(str)
    # 显示warnbox 的信号量
    signal_warn = pyqtSignal(str,str)
    #设置按钮文字以及可以点击的信号
    reload_signal = pyqtSignal()
    #设置退出线程信号
    thread1_signal = pyqtSignal()
    child_token_signal = pyqtSignal()
    #获取隔页进度条的信号
    getOnePicBarSignal = pyqtSignal(float)
    WidgetColorSignal = pyqtSignal(str)
    def __init__(self, communication=None, token = ""):
        # super(CutPdfPic, self).__init__(communication)
        super().__init__(communication)
        self.setupUi(self)
        self.UiInit()
        self.communication = communication
        #开始切分PDf的按钮
        self.StartCutPdfBtn.clicked.connect(self.cutPdf11)
        #重置拆分按钮的信号
        self.reload_signal.connect(self.reload1)
        #将内容写入到Qtext的信号
        self.signal1.connect(self.Write_QPText)
        #警告信号
        self.signal_warn.connect(self.warn_signal)
        self.thread1_signal.connect(self.thread1Quit)
        # 设置按钮连接选择文件
        self.OldPDfPath.clicked.connect(self.setOldFilePath)
        # 设置按钮连接选择文件
        self.PicSavePath.clicked.connect(self.setPicPath)
        self.endBtn.clicked.connect(self.yesNoCut)
        if token:
            self.token = token
        else:
            print("获取隔页界面初始化的token值为空")
            self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiOGNjNjgxOTY4MDNkIiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.3gwm3rH-lZqR7oOLi9vpNBrypSIMuHfYQ-pEklw8A0Q"
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE'
        print("这是获取隔页界面得到的token")
        print(self.token)
        self.user = ""
        self.communication = communication
        self.child_token_signal.connect(self.closeMain)
        self.hideTip()
        self.getOnePicBarSignal.connect(self.ChangeProcessBar)
        self.WidgetColorSignal.connect(self.WidgetColorFun)

    def WidgetColorFun(self, statu):
        if statu == "success":
            self.widget.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(32,205,32);")
        elif statu == "fail":
            self.widget.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(255,0,0);")
        else:
            self.widget.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(0,0,0);")

    def ChangeProcessBar(self, num):
        if num < 1.1:
            self.getOnePicBar.setValue(int(num * 100))
        else:
            self.getOnePicBar.setValue(100)
            self.getOnePicBar.setTextVisible(False)
            self.WidgetColorSignal.emit("success")

    def closeMain(self):
        if self.communication:
            self.communication.Auto_token_signal.emit()

    def yesNoCut(self):
        a = QMessageBox.question(self, 'warning', '是否停止获取隔页', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a == QMessageBox.Yes:
            self.stopCut()

    def UiInit(self):
        ui_list = getOption("getGe")
        # 判断类型
        if isinstance(ui_list, list):
            if len(ui_list) == 1:
                ui_tuple = ui_list[0]
                self.OldPdfPathEdit.setText(ui_tuple[1])
                self.savaOnePdfEdit.setText(ui_tuple[2])
                self.processNumberEdit.setText(ui_tuple[3])
                print("这里将输出一个空格")
                print(ui_tuple[4])
                print(111111111111111111111111111111111111111111111)
                if ui_tuple[4]:
                    if int(ui_tuple[4]) <= cpu_count():
                        self.thresholdEdit.setText(ui_tuple[4])
        elif isinstance(ui_list, str):
            pass
        else:
            self.textEdit.setText(str(ui_list))

    def write_DB(self):

        self.OldPath = self.OldPdfPathEdit.text()
        #判断路径是否存在
        if not self.OldPath:
            self.oldPathtip.setText("原PDF文件路径为空！")
            self.oldPathtip.setVisible(True)
            self.WidgetColorSignal.emit("fail")
            return "路径错误"
        else:
            #判断文件路径是否存在
            if not os.path.exists(self.OldPath):
                self.oldPathtip.setText("原PDF文件路径不存在！")
                self.oldPathtip.setVisible(True)
                self.WidgetColorSignal.emit("fail")
                return "路径错误"

        self.NewPath = self.savaOnePdfEdit.text()
        if not self.NewPath:
            self.savePathTip.setText('保存图片隔页位置为空！')
            self.savePathTip.setVisible(True)
            self.WidgetColorSignal.emit("fail")
            return "路径错误"
        else:
            if not os.path.exists(self.NewPath):
                self.savePathTip.setText("保存图片隔页位置不存在！")
                self.savePathTip.setVisible(True)
                self.WidgetColorSignal.emit("fail")
                return "路径错误"

        self.oldDir = set()
        f = os.listdir(self.NewPath)
        for i in f:
            dir = os.path.join(self.NewPath, i)
            if os.path.isdir(dir):
                self.oldDir.add(dir)
        self.LNum = self.thresholdEdit.text()
        try:
            self.Pnum = int(self.processNumberEdit.text())
            if 0 < self.Pnum < 9:
                checkTuple = ("getGe", self.OldPath, self.NewPath, str(self.Pnum), self.LNum)
            else:
                checkTuple = ("getGe", self.OldPath, self.NewPath, "", self.LNum)
        except:
            checkTuple = ("getGe", self.OldPath, self.NewPath, "", self.LNum)
        g = InsertDb(checkTuple)

    #隐藏
    def hideTip(self):
        self.oldPathtip.setVisible(False)
        self.savePathTip.setVisible(False)

    def cutPdf11(self):
        self.WidgetColorSignal.emit("reload")

        self.hideTip()
        result = self.write_DB()
        if result !=  "路径错误":
            self.plainTextEdit.clear()
            self.endBtn.setEnabled(True)
            self.StartCutPdfBtn.setText('正在执行')
            self.StartCutPdfBtn.setDisabled(True)
            self.WidgetColorSignal.emit("fail")
            if '"' in self.OldPath:
                # self.plainTextEdit.insertPlainText("源文件路径包含英文的双引号")
                self.oldPathtip.setText("源文件路径包含英文的双引号")
                self.WidgetColorSignal.emit("fail")
            else:
                if '"' in self.NewPath:
                    # self.plainTextEdit.insertPlainText("保存文件路径包含英文的双引号")
                    self.savePathTip.setText("保存文件路径包含英文的双引号")
                    self.WidgetColorSignal.emit("fail")
                else:
                    self.thread1 = runThread(communication=self)
                    self.thread1.token = self.token
                    self.thread1.user = self.user
                    self.thread1.start()

    def reload1(self):
        self.StartCutPdfBtn.setText("拆分")
        self.StartCutPdfBtn.setEnabled(True)
        self.endBtn.setDisabled(True)

    def Write_QPText(self, word):
        self.plainTextEdit.insertPlainText(word)

    def warn_signal(self, title, word):
        QMessageBox.information(self, title, word)

    def thread1Quit(self):
        self.thread1.terminate()

    def setOldFilePath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")

        if download_path:
                self.OldPdfPathEdit.clear()
                self.OldPdfPathEdit.setText(download_path)

    def setPicPath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if download_path:
                self.savaOnePdfEdit.clear()
                self.savaOnePdfEdit.setText(download_path)

    # 停止切分
    def stopCut(self):
        try:
            #
            # os.system("taskkill -f -im cut_pdF_pic.exe")
            self.thread1.pool.terminate()
            self.thread1.terminate()

            # self.newDir = set()
            # f = os.listdir(self.NewPath)
            # for i in f:
            #     dir = os.path.join(self.NewPath, i)
            #     if os.path.isdir(dir):
            #         self.newDir.add(dir)
            # dir_names = self.newDir - self.oldDir
            # print("new" + str(self.newDir))
            # print("old" + str(self.oldDir))
            # print(dir_names)
            # for i in dir_names:
            #     shutil.rmtree(i)
        except:
            traceback.print_exc()
        self.plainTextEdit.insertPlainText("停止成功")
        self.reload_signal.emit()

def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
class runThread(QThread):
    def __init__(self, communication):
        super(runThread, self).__init__()
        #用于传递的信号
        self.communication = communication
        # #进程池
        self.run_code = 1
        self.user = ""
        self.token = ""
        # self.urldb = os.path.join("./database", "url.db")
        FilePath = os.path.dirname(__file__)
        print(FilePath)
        FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
        # self.urldb = os.path.join( "../database" , "url.db")
        self.urldb = os.path.join( FilePath , "url.db")
        # print("=====================================")
        # print(self.urldb)

    def get_url(self,urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    #开始执行时传递的id，和所需要记录的文本
    def checkToken(self,id,comments):
        try:

            if not os.path.exists(self.urldb):
                self.communication.signal1.emit("保存URl表不存在")
                self.run_code = 0
                return False
            print("检查token是否过期")
            print(self.token)
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
                print(response.text)
                if response.status_code != 200:

                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break

                        if num == 2:
                            self.communication.child_token_signal.emit()
                            self.run_code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self,id,comments):
        try:
            # self.urldb = os.path.join("./database", "url.db")
            if not os.path.exists(self.urldb):
                self.communication.signal1.emit( "保存URl表不存在")
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }
            print(self.token)
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【执行完成：】 {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)

                #判断响应的状态码是否为200， 不为200会进行三次尝试
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            self.communication.child_token_signal.emit()
                            self.run_code = 0
                        num+=1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    #检查空格
    def checkSpace(self):

        file_path = self.communication.OldPdfPathEdit.text()
        filename = ""
        for parent, dir, file in os.walk(file_path):
            for i in file:
                if " .pdf" in i:
                    filename += i + "   "
                    self.communication.signal1.emit("pdf文件：" + i + " 包含空格\n")
                    self.run_code = 0
        if filename:
            self.communication.signal_warn.emit("warning", "存在PDF文件包含空格，请修改后再次输入")

    def run(self):
        self.checkSpace()
        print(self.token)
        self.checkToken(3, "获取隔页")

        if self.run_code:
            self.true_run()
        else:
            self.communication.WidgetColorSignal.emit("fail")
            self.communication.reload_signal.emit()
            self.communication.signal1.emit("请登录后使用")

    def true_run(self):
        self.process_count1 = self.communication.processNumberEdit.text()
        self.OldFilePath = self.communication.OldPdfPathEdit.text()
        print(self.OldFilePath)
        self.NewFilePath = self.communication.savaOnePdfEdit.text()
        print(self.NewFilePath)
        self.LightNum = self.communication.thresholdEdit.text()
        # 判断路径是否过长
        len_number = 0
        # 判断路劲是否存在
        if os.path.exists(self.OldFilePath):
            if os.path.exists(self.NewFilePath):
                for parent, dirnames, filenames in os.walk(self.OldFilePath):
                    for filename in filenames:
                        file_path = os.path.join(parent, filename)
                        pathLen = len(file_path) + len(self.NewFilePath) - len(self.OldFilePath)
                        if pathLen >= 259:
                            len_number = 1
                            self.communication.signal1.emit(file_path + " \n路径过长")
                            self.communication.WidgetColorSignal.emit("fail")
            else:
                self.run_code = 0
                self.communication.signal1.emit("保存文件不存在，请重新输入\n")
                self.communication.WidgetColorSignal.emit("fail")
                self.communication.reload_signal.emit()
                #线程结束
                self.communication.thread1_signal.emit()
        else:
            self.run_code = 0
            self.communication.signal1.emit("原路径不存在，请重新输入\n")
            self.communication.WidgetColorSignal.emit("fail")
            self.communication.reload_signal.emit()
            # 线程结束
            self.communication.thread1_signal.emit()

        # 判断路径长度是否大于259
        if len_number and self.run_code:
            # 线程结束
            self.communication.thread1_signal.emit()
        if not self.LightNum and self.run_code:
            self.LightNum = 19

        # 设置默认的进程数为cpu的核数-1
        if not self.process_count1 :
            self.process_count1 = int(cpu_count() - 1)

        else:
            try:
                if int(self.process_count1) > int(cpu_count()) or int(self.process_count1) < 1:
                    self.communication.processNumberEdit.setText("")
                    self.communication.signal1.emit("请输入1-{}的整数".format(cpu_count() ))
                    self.communication.reload_signal.emit()
                    self.communication.signal_warn.emit("warning", "请输入1-{}的整数".format(cpu_count() ))
                    self.communication.WidgetColorSignal.emit("fail")
                    self.communication.thread1_signal.emit()
                self.process_count1 = int(self.process_count1)

            except:
                try:
                    # 线程结束
                    # QMessageBox.warning(self, "Warining", "请输入1-8的整数", QMessageBox.Ok)
                    self.communication.processNumberEdit.setText("")
                    self.communication.signal1.emit("请输入1-{}的整数".format(cpu_count() ))
                    self.communication.reload_signal.emit()
                    self.communication.signal_warn.emit("warning", "请输入1-{}的整数".format(cpu_count() ) )
                    self.communication.WidgetColorSignal.emit("fail")
                    self.communication.thread1_signal.emit()
                    self.run_code = 0
                    self.process_count1 = ""

                except:
                    traceback.print_exc()

        # 检测用于保存表的路径是否存在
        # Db_path = r'.\database'
        # if not os.path.exists(Db_path):
        #     os.makedirs(Db_path)
        # table_path = os.path.join(Db_path, "cut_Pdf_Db.db")
        # # print(table_path)
        # # 创建表
        # try:
        #     if os.path.isfile(table_path):
        #         os.remove(table_path)
        # except:
        #     self.communication.signal1.emit("切分PDF文件表目前已被打开。请关闭后使用！\n")
        #     self.communication.reload_signal.emit()
        #     self.run_code = 0
        # try:
        #     conn = sqlite3.connect(table_path)
        #     cursor = conn.cursor()
        #     cursor.execute(
        #         'CREATE TABLE IF NOT EXISTS  Old_New(OldFilePath varchar(255) , NewFilePath varchar(720), ProcessCount INT, LightNum  INT)')
        #     # 插入数据
        #     sql = "insert into Old_New values ('{}', '{}', '{}','{}')".format(self.OldFilePath, self.NewFilePath, self.process_count1, int(self.LightNum))
        #     print(sql)
        #     cursor.execute(sql)
        #     cursor.close()
        #     conn.commit()
        #     conn.close()
        #
        # except:
        #     self.communication.signal1.emit("获取隔页信息插入失败！\n")
        #     self.communication.reload_signal.emit()
        #     self.run_code = 0

        if self.run_code:
            print("启动参数")
            print(self.OldFilePath, self.NewFilePath, self.process_count1, int(self.LightNum))
            if not os.path.exists('./log'):
                os.mkdir("log")
            log_name = str(os.getcwd()) + '/log/底稿切分Pdf隔页运行日志_' + str(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')
            error_name = str(os.getcwd()) +  '/log/底稿切分Pdf隔页运行错误日志_' + str(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')
            src_pdf_path = self.OldFilePath
            save_pic_path = self.NewFilePath
            COLOR_THRESHHOLD = self.LightNum
            processors = self.process_count1
            print(src_pdf_path)
            print(save_pic_path)
            print(COLOR_THRESHHOLD)
            print(processors)
            print('开始时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(COLOR_THRESHHOLD)
            pdf_list = []
            for parent, dirs, files in os.walk(src_pdf_path):
                for file in files:
                    if str(file).endswith(".pdf"):
                        file_path = os.path.join(parent, file)
                        pdf_list.append(file_path)
            print(pdf_list)
            # 判断
            if len(pdf_list):
                # 如果文件数量小于进程数量，那么按文件数量来启动进程。
                if len(pdf_list) < int(processors):
                    processors = len(pdf_list)
                self.pool = Pool(processes=int(processors))
                li = []
                for i in pdf_list:
                    print(i)
                    res = self.pool.apply_async(get_pdf_color_page, args=(i, save_pic_path, log_name, error_name, COLOR_THRESHHOLD))
                    #进度条的信号
                    # self.communication.getOnePicBarSignal.emit(pdf_list.index(i) + 1/len(pdf_list))
                    li.append(res)
                self.pool.close()
                self.pool.join()
                self.communication.WidgetColorSignal.emit("success")
                self.communication.signal1.emit("执行完毕")
            else:
                print("原文件夹为空，或者均已OCR请确认后再次输入")


        #通过执行exe来运行
        # if self.run_code:
        #     main = os.path.abspath(os.path.join(os.getcwd(), "exe\cut_pdF_pic.exe"))
        #     if not os.path.isfile(main):
        #         self.communication.signal1.emit("切分隔页的exe不存在\n")
        #         self.communication.reload_signal.emit()
        #         self.communication.signal_warn.emit("warning", "切分隔页的exe不存在")
        #         self.communication.thread1_signal.emit()
        #     else:
        #         self.communication.signal1.emit("执行隔页exe\n")
        #         try:
        #             print("启动隔页exe的参数：", end = "")
        #             print(self.OldFilePath, self.NewFilePath, self.process_count1, int(self.LightNum))
        #             f = os.popen('"{main}" "{oldPath}" "{savePath}" "{process}" "{num}"'.format(main = main,oldPath = self.OldFilePath, savePath =self.NewFilePath, process= self.process_count1, num= int(self.LightNum)))
        #             data = f.readlines()
        #             f.close()
        #             for i in data:
        #                 self.communication.signal1.emit(i)
        #         except Exception as e:
        #             start_time = get_now()
        #             index_check_log_name = './log/底稿切分隔页UI报错日志_' + str(start_time)
        #             log_path = os.path.join(os.getcwd(),index_check_log_name.replace("./", "") + ".txt").replace("\\","/")
        #             self.communication.signal1.emit("保存运行日志的文件夹为：" + log_path.split('log/')[0] + "log。运行日志文件名为：" +log_path.split('log/')[1] + "\n")
        #             with open(index_check_log_name + '.txt', "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        #                 file.write('[Error]' + str(get_now()) + "\n")
        #                 file.write('[报错内容]' + str(e) + "\n")
        #                 file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
        #                 file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
        #         #执行完成
        #         self.communication.signal1.emit("执行完成")
        #         self.communication.reload_signal.emit()
        self.communication.reload_signal.emit()
        self.checkToken1(3, "获取隔页")


def get_pdf_color_page(file_path, save_pic_path, log_name, error_name, COLOR_THRESHHOLD):
    print(11111111111111111111111111111111111111111111111111111)
    file = os.path.split(file_path)[1]
    pdf = fitz.open(file_path)
    pdffolderpath = os.path.join(save_pic_path, file[:-4].strip())
    n_folder_max = 0
    print(file_path.replace("/", "\\") + "开始处理。 时间为" + str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")
    try:
        print(log_name)
    except:
        traceback.print_exc()
    with open(log_name, "a") as f:
        f.write("{}开始处理。 时间为 ：".format(file_path.replace("/", "\\"))+ str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")

    if os.path.isdir(pdffolderpath):
        print('文件夹路径' + str(pdffolderpath) + '已存在')
        with open(error_name, "a") as f:
            f.write('文件夹路径' + str(pdffolderpath) + '已存在。处理时间为 ：' + str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")
        file_list = os.listdir(pdffolderpath)
        for single_file in file_list:
            n_folder_now = int(os.path.splitext(single_file)[0])
            if n_folder_now > n_folder_max:
                n_folder_max = n_folder_now
    else:
        os.mkdir(pdffolderpath)
    try:
        n_this_pdf = pdf.pageCount
        print(pdf.pageCount)
    except:
        n_this_pdf = pdf.page_count
    # for pg in range(0, n_this_pdf):
    if n_folder_max > n_this_pdf:
        n_folder_max = 0
        shutil.rmtree(pdffolderpath)
        os.mkdir(pdffolderpath)
        print(file[:-4].strip() + '现有文件夹中最大页数超过PDF最大页数，已重置')
        with open(error_name, "a") as f:
            f.write(file[:-4].strip() + '现有文件夹中最大页数超过PDF最大页数，已重置。处理时间为 ：' + str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")

    for pg in range(n_folder_max, n_this_pdf):
        page = pdf[pg]
        pic_name = str(pg + 1).zfill(4) + '.jpg'
        with open(log_name, "a") as f:
            f.write(pdffolderpath + pic_name + "    的处理时间为:  " + str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))+ "\n")
        save_pdf_pic_path = os.path.join(pdffolderpath, pic_name)
        find_save_color_pics_in_one_pdf(page, save_pdf_pic_path,COLOR_THRESHHOLD)
    with open(log_name, "a") as f:
        f.write("{}。 完成时间为 ：".format(file_path.replace("/", "\\"))+ str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")

    print(file_path + "完成处理。 时间为" + str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))) + "\n")
log_name = './log/底稿切分Pdf隔页运行日志_' + str(
        time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')
error_name = './log/底稿切分Pdf隔页运行错误日志_' + str(
    time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')


def find_save_color_pics_in_one_pdf(page, pic_path, COLOR_THRESHHOLD):
    trans = fitz.Matrix(1.0, 1.0).prerotate(0)
    pm = page.get_pixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
    sio = pm.tobytes()
    sio2 = BytesIO(sio)
    sio2.seek(0)
    img = Image.open(sio2)
    img = np.array(img)
    IMG_SP = img.shape
    # 新版的，向内移动了一部分避免孔洞填充
    cropped = img[int(IMG_SP[0] * 10 / 143):int(IMG_SP[0] * 50 / 143),
              int(IMG_SP[1] * 15 / 100):int(IMG_SP[1] * 45 / 100)]  # 裁剪坐标为[y0:y1, x0:x1]
    sum_sig = 0
    count_sig = 0
    for i in range(0, cropped.shape[0]):
        for j in range(0, cropped.shape[1]):
            # hsl中计算黑色时，下面的取rgb最大值小于等于46就是黑色，黑色计算偏差没有意义，注意png有一个透明层会使得判断失效
            if max(cropped[i, j]) > 46:
                sig_single = max(cropped[i, j]) - min(cropped[i, j])
                if sig_single > 5:
                    sum_sig += sig_single
                    count_sig += 1
    # avg_sig = sum_sig / (cropped.shape[0] * cropped.shape[1])
    if count_sig:
        avg_sig = sum_sig / count_sig
        if count_sig / (cropped.shape[0] * cropped.shape[1]) > 0.8 and avg_sig > COLOR_THRESHHOLD:
            trans = fitz.Matrix(1.5, 1.5).prerotate(0)
            pm = page.get_pixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
            pm.save(pic_path)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = CutPdfPic()
    myWin.show()
    sys.exit(app.exec_())