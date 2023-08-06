'''
这是将Ocr结果保存到excel表中
'''

try:
    from Function.sqlite_to_excel import fill_tb_index, find_parent_index, compute_new_filename_new_loc
    from Ui.OcrTableUi import Ui_OcrTable
    from Function.optionDb import getOption, InsertDb
except:
    from .Function.sqlite_to_excel import fill_tb_index, find_parent_index, compute_new_filename_new_loc
    from .Ui.OcrTableUi import Ui_OcrTable
    from .Function.optionDb import getOption, InsertDb
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
import os, time
import pandas as pd
import requests
import json
import sqlite3
import random
import traceback
'''

OCR的结果保存到Excel表中的方法

'''
def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
class OcrTable(QWidget, Ui_OcrTable):
    AllBtnEnbSignal = pyqtSignal()
    AllBtnDisSignal = pyqtSignal()
    #设置表格路径的信号
    TablePathSignal = pyqtSignal(str)
    #判断token过期的信号
    token_signal = pyqtSignal()
    def __init__(self, communication=None, token = ''):
        # super(OcrTable, self).__init__(communication)
        super().__init__(communication)
        self.setupUi(self)

        self.code = 1
        #设置按钮的信号连接
        self.SaveBtn.clicked.connect(self.startwork)
        self.improveBtn.clicked.connect(self.startwork)
        self.TablePathBtn.clicked.connect(self.setFilePath)
        self.file_name1 = ""

        self.name = ""
        self.communication = communication
        if token:
            self.token = token
        else:
            print("将OCR结果的内容保存到表中的token值为空")
            self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiOGNjNjgxOTY4MDNkIiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.3gwm3rH-lZqR7oOLi9vpNBrypSIMuHfYQ-pEklw8A0Q"
        print("这是输出OCR图片界面的Token值")
        print(self.token)
        self.user = ""
        self.run_code = 1
        self.UiInit()
        self.AllBtnEnbSignal.connect(self.all_btn_enb)
        self.AllBtnDisSignal.connect(self.all_btn_dis)
        self.TablePathSignal.connect(self.TablePath)
        self.token_signal.connect(self.tokenSignalFun)

    def tokenSignalFun(self):
        print("这是token过期触发的信号")

    def TablePath(self, word):
        if self.communication:
            self.communication.OcrTablePathSignal.emit(word)

    #初始化UI界面
    def UiInit(self):
        ui_list = getOption("SqlExcel")
        # 判断类型
        if isinstance(ui_list, list):
            if len(ui_list) == 1:
                self.tablePathEdit.setText(ui_list[0][1])
        elif isinstance(ui_list, str):
            pass
        else:
            self.textEdit.setText(str(ui_list))

    def setFilePath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if download_path:
            self.tablePathEdit.clear()
            self.tablePathEdit.setText(download_path)

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
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            # self.urldb = os.path.join( "../database" , "url.db")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                try:
                    QMessageBox.information(self,"warning","保存URl表不存在")
                except:
                    traceback.print_exc()
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
                print(self.token)
                print("这是判断token是否过期的网站")
                print(response.text)
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            if self.communication:
                                self.communication.Auto_token_signal.emit()
                                self.run_code = 0
                        num += 1
                else:
                    print("更新成功")
        except:
            self.run_code = 0
            traceback.print_exc()

    #设置全部按键不可点击
    def all_btn_dis(self):
        self.SaveBtn.setDisabled(True)
        self.improveBtn.setDisabled(True)

    def all_btn_enb(self):
        self.SaveBtn.setEnabled(True)
        self.improveBtn.setEnabled(True)


    def startwork(self):
        self.checkToken(6, "Sql内容保存到Excel")
        if self.run_code:
            # self.true_run()
    # def true_run(self):
            #传递按钮的文本
            sender_text = self.sender().text()
            self.thread1 = RunThread(self, sender_text)
            self.thread1.token = self.token
            self.thread1.user = self.user
            self.thread1.name = self.name
            self.thread1.start()
        else:
            # self.Warn_Signal.emit("warning","请登录后使用")
            self.PtextEdit.clear()
            self.PtextEdit.setPlainText('请登录后使用')


class RunThread(QThread):
    def __init__(self, communication, sender_text):
        super(RunThread, self).__init__()
        self.communication = communication
        self.user = ""
        self.token = ""
        self.sender_text = sender_text
        self.name = ""
        print(self.communication.communication)

    def sql_excel(self):
        db_file = os.path.join("./database", 'txt_OCR.db')
        conn = sqlite3.connect(db_file)
        df_ocr = pd.read_sql_query("select * from TB_OCR;", conn)
        conn.close()
        return df_ocr

    def run(self):
        self.start_time = str(get_now())
        if not os.path.exists('./log'):
            os.mkdir('./log')
        # 保存日志的名字
        try:
            self.communication.PtextEdit.clear()
            self.file_name = "./log/底稿识别OCR数据库内容保存到Excel运行日志_" + self.start_time + ".txt"
            log_path = os.path.join(os.getcwd(), self.file_name.replace("./", "")+".txt").replace("\\", "/")
            self.communication.PtextEdit.insertPlainText("保存运行日志的文件夹为："+log_path.split('log/')[0]+"log。\n运行日志文件名为："+log_path.split('log/')[1]+"\n")
        except:
            traceback.print_exc()
        with open(self.file_name, 'a' ) as f:
            f.write("[开始处理]" + self.start_time + "\n")
        try:
            sender_text = self.sender_text
            print(sender_text)
            df_ocr = self.sql_excel()
            if not os.path.exists(self.communication.tablePathEdit.text()):
                self.communication.PtextEdit.insertPlainText("文件路径不存在。\n")
                with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                    file.write("文件路径不存在。\n")
            else:
                if sender_text == "转存" :
                    now_time = self.start_time.replace("_", "")
                    print("表格保存位置为：", end="")
                    print(self.communication.tablePathEdit.text())
                    file_path =os.path.join(self.communication.tablePathEdit.text() ,"文档处理控制表【基于OCR识别结果校验】_"+now_time +".xlsx").replace("\\", '/')
                    print("========================")
                    print(file_path)
                    self.name = file_path
                    self.communication.name = file_path


                #判断数据库是否为空
                if df_ocr.empty:
                    self.communication.PtextEdit.insertPlainText("数据库为内容为空，建议检查后继续。\n")
                    with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                        file.write("数据库为内容为空，建议检查后继续。\n")
                    return False

                #判断使用手动输入的路径，还是通过路径行插入的路径
                try:
                    self.FileNum = int(self.communication.FileDeepEdit.text())
                except:
                    self.FileNum = ""
                if not self.FileNum:
                    self.FileNum = 3
                    print("默认切分的层级数字：", end="")
                    print(self.FileNum)
                if sender_text == "转存":
                    self.communication.AllBtnDisSignal.emit()
                    df_ocr.to_excel(file_path, index=False)
                    self.communication.PtextEdit.insertPlainText("从SQlite到excel完成")
                    self.communication.AllBtnEnbSignal.emit()
                    self.communication.TablePathSignal.emit(self.name)

                elif sender_text == "完善" :
                    self.communication.AllBtnDisSignal.emit()
                    file_path = self.name
                    print("========================")
                    print(file_path)

                    if os.path.isfile(file_path):
                        print("完善Excel功能按钮")
                        fill_tb_index(file_path)
                        find_parent_index(file_path)
                        compute_new_filename_new_loc(file_path, layer_file = self.FileNum)
                        self.communication.AllBtnEnbSignal.emit()
                        self.communication.PtextEdit.insertPlainText("完善excel完成\n")
                        with open(self.file_name, "a") as file:
                            file.write("完善excel完成\n")
                    else:
                        self.communication.PtextEdit.clear()
                        self.communication.PtextEdit.insertPlainText("请从SQlite中导出Excel，如已导出请关闭相关Excel!")
                        self.communication.AllBtnEnbSignal.emit()

                else:
                    print("未知按钮被触发。")
                    return False

        # except:
        #     traceback.print_exc()
        except  Exception as e:

            self.communication.AllBtnEnbSignal.emit()
            now = get_now()
            self.communication.PtextEdit.insertPlainText('[Error]' + str(get_now()) + "\n")
            self.communication.PtextEdit.insertPlainText('[报错内容]' + str(e) + "\n")
            if "No engine for filetype" in str(e):
                self.communication.PtextEdit.insertPlainText("后缀名不正确")
            self.communication.PtextEdit.insertPlainText('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
            self.communication.PtextEdit.insertPlainText('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[Error]' + str(get_now()) + "\n")
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
        self.checkToken1(6, "Sql内容保存到Excel")

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self,id,comments):
        try:
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            # self.urldb = os.path.join( "../database" , "url.db")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                QMessageBox.information(self,"warning","保存URl表不存在")
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.communication.get_url("commit")
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
                            if self.communication.communication:
                                self.communication.token_signal.emit()
                                self.run_code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    #检查是否包含不可命名的字符串
    def find_ilegal_character(self, txt):
        list_ilegal_character = []
        if '\\' in txt:
            list_ilegal_character.append('\\')
        if '/' in txt:
            list_ilegal_character.append('/')
        if ':' in txt:
            list_ilegal_character.append(':')
        if '*' in txt:
            list_ilegal_character.append('*')
        if '?' in txt:
            list_ilegal_character.append('?')
        if '"' in txt:
            list_ilegal_character.append('"')
        if '<' in txt:
            list_ilegal_character.append('<')
        if '>' in txt:
            list_ilegal_character.append('>')
        if '|' in txt:
            list_ilegal_character.append('|')
        if '\n' in txt:
            list_ilegal_character.append('回车')
        if '\t' in txt:
            list_ilegal_character.append('tab')
        return list_ilegal_character

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OcrTable()
    win.show()
    sys.exit(app.exec_())
