'''这是获取隔页的主方法'''
# -*- coding:utf-8 -*-

import datetime
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
print("===============================")
print(os.path.dirname(__file__))
print(os.getcwd())
from multiprocessing import freeze_support

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

def get_pdf_color_page(file_path, save_pic_path, log_name, error_name, COLOR_THRESHHOLD):
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



if __name__ == '__main__':
    log_name = './log/底稿切分Pdf隔页运行日志_' + str(
        time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')
    error_name = './log/底稿切分Pdf隔页运行错误日志_' + str(
        time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + '.txt')
    if not os.path.exists("./log"):
        os.mkdir('./log')
    try:
        freeze_support()
        print(sys.argv)
        # src_pdf_path =  sys.argv[1]
        # save_pic_path =  sys.argv[2]
        # COLOR_THRESHHOLD =  int(sys.argv[4])
        # processors = sys.argv[3]
        src_pdf_path = r"E:\000old"
        save_pic_path = r"E:\000save"
        COLOR_THRESHHOLD = 19
        processors = 4
        # src_pdf_path = r"E:\0"
        # save_pic_path =  r"E:\1"
        # COLOR_THRESHHOLD =  19
        # processors = 4
        # src_pdf_path = r'E:\3\0'
        # save_pic_path = r'E:\3\1'
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
        #判断
        if len(pdf_list):
            #如果文件数量小于进程数量，那么按文件数量来启动进程。
            if len(pdf_list) <  int(processors) :
                processors =len(pdf_list)
            p = Pool(processes=  int(processors))

            # p.map(partial(get_pdf_color_page, save_pic_path=save_pic_path,log_name=log_name, error_name=error_name, COLOR_THRESHHOLD=int(COLOR_THRESHHOLD)), pdf_list)
            li = []
            for i in pdf_list:
                res = p.apply_async(get_pdf_color_page, args=(i,save_pic_path, log_name, error_name, COLOR_THRESHHOLD))
                li.append(res)
            p.close()
            p.join()
            print('结束时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            print("原文件夹为空，或者均已OCR请确认后再次输入")

    except  Exception as e:
        traceback.print_exc()
        try:
            with open(log_name, "a") as file:
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
        except:
            traceback.print_exc()



