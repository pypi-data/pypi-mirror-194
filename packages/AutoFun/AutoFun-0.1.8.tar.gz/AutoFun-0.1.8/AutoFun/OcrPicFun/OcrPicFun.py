'''
这是Ocr图片的功能方法
'''
import traceback
import requests, json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os, time, random
try:

    from Function.get_json import get_json_baidu_nopos
    from Function.dict_to_json import src_dict_to_json
    from settings import  OCR_PIC_SIZE_THRESHOLD
    from Ui.OcrparameterUi import Ui_OcrParameter

except:
    from .Function.get_json import get_json_baidu_nopos
    from .Function.dict_to_json import src_dict_to_json
    from .settings import  OCR_PIC_SIZE_THRESHOLD
    from .Ui.OcrparameterUi import Ui_OcrParameter


from concurrent.futures import ThreadPoolExecutor
import sqlite3
import cv2
import numpy as np
from decimal import Decimal

def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

class OcrParameter(QWidget, Ui_OcrParameter):
    # 信号量1用于输出执行中的错误
    signal1 = pyqtSignal(str)
    # 用于输出内容不包含还原按钮
    signal2 = pyqtSignal(str)
    # 设置按钮可以点击的信号
    btn_signal = pyqtSignal()
    # token信号量
    token_signal = pyqtSignal()
    child_token_signal = pyqtSignal()
    # 警告信号量
    warning_signal = pyqtSignal(str)
    # Ocr_signal信号
    Ocr_signal = pyqtSignal(str)
    ProcessBar_signal = pyqtSignal(float)
    WidgetColorSignal = pyqtSignal(str)
    def __init__(self, communication=None, token = ""):
        # super(OcrParameter, self).__init__(communication)
        super().__init__(communication)
        self.setupUi(self)

        self.user = ""
        self.communication = communication
        if token:
            self.token = token
        else:
            print("OCR图片界面初始化的token值为空")
            # self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiOGNjNjgxOTY4MDNkIiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.3gwm3rH-lZqR7oOLi9vpNBrypSIMuHfYQ-pEklw8A0Q"
            # self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE"
            self.token = "1eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE"
        print("这是输出OCR图片界面的Token值")

        print(self.token)
        self.FilePath = r"E:\00Pic"

        # 设置开始线程按钮
        self.pushButton.clicked.connect(self.startOcr)
        # 设置信号用于输出
        self.signal1.connect(self.reloadBtn)

        self.token_signal.connect(self.check_token)
        self.child_token_signal.connect(self.closeMain)
        self.warning_signal.connect(self.showWarning)
        self.signal2.connect(self.printtext)
        #Ocr变更的信号量
        self.Ocr_signal.connect(self.changeOcrNum)
        self.ProcessBar_signal.connect(self.ChangeProcessBar)
        self.WidgetColorSignal.connect(self.WidgetColorFun)

    def WidgetColorFun(self, statu):
        if statu == "success":
            self.widget_2.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(32,205,32);")
        elif statu == "fail":
            self.widget_2.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(255,0,0);")
        else:
            self.widget_2.setStyleSheet("border-width: 2px;border-style: solid;border-color: rgb(0,0,0);")

    def ChangeProcessBar(self, num):
        if num < 1.1:
            self.OcrPBar.setValue(int(num * 100))
        else:
            self.OcrPBar.setValue(100)
            self.OcrPBar.setTextVisible(False)
            self.Finishlabel.setVisible(True)

    #Ocr改变的信号
    def changeOcrNum(self, ocrNum):
        self.OcrNum = int(ocrNum)
        self.ocrEdit.setText(str(ocrNum))

    #输出文本的内容
    def printtext(self, p_str):
        self.QtextEdit.insertPlainText(p_str)

    def showWarning(self, word):
        QMessageBox.information(self, "warning", word)

    def closeMain(self):
        #判断是否为别的函数调用启动
        if self.communication:
            # self.communication.token_singal.emit()
            pass

    def check_token(self):
        if self.communication:
            #检查token过期的信号量
            self.communication.token_singal.emit()
            self.thread1.terminate()

    def get_url(self, urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    # 初始化OCr数量
    def getOcrNum(self):
        # self.urldb = os.path.join("./database", "url.db")
        FilePath = os.path.dirname(__file__)
        FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
        self.urldb = os.path.join(FilePath, "url.db")
        if not os.path.exists(self.urldb):
            self.signal1.emit("保存URl表不存在")
            self.OcrNum = 0
            return False
        dbText = self.get_url("ocrnum")
        print("获取OCR数量的数据库查询单列内容")
        print(dbText)
        if dbText:
            url = dbText[0][1]
        headers = {
            "token": self.token
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            self.QtextEdit.insertPlainText(
                "状态码为：" + str(response.status_code) + "。网页返回值为" + str(response.text) + "获取可用OCR数量失败")
            self.OcrNum = 0
            self.ocrEdit.setText(str(self.OcrNum))
            return False
        else:
            response_json = response.json()
            self.OcrNum = int(response_json["data"]["n_ocr"])
            print("写入")
            self.ocrEdit.setText(str(self.OcrNum))

    # 开始线程代码
    def startOcr(self):
        if self.communication:
            print("从切分PDF隔页界面中获取参数")
            self.communication.OcrParamSignal.emit()
        self.Finishlabel.setVisible(False)
        self.OcrPBar.setValue(0)
        self.OcrPBar.setTextVisible(True)
        # print(self.OcrNum)
        # if  not self.communication:
        #     self.OcrNum = 1
        self.OcrNum = 1
        if int(self.OcrNum) > 0:
            self.true_run()
        else:
            self.WidgetColorSignal.emit("fail")
            QMessageBox.information(self, 'warning', "可用OCR数量为0，如需继续使用请联系技术人员")

    def true_run(self):
        try:
            self.pushButton.setDisabled(True)
            self.pushButton.setText("正在运行请稍等")
            self.QtextEdit.clear()
            root_path = self.FilePath
            self.thread1 = NowThread(
                user=self.user,
                communication=self,
                max_thread_number=4,
                root_path=root_path,
                token=self.token
            )
            print("可以的OCR数量")
            print(self.OcrNum)
            self.thread1.OCR_num = int(self.OcrNum)

            self.thread1.start()  # 开始线程
        except:
            traceback.print_exc()

    # 输出错误并将识别按钮设置为可以点击
    def reloadBtn(self, p_str):
        self.QtextEdit.insertPlainText(p_str)

        self.pushButton.setEnabled(True)
        self.pushButton.setText("识别")

    def end_thread(self):
        try:
            self.thread1.terminate()
            self.WidgetColorSignal.emit('fail')
        except:
            pass

class NowThread(QThread):

    def __init__(self, user, root_path, communication, max_thread_number, token):
        """
        :param communication:通讯使用的
        :param max_thread_number:最大线程数
        """
        super(NowThread, self).__init__()
        # 设置文件队列
        self.FilePath_list = []
        self.user = user
        self.OCR_num = 0
        self.runFirst = 1
        # token
        self.token = token
        # 文件路径
        self.root_path = root_path
        # 信号量
        self.communication = communication
        # 最大线程数量
        self.max_thread_number = max_thread_number
        # 查询结果的队列
        self.success_list = []
        self.code = 1
        # 程序运行的开始时间
        self.start_time = str(get_now())
        self.FinishList = []

    def run(self):
        print("调用上传执行功能的接口")
        self.checkToken1()
        # for i in range(10):
        #     time.sleep(random.uniform(0.4,1))
        #     self.communication.Ocr_signal.emit(str(i))
        # print("233333333333333333")
        # self.code =0
        print("是否需要执行", end = '')
        print(self.code)
        # self.code = 1
        if self.code:
            try:
                self.trun_run()
            except:
                traceback.print_exc()
                self.communication.WidgetColorSignal.emit("fail")

        else:
            self.communication.WidgetColorSignal.emit("fail")
            # self.communication.signal2.emit("请登录后使用！")
            self.communication.signal1.emit("请登录后使用！")

    #当图片大小大于所限制的大小时，会调用此方法将图片进行大小的缩放
    def cut_jpg(self, pic_path):
        img = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imencode('.jpg', img)[1].tofile(pic_path)
        size_pic = os.path.getsize(pic_path)
        while size_pic > OCR_PIC_SIZE_THRESHOLD:
            para_resize = (size_pic / OCR_PIC_SIZE_THRESHOLD) ** 0.5
            para_resize = Decimal(para_resize).quantize(Decimal("0.00")) + Decimal(0.01).quantize(Decimal("0.00"))
            img = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            x, y = img.shape[0:2]
            img = cv2.resize(img, (int(y / para_resize), int(x / para_resize)))
            cv2.imencode('.jpg', img)[1].tofile(pic_path)
            size_pic = os.path.getsize(pic_path)

    #添加OCR额度请求函数
    def AddOcrNum(self, num ):
        print("需要添加的OCR数字：", end = "")
        print(num)

    def trun_run(self):
        if not os.path.exists("./log"):
            os.mkdir("./log")
        # 底稿OCR日志文件名字
        self.loggin_name = "./log/底稿OCR运行日志_" + self.start_time + '.txt'
        log_path = os.path.join(os.getcwd(), self.loggin_name.replace("./", "")).replace("\\", "/")

        self.communication.signal2.emit("保存日志的文件夹为：" + log_path.split('log/')[0] + "log。\n日志文件名为：" + log_path.split('log/')[1] + "\n")
        with open(self.loggin_name, 'a') as f:
            f.write("[开始处理]" + self.start_time + "\n")
        self.communication.signal2.emit('开始OCR图片\n')

        # 判断路劲是否存在，并且将路劲下的.jpg文件保存到列表中
        if os.path.exists(self.root_path):
            file_list = []
            print("OCR数量："+ str(self.OCR_num))
            run_code = 1
            for parent, dirs, files in os.walk(self.root_path):
                for file in files:
                    if '.jpg' in file and not (os.path.isfile(os.path.join(parent, file[:-4] + '.json'))):
                        file_path = os.path.join(parent, file)
                        file_list.append(file_path)
                        print(file_path)
                        # 如果文件的大小大于4194300
                        if os.stat(file_path).st_size > OCR_PIC_SIZE_THRESHOLD:
                            self.cut_jpg(file_path)
                        try:
                            if os.stat(file_path).st_size == 0:
                                self.communication.warning_signal.emit(file_path + "大小为0KB")
                                self.communication.signal1.emit(file_path.replace("\\", "/") + "大小为0KB。请检查后继续。\n")
                                self.communication.WidgetColorSignal.emit("fail")
                                run_code = 0
                        except:
                            traceback.print_exc()
            self.file_list = file_list
            print(self.file_list)
            if self.communication.OcrRequestsCheckBox.isChecked():
                if len(file_list) > self.OCR_num:
                    self.AddOcrNum(len(file_list) - self.OCR_num)
            # 创建线程，使用线程执行识别
            if run_code and self.OCR_num:
                try:
                    with ThreadPoolExecutor(max_workers=4) as pool:
                        results = pool.map(self.action, file_list)
                        print('--------------')
                        self.communication.WidgetColorSignal.emit("success")
                except:
                    traceback.print_exc()
                if self.code:
                    self.communication.signal1.emit("运行结束，请检查文件")
                    with open(self.loggin_name, 'a') as f:
                        f.write("运行结束，请检查文件" + "\n")
                    # 执行最后一次插入操作
                else:
                    self.communication.signal1.emit("发生错误")
                    self.communication.WidgetColorSignal.emit("fail")
                    with open(self.loggin_name, 'a') as f:
                        f.write("发生错误" + "\n")

        else:
            self.communication.signal1.emit("文件路径不存在!")
            with open(self.loggin_name, 'a') as f:
                f.write("文件路径不存在!" + "\n")

    # 执行主函数
    def action(self, jpgFilePath):
        print(self.OCR_num)
        if self.OCR_num == 0:
            self.communication.signal2.emit("OCR可用数量为0\n")
        if self.code and self.OCR_num > 0:

            parent, file = os.path.split(jpgFilePath)
            #获取百度无坐标内容
            response_json = get_json_baidu_nopos(jpgFilePath)
            self.response_json = response_json
            print(self.response_json)

            if response_json:
                # 如果正常识别则保存
                if "error_code" not in response_json:
                    self.checkToken()
                    self.checkOcrNum()
                    src_dict_to_json(file[:-4], parent, response_json)

                    self.success_list.append(jpgFilePath)
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "  识别成功保存JSON文件" + "\n")
                    # self.FilePath_list.append(jpgFilePath)
                    print("当前进度为：",end= '')
                    self.FinishList.append(jpgFilePath)
                    num = len(self.FinishList)/len(self.file_list)
                    print(num)
                    self.communication.ProcessBar_signal.emit(num)

                # 如果状态码为
                elif response_json['error_code'] == 111:
                    self.code = 0
                    self.communication.signal1.emit("token过期，请重新获取后再执行代码\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "  token过期，请重新获取后再执行代码\n" + "\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")

                elif response_json['error_code'] == 110:
                    self.code = 0
                    self.communication.signal1.emit("token过期，请重新获取后再执行代码\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "  token过期，请重新获取后再执行代码\n" + "\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")

                elif response_json['error_code'] == 282000:
                    self.code = 0
                    self.communication.signal1.emit(
                        jpgFilePath + "  错误码的原因可能是您上传的图片中文字过多，""识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请联系技术支持团队" + "\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")

                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "  如果您使用的是高精度接口，报这个错误码的原因可能是您上传的图片中文字过多，"
                                              "识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请技术支持团队" + "\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")

                elif response_json['error_code'] == 17:
                    self.code = 0
                    self.communication.signal1.emit("免费资源测试完毕，请求超时，请您稍后再试，或者联系工作人员" + "\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + " 免费资源测试完毕，请求超时，请您稍后再试，或者联系工作人员\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")

                # elif response_json['error_code']==18:
                elif response_json['error_code'] == 18:
                    self.communication.signal1.emit("QPS超限额，正常尝试延迟访问，请稍后。" + "\n")
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "QPS超限额，正常尝试延迟访问，请稍后。\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                    self.retry(jpgFilePath=jpgFilePath)

                elif response_json['error_code'] == 216202:
                    self.code = 0
                    self.communication.signal1.emit("图片的base64编码大小大于4M,请修改文件大小后继续。文件名为： \n" + jpgFilePath + "\n")
                    self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                    with open(self.loggin_name, 'a') as f:
                        f.write("图片的base64编码大小大于4M,请修改文件大小后继续。文件名为： \n" + jpgFilePath + "\n")
                        f.write("error_msg " + response_json['error_code'] + "\n")

            else:
                print("返回结果为空")
                with open(self.loggin_name, 'a') as f:
                    f.write(jpgFilePath + "识别结果为空 \n")
                    f.write("error_msg " + response_json['error_code'] + "\n")
                self.communication.signal1.emit(jpgFilePath + "识别返回内容为空")
        else:
            if self.runFirst:
                self.runFirst = 0

    def checkToken(self):
        try:
            print(self.communication.token)
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                self.communication.signal1.emit("保存URl表不存在")
                self.code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": 4,
                    "comments": "【OCR执行返回】:{file}".format(file=self.response_json),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                # print(response.text)
                response.json()
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(2, 3))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            self.communication.child_token_signal.emit()
                            self.code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    def checkToken1(self):
        try:
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                self.communication.signal1.emit("保存URl表不存在")
                self.code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": 4,
                    "comments": "【OCR开始】",
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                # print(response.text)
                response.json()
                if response.status_code != 200:
                    print("上传功能接口返回的网页界面不为200")
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            self.communication.child_token_signal.emit()
                            self.code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()

    def checkOcrNum(self):

        try:
            # self.urldb = os.path.join("./database", "url.db")
            FilePath = os.path.dirname(__file__)
            FilePath = FilePath.replace(FilePath.split("/")[-1], "database")
            self.urldb = os.path.join(FilePath, "url.db")
            if not os.path.exists(self.urldb):
                self.communication.signal1.emit("保存URl表不存在")
                self.code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commitocr")
            print("Url信息表内的提交接口的信号")
            print(dbText)
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": 4,
                    "comments": "获取OCr数量",
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                print("Ocr数量接口返回的内容")
                print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
                print(response)
                print(self.token)
                # print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
                self.OCR_num = int(response.json()["data"]["n_ocr"])
                self.communication.Ocr_signal.emit(str(self.OCR_num))

                if response.status_code != 200:

                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(2, 3))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            self.communication.child_token_signal.emit()
                            self.code = 0
                        num += 1
                else:
                    print("修改OCr数量")

        except:
            traceback.print_exc()

    def retry(self, jpgFilePath):
        num = 0
        while num < 5:
            time.sleep(random.uniform(4, 6))
            if self.code:
                parent, file = os.path.split(jpgFilePath)
                response_json = get_json_baidu_nopos(jpgFilePath, self.token)
                self.response_json = response_json
                # print(response_json)
                if response_json:
                    # 如果正常识别则保存
                    self.checkToken()
                    self.checkOcrNum()
                    if "error_code" not in response_json:
                        src_dict_to_json(file[:-4], parent, response_json)
                        self.success_list.append(jpgFilePath)
                        with open(self.loggin_name, 'a') as f:
                            f.write(jpgFilePath + "  识别成功保存JSON文件" + "\n")
                        # self.FilePath_list.append(jpgFilePath)
                        break

                    # 如果状态码为
                    elif response_json['error_code'] == 111:
                        self.code = 0
                        self.communication.signal1.emit("token过期，请重新获取后再执行代码\n")
                        self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                        with open(self.loggin_name, 'a') as f:
                            f.write(jpgFilePath + "  token过期，请重新获取后再执行代码\n" + "\n")
                            f.write("error_msg " + response_json['error_code'] + "\n")
                        break

                    elif response_json['error_code'] == 282000:
                        self.code = 0
                        self.communication.signal1.emit(
                            jpgFilePath + "  错误码的原因可能是您上传的图片中文字过多，""识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请联系技术支持团队" + "\n")
                        self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")

                        with open(self.loggin_name, 'a') as f:
                            f.write(jpgFilePath + "  如果您使用的是高精度接口，报这个错误码的原因可能是您上传的图片中文字过多，"
                                                  "识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请技术支持团队" + "\n")
                            f.write("error_msg " + response_json['error_code'] + "\n")
                        break

                    elif response_json['error_code'] == 17:
                        self.code = 0
                        self.communication.signal1.emit("免费资源测试完毕，请求超时，请您稍后再试，或者联系工作人员" + "\n")
                        self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                        with open(self.loggin_name, 'a') as f:
                            f.write(jpgFilePath + " 免费资源测试完毕，请求超时，请您稍后再试，或者联系工作人员\n")
                            f.write("error_msg " + response_json['error_code'] + "\n")
                        break

                    elif response_json['error_code'] == 18:
                        if self.code == 4:
                            self.code = 0
                        self.communication.signal1.emit("QPS超限额，正常尝试延迟访问，请稍后。" + "\n")
                        with open(self.loggin_name, 'a') as f:
                            f.write(jpgFilePath + "QPS超限额，正常尝试延迟访问，请稍后。\n")
                            f.write("error_msg " + response_json['error_code'] + "\n")
                        self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                        num += 1

                    elif response_json['error_code'] == 216202:
                        self.code = 0
                        self.communication.signal1.emit("图片的base64编码大小大于4M,请修改文件大小后继续。文件名为： \n" + jpgFilePath + "\n")
                        self.communication.signal1.emit("error_msg " + response_json['error_code'] + "\n")
                        with open(self.loggin_name, 'a') as f:
                            f.write("图片的base64编码大小大于4M,请修改文件大小后继续。文件名为： \n" + jpgFilePath + "\n")
                            f.write("error_msg " + response_json['error_code'] + "\n")
                        break
                else:
                    print("返回结果为空")
                    with open(self.loggin_name, 'a') as f:
                        f.write(jpgFilePath + "识别结果为空 \n")
                        f.write("error_msg " + response_json['error_code'] + "\n")
                    self.communication.signal1.emit(jpgFilePath + "识别返回内容为空")
                    break
            else:
                num += 1

    def get_url(self, urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OcrParameter()
    win.show()
    sys.exit(app.exec_())
