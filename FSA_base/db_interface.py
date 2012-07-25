#-*- coding: utf8 -*-
#подключение библиотек
import sqlite3 as sqlite
import os, sys
import string
import traceback

class base: #главный класс для работы с базой данных 
    def __init__(self, type_str, name = "fs_db2.db"):
        self.name = name
        self.type_str = type_str
    def create(self, key = 0): #создание новой БД
        try:
            if key == 1:
                self.refresh_db()
            #таблица трендов:
            self.cursor.execute('CREATE TABLE trends (id INTEGER PRIMARY KEY, '+self.type_str+')')
            #таблица отношений:
            self.cursor.execute('CREATE TABLE relationships (id INTEGER PRIMARY KEY, base_trend TEXT(100), second_trend TEXT(100), comment TEXT(300), type INTEGER(2))')
            #таблица настроек:
            self.cursor.execute('CREATE TABLE properties (id INTEGER PRIMARY KEY, base_trend TEXT(100), color TEXT(20), position INTEGER(5), type INTEGET(2)')
            self.cursor.close()
        except:
            traceback.print_exc()
            print u"Ошибка: Невозможно создать базу."
    def print_db(self): #Вывод ДБ на экран. Для тестирования.
        try:
            self.cursor.execute('SELECT * FROM trends ')
            trandlist = self.cursor.fetchall()  
            strret =  "\n".join(map(lambda x: "\n" +"; ".join(map(str, x)), trandlist))
            self.cursor.close()
            return trandlist
            #print(strr)
        except:
            traceback.print_exc()
            print "Ошибка: Не возможно вывести базу данных"
    def add_rsh(self, data_str):#добавление нового элемента в таблицу отношений
        try:
            self.cursor.execute('INSERT INTO relationships (id, base_trend, second_trend, comment, type) VALUES(NULL,'+data_str+')')
            self.connect.commit()
            self.cursor.close()
        except:
            traceback.print_exc()
            print u"Ошибка: Невозможно добавить данные в базу."
    def add_data(self, data_str): #Добавление нового элемента в таблицу трендов
        try:
            self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources, relationship, power, s_point, f_point) VALUES(NULL,'+data_str+')')
            self.connect.commit()
            self.cursor.close()
        except:
            traceback.print_exc()
            print u"Ошибка: Невозможно добавить данные в базу."
    def delete_db(self): #Удаление БД.
        try:
            self.connect.close()
            os.remove(self.name)
        except:
            print u"Ошибка: Невозможно удалить базу данных."
    def refresh_db(self): #Пересоздание БД.
        self.delete_db()
        self.connect_db()
    def connect_db(self): #Соединение с созданной БД.
        self.connect = sqlite.connect(self.name)
        self.cursor = self.connect.cursor()
    def verty_db(self):
        
        self.cursor = self.connect.cursor()
        self.cursor.execute('DELETE FROM trends WHERE length(trend_name)<1')
        self.cursor.execute('DELETE FROM trends WHERE s_point<2000')
        self.cursor.execute('DELETE FROM trends WHERE f_point<2000')
        self.cursor.close()
    def update_str(self, column, data, key_status, key = "trend_name", db = "trends"):
        self.cursor = self.connect.cursor()
        self.cursor.execute('UPDATE '+db+' SET '+column+ ' = "'+str(data)+'" WHERE '+str(key)+' = ' +str(key_status))
        self.cursor.close()
        