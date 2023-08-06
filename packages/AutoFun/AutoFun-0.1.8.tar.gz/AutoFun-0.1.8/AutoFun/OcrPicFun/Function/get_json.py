# encoding:utf-8
#服务器IP有变动，获取返回值时大约每几百个会有一次服务器不响应断开，需要加上异常捕捉机制，如果崩了就暂停几十秒再继续运行，最后最好再验证一下json个数和jpg个数是否对的上
import os
import traceback

import requests
import base64
from requests.adapters import HTTPAdapter
import random
# from SETTING import OCR_API
import time
import pickle
'''
合合表格识别
'''
list_request_url=[
    "http://www.rongdakeji.net:10020/icr/recognize_multi_table_raw",
    "http://www.rongdakeji.net:10021/icr/recognize_multi_table_raw",
]

def get_json_ocr(pic_path):
    if OCR_API=='baidu':
        return get_json_baidu(pic_path)
    elif OCR_API=='baidu_no_pos':
        return get_json_baidu_nopos(pic_path)
    else:
        return get_json_hehe(pic_path)

def get_json_hehe(pic_path):
    # request_url = "http://114.241.107.154:10020/icr/recognize_multi_table_raw"
    # request_url = "http://114.241.108.194:10020/icr/recognize_multi_table_raw"
    # request_url = "http://114.241.105.139:10020/icr/recognize_multi_table_raw"
    # request_url = "http://www.rongdakeji.net:10020/icr/recognize_multi_table_raw"
    # request_url = "http://www.rongdakeji.net:10021/icr/recognize_multi_table_raw"

    request_url = random.sample(list_request_url, 1)[0]
    files = {"file": open(pic_path, "rb")}
    headers = {'Connection': 'close'}
    response = requests.post(request_url, files=files, headers=headers)
    print(response.json()["error_code"])
    if response:
        # print (response.json())
        return response.json()
    else:
        return get_json_baidu(pic_path)

# access_token = '24.6729eac17564756c7286ad13bde70b80.2592000.1634186279.282335-24846560'
# <<<<<<< HEAD
# access_token = '24.84f8400f748bdf1fe8dd71d443b99166.2592000.1634211575.282335-24393717'#yyt

print(os.getcwd())
f2 = open("td.txt", "rb")

# 从 tmp.txt 中读取并恢复 obj 对象
obj2 = pickle.load(f2)
f2.close()
# traceback.print_exc()
#---------------------------------------------------------------------------------------------
access_token = obj2

# access_token = '24.1a440167b8643947628bf8833acc92ff.2592000.1643449254.282335-24846560'
# >>>>>>> f65f39ee870893a5b91b83392fb0e9d15bc35e20

def get_json_baidu(pic_path):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    f = open(pic_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img,"detect_direction": 'true',"probability": 'true',}
    # params = {"image": img,"detect_direction": 'false',"probability": 'ture',}
    # params = {"image": img,}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    while True:
        # response = requests.post(request_url, data=params, headers=headers)
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            response_json = response.json()
            if not 'error_code' in response_json:
                ocr_goal=response.json()
                break
            elif str(response_json['error_code'])==str(282000):
                ocr_goal = get_json_hehe(pic_path)
                break
            else:
                print(response_json)
                time.sleep(2)
    return  ocr_goal

def get_json_baidu_nopos(pic_path):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    f = open(pic_path, 'rb')
    img = base64.b64encode(f.read())
    # params = {"image": img,"detect_direction": 'true',"probability": 'true','paragraph': 'true',}
    params = {"image": img,"detect_direction": 'true',"probability": 'true',}
    # params = {"image": img,}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        return response.json()
    else:
        return False
    # while True:
    #     response = requests.post(request_url, data=params, headers=headers)
    #     if response:
    #         response_json = response.json()
    #         if not 'error_code' in response_json:
    #             ocr_goal=response.json()
    #             response.close()
    #             break
    #         elif 'error_code'==str(282000):
    #             ocr_goal = get_json_hehe(pic_path)
    #             response.close()
    #             break
    #         else:
    #             print(response_json)
    #             response.close()
    #             time.sleep(2)
    #     # else:
        #     response.close()
    return  ocr_goal


if __name__ == '__main__':
    # pic_path=r'C:\Users\RD-PC\Desktop\新建文件夹 (4)\2018-9-7-0010发票.pdf - Adobe Acrobat Pro DC.jpg'
    # pic_path=r'C:\Users\RD-PC\Desktop\未标题提取页面 .pdf - Adobe Acrobat Pro DC.jpg'
    # pic_path=r'C:\Users\RD-PC\PycharmProjects\hehe_tb_parse\Adobe Acrobat Pro DC.jpg'
    # pic_path=r'C:\Users\RD-PC\Desktop\新建 DOCX 文档.jpg'
    pic_path=r'E:\2\0002.jpg'
    # pic_path=r'C:\Users\RD-PC\Desktop\hehedemo\崔红叶银行卡流水.pdf'
    # access_token='24.79bcbb109cf1f5b5e84df0a8e065289e.2592000.1606462834.282335-22889530'
    # msg_hehetb=get_json_hehe(pic_path)
    # msg_hehetb=get_json_baidu(pic_path)
    msg_hehetb=get_json_baidu_nopos(pic_path)
    print(msg_hehetb)
