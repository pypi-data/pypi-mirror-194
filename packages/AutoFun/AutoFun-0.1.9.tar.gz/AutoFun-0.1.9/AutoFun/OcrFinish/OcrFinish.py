'''
这是判断Ocr是否完成的主判断功能
'''
try:
    from Ui.OcrfinishUi import Ui_OcrFinish
except:
    from .Ui.OcrfinishUi import Ui_OcrFinish
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, time
import traceback
import requests
import json
import sqlite3
import random
import sys

def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
style = '''
QTabWidget::pane {
    border-top: 1px solid #E5E5E5;
    background-color:#FFFFFF;
}

QTabWidget QTabBar::tab {
    border-bottom: 2px solid rgba(0,0,0,0);
    min-width: 70px; /*不要太大就可以使得border宽度和字体一样宽*/
    margin-left:25px; /*用来隔开每个tab*/
    margin-right-25px;
    padding-top: 14px;
    padding-bottom:14px;
    color:#444;
    background-color:#fafafa;
}

QTabBar::tab:hover{
    color:rgb(198, 47, 47);
}

QTabBar::tab:selected {
    color:rgb(198, 47, 47);
    background-color:#fafafa;
    border-bottom: 2px solid rgb(198, 47, 47);
    /*border-bottom: 2px solid #2080F7;*/
    /*font-weight:bold;*/
}

QTabWidget::tab-bar {
    border-top: 2px solid #E5E5E5;
    border-bottom: 2px solid #E5E5E5;
    border-left:1px solid #E5E5E5;
    alignment: center;
    font-size: 17px;
    background-color:#fafafa;
}


QScrollArea{
    border:0px;
}

#Main_widget{
    font-family:Microsoft YaHei;
    background-color:#fafafa;
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
class OcrFinish(QWidget, Ui_OcrFinish):
    #警告信号
    Warn_Signal = pyqtSignal(str, str)
    Qwarn_Signal = pyqtSignal()
    #进程池信号
    ProcessBar_signal = pyqtSignal(float)
    WidgetColorSignal = pyqtSignal(str)
    def __init__(self, communication=None, token = ""):
        # super(OcrFinish, self).__init__(communication)
        super().__init__(communication)
        self.setupUi(self)
        self.setStyleSheet(style)
        self.OcrPath = ""
        self.btn2.clicked.connect(self.startWork)
        self.run_code = 1
        self.communication = communication
        if token:
            self.token = token
        else:
            print("判断OCR结果是否完成的界面的token值为空")
            self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiOGNjNjgxOTY4MDNkIiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.3gwm3rH-lZqR7oOLi9vpNBrypSIMuHfYQ-pEklw8A0Q"
        print("这是输出OCR图片界面的Token值")
        print(self.token)
        self.user = ""
        self.Warn_Signal.connect(self.warnInfo)
        self.ProcessBar_signal.connect(self.ChangeProcessBar)
        self.WidgetColorSignal.connect(self.WidgetColorFun)

    def WidgetColorFun(self, statu):
        if statu == "success":
            self.widget_3.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(32,205,32);")
        elif statu == "fail":
            self.widget_3.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(255,0,0);")
        else:
            self.widget_3.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(0,0,0);")

    def ChangeProcessBar(self, num):
        if num < 1.1:
            self.OcrFinishPBar.setValue(num * 100)
        else:
            self.OcrFinishPBar.setValue(100)
            self.OcrFinishPBar.setTextVisible(False)
            self.Finishlabel.setVisible(True)
            self.WidgetColorSignal.emit("success")
            # self.OcrFinishPBar.setValue(T)

    def warnInfo(self, warntype, text):
        QMessageBox.information(warntype, text)

    def get_url(self, urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    def checkToken(self, id, comments):
        try:
            # print(self.communication.token)
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            # self.urldb = os.path.join( "../database" , "url.db")
            self.urldb = os.path.join(FilePath, "url.db")
            print("保存url信息表的路径", end="")
            print(self.urldb)
            print(os.getcwd())
            if not os.path.exists(self.urldb):
                QMessageBox.information(self, "warning", "保存URl表不存在")
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
                            #token过期使用的信号
                            # self.communication.token_singal.emit()
                            self.run_code = 0
                            print("这里是设置token过期要使用的")
                        num += 1
                else:
                    print("更新成功")
        except:
            self.run_code = 0
            traceback.print_exc()

    def warn_code(self):  # 关闭窗口触发以下事件
        a = QMessageBox.question(self, 'warning', '注意：检查通过后会清空历史OCR数据存入新OCR数据', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a != QMessageBox.Yes:
            # self.thread1.run_code = 0
            self.run_code = 0
        else:
            self.run_code = 1



    def startWork(self):
        self.Finishlabel.setVisible(False)
        self.OcrFinishPBar.setValue(0)
        self.OcrFinishPBar.setTextVisible(True)
        # self.run_code = 1
        self.checkToken(5, "Json保存到Sql")
        if self.run_code:
            self.warn_code()
            self.WidgetColorSignal.emit("")
            if self.communication:
                print("")
                self.communication.OcrFinishSignal.emit()
            if self.run_code:
                print("启动线程")
                self.thread1 = RunThread(self)
                self.thread1.token = self.token
                self.thread1.user = self.user
                self.thread1.root_path = self.OcrPath
                self.thread1.start()
            else:
                print("不启动线程")
        else:
            self.WidgetColorSignal.emit("fail")
            # self.Warn_Signal.emit("warning","请登录后使用")
            self.QtextEdit.clear()
            self.QtextEdit.setPlainText('请登录后使用')

class RunThread(QThread):
    def __init__(self, communication):
        super(RunThread, self).__init__()
        self.communication = communication
        self.run_code = 1
        self.user = ""
        self.token = ""
        self.same_code = 1
        # self.root_path = r"D:\0000需要OCR图片的位置"

    def run(self):
        print("线程执行主函数")
        print(self.root_path)
        if self.run_code:
            self.true_run()

    def get_url(self, urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self, id, comments):
        try:
            # print(self.communication.token)
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            print(FilePath)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            # self.urldb = os.path.join( "../database" , "url.db")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                self.communication.Warn_Signal.emit( "warning", "保存URl表不存在")
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
                            #token过期要使用的信号
                            # self.communication.token_singal.emit()
                            self.run_code = 0
                            print("这里是设置token过期要使用的")
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    def true_run(self):
        self.start_time = str(get_now())
        self.communication.QtextEdit.clear()
        self.communication.btn2.setDisabled(True)
        self.communication.btn2.setText("正在运行请稍等")
        if not os.path.exists("./log"):
            os.mkdir("./log")
        # 保存日志的名字
        self.file_name = "./log/底稿隔页识别结果的Json保存数据库运行日志_" + self.start_time + '.txt'
        with open(self.file_name, 'a') as f:
            f.write("[开始处理]" + self.start_time + "\n")
        try:
            # self.root_path = r"D:\0000需要OCR图片的位置"
            # 获取jpg和json文件的列表
            if os.path.exists(self.root_path):
                json_file_list = []
                json_file_set = set()
                jpg_file_set = set()
                jpg_file_list = []
                for parent, dirs, files in os.walk(self.root_path):
                    for file in files:
                        if '.json' in file:
                            file_path = os.path.join(parent, file)
                            json_file_set.add(file_path[:-5])
                            json_file_list.append(file_path)
                        elif ".jpg" in file:
                            file_path = os.path.join(parent, file)
                            jpg_file_set.add(file_path[:-4])
                            jpg_file_list.append(file_path)


                self.communication.btn2.setEnabled(True)
                self.communication.btn2.setText("单步执行")

                # #忽略json不匹配的情况
                # if self.cb1.checkState() == Qt.Checked:
                #     self.QtextEdit.insertPlainText("忽略json文件和图片文件不匹配的情况")
                #     self.same_code = 0
                # print(self.same_code)

                # 是否要判断json文件和jpg文件数量相等
                if self.same_code:
                    is_same = self.is_same_file(json_file_set, jpg_file_set)
                    if not is_same:
                        return False
                    else:
                        self.communication.QtextEdit.insertPlainText("数量相同开始下一步" + "\n")
                # 获取JSON并且保存到SQlite数据库中
                print("开始创建数据表\n")
                create_code = self.create_tb()
                if not create_code:
                    return False

                print("将json写入到sqlit中\n")
                for i in json_file_list:
                    self.communication.ProcessBar_signal.emit(json_file_list.index(i) / len(json_file_list))
                    self.Json_to_sqlit(i)
                self.communication.ProcessBar_signal.emit(1.1)
                self.communication.QtextEdit.insertPlainText("插入数据库执行完成")

            else:
                self.communication.btn2.setEnabled(True)
                self.communication.btn2.setText("单步执行")
                self.communication.QtextEdit.insertPlainText("文件路径不存在!" + "\n")
        except  Exception as e:

            self.communication.Warn_Signal.emit("warning", "参数不对，程序报错，请重新输入")
            now = get_now()
            self.communication.QtextEdit.insertPlainText(str(e))
            with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[Error]' + str(get_now()) + "\n")
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")

        self.checkToken1(5, "Json保存到Sql")

    # 创建数据表主逻辑
    def create_tb(self):
        try:
            Db_path = r'.\database'
            if not os.path.exists(Db_path):
                os.makedirs(Db_path)
            db_file = os.path.join(Db_path, 'txt_OCR.db')
            if os.path.isfile(db_file):
                os.remove(db_file)
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            cursor.execute(
                'create table TB_OCR(filename varchar(255) , OCRtxt varchar(720), n_page varchar(5), min_score varchar(50), avg_score varchar(50))')
            # cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
            # cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
            cursor.close()
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            self.communication.QtextEdit.insertPlainText('[Error]' + str(get_now()) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错内容]' + str(e) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            self.communication.QtextEdit.insertPlainText('如已打开目标文件，请关闭后重新尝试！')
            with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[Error]' + str(get_now()) + "\n")
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            return False

    def Json_to_sqlit(self, file_path):
        # 创建数据表
        # 当前路径名字
        self.file_name11 = file_path
        try:
            # self.communication.QtextEdit.insertPlainText("开始写入" + file_path + "\n")
            Db_path = r'.\database'
            if not os.path.exists(Db_path):
                os.makedirs(Db_path)
            db_file = os.path.join(Db_path, 'txt_OCR.db')
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            with open(file_path, encoding="utf-8") as f:
                json_text = json.load(f)
                word_reslt_list = json_text["words_result"]
                # 平均值和最小值为识别内容的平均值和最小值的平均值， 识别文本为所有返回结果文本的值的合集
                OCRtxt = "".join([str(i["words"]) for i in word_reslt_list])
                print(OCRtxt)
                avg_score = sum([i["probability"]["average"] * len(i["words"]) for i in word_reslt_list]) / len(OCRtxt)
                min_score = sum([i["probability"]["min"] * len(i["words"]) for i in word_reslt_list]) / len(OCRtxt)

                # 第几页
                n_page = int(file_path.split("\\")[-1].replace(".json", ""))
                filename = file_path.split("\\")[-2]
                if "/" in filename:
                    filename = filename.split("/")[-2]
                print(filename)
                print(file_path)

                try:
                    sql = r"insert into TB_OCR values ('{filename}','{OCRtxt}',  '{n_page}', '{min_score}', '{avg_score}')" \
                        .format(OCRtxt=OCRtxt, filename=filename, n_page=n_page, min_score=min_score,
                                avg_score=avg_score)
                    print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                        file.write(self.file_name11 + "___" + self.start_time + "___写入数据库成功\n")
                except Exception as e:
                    conn.rollback()
                    self.communication.QtextEdit.insertPlainText(self.file_name11 + " " + str(e) + "\n")
                    QMessageBox.information(self, "warning", self.file_name11 + " " + str(e) + "\n")
                    with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                        file.write('[Error]' + str(get_now()) + "\n")
                        file.write('[报错内容]' + str(e) + "\n")
                        file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                        file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
                finally:
                    cursor.close()
                    conn.close()

                return True

        except Exception as e:
            self.communication.QtextEdit.insertPlainText('[Error]' + str(get_now()) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错内容]' + str(e) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
            self.communication.QtextEdit.insertPlainText('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            with open(self.file_name, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[Error]' + str(get_now()) + "\n")
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            return False

    # 判断JSON文件和JPG文件是否对应，并输出其中多余的文件名字以及位置
    def is_same_file(self, json_file_set, jpg_file_set):
        json_jpg = json_file_set - jpg_file_set
        for i in json_jpg:
            print("JSON文件多余，其文件名为:" + i + ".json")
            self.communication.QtextEdit.insertPlainText("JSON文件多余，其文件名为:" + i + ".json\n")
        jpg_json = jpg_file_set - json_file_set
        for i in jpg_json:
            print("JPG文件多余，其文件名为:" + i + ".jpg")
            self.communication.QtextEdit.insertPlainText("JPG文件多余，其文件名为:" + i + ".jpg\n")
        if not json_jpg and not jpg_json:
            return True
        else:
            return False


if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = OcrFinish()
    myWin.show()
    sys.exit(app.exec_())