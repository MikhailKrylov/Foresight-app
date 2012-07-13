#-*- coding: utf8 -*-
import sqlite3 as sqlite
import os, sys
import string
import traceback
import string

class base:
    def __init__(self, type_str, name = "fs_db.db"):
        self.name = name
        self.type_str = type_str
    def create(self, key = 0):
        try:
            if key == 1:
                self.refresh_db()
            self.cursor.execute('CREATE TABLE trends (id INTEGER PRIMARY KEY, '+self.type_str+')')
        except:
            print u"Ошибка: Невозможно создать базу."
     
    def print_db(self):
        try:
            self.cursor.execute('SELECT * FROM trends ')
            strr = self.cursor.fetchall()  

            #print("\n".join(map(str, strr[0])))
            print "\n".join(map(lambda x: "\n" +"; ".join(map(str, x)), strr))
            #print(strr)
        except:
            traceback.print_exc()
            print "Ошибка: Не возможно вывести базу данных"
    def add_data(self, data_str):
        try:
            #self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources) VALUES(NULL, "qeddr", "rddt", "мама")')
            self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources, rsh, s_point, f_point) VALUES(NULL,'+data_str+')')
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