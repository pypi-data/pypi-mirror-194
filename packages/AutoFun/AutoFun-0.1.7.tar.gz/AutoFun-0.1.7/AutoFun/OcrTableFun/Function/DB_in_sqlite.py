# -*- coding: utf-8 -*-

import os, sqlite3
import pandas as pd

def creat_tb():
    db_file = os.path.join('./database', 'txt_OCR.db')
    if os.path.isfile(db_file):
        os.remove(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
    try:
        cursor.execute('create table TB_OCR(filename varchar(255) ,OCRtxt varchar(720), n_page varchar(5), min_score varchar(50), avg_score varchar(50))')
    # cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
    # cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
        cursor.close()
        conn.commit()
        return
    except Exception as e:
        conn.rollback()
        return e
    finally:
        conn.close()

# 初始数据:
def insert_one_data_TB_OCR(filename,OCRtxt,n_page,min_score,avg_score):
    db_file = os.path.join(os.path.dirname(__file__), 'txt_OCR.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
    # cursor.execute('create table TB_OCR(filename varchar(255) , n_page varchar(5), score varchar(50))')
    cursor.execute(r"insert into TB_OCR values ('{filename}', '{OCRtxt}', '{n_page}', '{min_score}', '{avg_score}')".format(filename=filename,OCRtxt=OCRtxt,n_page=n_page,min_score=min_score,avg_score=avg_score))
    # cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
    # cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
    cursor.close()
    conn.commit()
    conn.close()

def get_df_from_sqlite_OCRtxt():
    db_file = os.path.join(os.path.dirname(__file__), 'txt_OCR.db')
    conn = sqlite3.connect(db_file)
    df_ocr = pd.read_sql_query("select * from TB_OCR;", conn)
    return df_ocr


# def get_score_in(low, high):
#     ' 返回指定分数区间的名字，按分数从低到高排序 '
#     pass
#
# # 测试:
# assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
# assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
# assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)
#
# print('Pass')

if __name__ == '__main__':
    print('ss')
    creat_tb()
    # insert_one_data_TB_OCR('002.pdf', '11', '0.99')
    # print(get_df_from_sqlite_OCRtxt())
