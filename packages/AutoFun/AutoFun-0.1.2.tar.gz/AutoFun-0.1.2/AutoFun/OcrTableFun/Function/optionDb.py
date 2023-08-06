import sqlite3
import os
import traceback


def creatOptionDb():
    if not os.path.isfile('./database//userOption.db'):
        if not os.path.exists('./database'):
            os.mkdir('./database')
        db_file = os.path.join('./database', 'userOption.db')
        if not os.path.isfile('./database/userOption.db'):
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                # cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
                try:
                    cursor.execute('create table Useroption(name varchar(255) ,value1 varchar(260),value2 varchar(260),value3 varchar(260),value4 varchar(260),value5 varchar(260),value6 varchar(260),value7 varchar(260))')
                    conn.commit()
                    cursor.close()
                    conn.close()
                    defaultData()
                    return False
                except Exception as e:
                    traceback.print_exc()
                    conn.rollback()
                    cursor.close()
                    conn.close()
                    return e

        else:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            try:
                cursor.execute('CREATE TABLE IF NOT EXISTS Useroption(name varchar(255) ,value1 varchar(260),value2 varchar(260),value3 varchar(260),value4 varchar(260),'
                    'value5 varchar(260),value6 varchar(260),value7 varchar(260))')
                # cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
                # cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
                conn.commit()
                cursor.close()
                conn.close()
                result = defaultData()
                #没有出错则返回FALSE
                return False
            except Exception as e:
                conn.rollback()
                cursor.close()
                conn.close()
                #报错返回E
                return e

#初始化数据库
def defaultData():
    db_file = os.path.join('./database', 'userOption.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
    name_list = ["checkIndex", 'makeDir', 'getGe', 'OCR', 'JsonSql', 'SqlExcel', 'move', 'checkFile', 'splitName', 'WordPdf','splitPdf',"Useroption","Onload","Tablepath"]
    try:
        for i in name_list:
            sql = 'INSERT INTO Useroption (name) values ("{}"); '.format(i)
            print(sql)
            cursor.execute(sql)
            conn.commit()

    except Exception as e:
        conn.rollback()
    cursor.close()
    conn.close()

def getOption(name):
    #判断路径是否存在
    if not os.path.isfile('./database//userOption.db'):
        return "保存dataOption路径不存在"
    else:
        db_file = os.path.join('./database', 'userOption.db')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            sql = "select * from Useroption where name = '{}'".format(name)
            cursor.execute(sql)
            g = cursor.fetchall()
            cursor.close()
            conn.close()
            return g
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            # 报错返回E
            return e

def InsertDb(Oldist):
    name_tuple = ("name", "value1", "value2", "value3", "value4", "value5", "value6", "value7")
    if not os.path.isfile('./database//userOption.db'):
        creatOptionDb()
    checkOrAdd(Oldist[0])
    db_file = os.path.join('./database', 'userOption.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    name = ""
    for i in range(1, len(Oldist)):
        if not i == len(Oldist)-1:
            name = name+ name_tuple[i] + "='" + Oldist[i] + "', "
        else:
            name = name + name_tuple[i] + "='" + Oldist[i] +"'"
    condition = name_tuple[0] +" ='"+ Oldist[0] + "'"
    sql = 'Update Useroption  SET {name} WHERE {condition}'.format(name = name, condition = condition)
    # sql = "Update Useroption  SET value1=' 1', value2='2', value3='3', value4='4'  WHERE name ='checkIndex'"
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return False

    except Exception as e:
        traceback.print_exc()
        conn.rollback()
        cursor.close()
        conn.close()
        return e

def checkOrAdd(name):
    db_file = os.path.join('./database', 'userOption.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    sql = "select * from Useroption where name = '{}'".format(name)
    cursor.execute(sql)
    g = cursor.fetchall()
    if not len(g):
        try:
            sql = 'INSERT INTO Useroption (name) values ("{}"); '.format(name)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return False
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            cursor.close()
            conn.close()
            return e

if __name__ == "__main__":
    # z = ("checkIndex", " 1","2", "3", "4")
    # InsertDb(z)
    # defaultData()
    checkOrAdd('splitPdf1')