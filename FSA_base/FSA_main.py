#-*- coding: utf8 -*-

'''
Created on 12.07.2012

@author: werer
'''
#from pysqlite2 import dbapi2 as sqlite
import sqlite3 as sqlite
import os, sys
from encodings.utf_16 import encode
def main():
    trend_base = base()
    #trend_base.delete_db()
    trend_base.connect_db()
    trend_base.create(1)
    #trend_base.refresh()
    nm = u"'Основы инорматики'"
    cm = u"'Тест тест'"
    sa = u"'http://ya.ru'"
    trend_base.add_data(nm +u', '+ cm +u', '+ sa)
    #trend_base.print_db()
    #trend_base.add_data('"Основы инорматики", "Данный вид деятельности не способствует умственному развититию особей homo sapiens", "http://ya.ru"')
    trend_base.print_db()
    


class base:
    def __init__(self, name = "fs_db.db", type_str = "trend_name UTF8(100), comment UTF8(300), sources TEXT(300)"):
        self.name = name
        self.type_str = type_str
    def create(self, key = 0):
        try:
            if key == 1:
                self.refresh_db()
            self.cursor.execute('CREATE TABLE trends (id INTEGER PRIMARY KEY, '+self.type_str+')')
            #self.cursor.execute('PRAGMA encoding = "UTF-8"')
            #self.connect.commit('SET COLLATION_CONNECTION="utf8_general_ci"')
        except:
            print u"Ошибка: Невозможно создать базу."
    def print_db(self):
        try:
            self.cursor.execute('SELECT * FROM trends ')
            strr = self.cursor.fetchall()  
            print strr
        except:
            print "Ошибка: Не возможно вывести базу данных"
    def add_data(self, data_str):
        try:
           # self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources) VALUES(NULL, "qeddr", "rddt", "мама")')
            self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources) VALUES(NULL,'+data_str+')')
            self.connect.commit()
        except:
            print u"Ошибка: Невозможно добавить данные в базу."
    def delete_db(self):
        try:
            self.connect.close()
            os.remove(self.name)
        except:
            print u"Ошибка: Невозможно удалить базу данных."
    def refresh_db(self):
        self.delete_db()
        self.connect_db()
    def connect_db(self):
        self.connect = sqlite.connect(self.name)
        self.cursor = self.connect.cursor()

main()
    