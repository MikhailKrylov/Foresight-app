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
            #таблица отношений:
            self.cursor.execute('CREATE TABLE relationships (id INTEGER PRIMARY KEY,  base_trend TEXT(100), second_trend TEXT(100), comment TEXT(300), type INTEGER(2))')
            #таблица настроек:
            self.cursor.execute('CREATE TABLE properties (id INTEGER PRIMARY KEY, base_trend TEXT(100), color TEXT(20), position INTEGER(5), type INTEGET(2)')
            #таблица трендов:
            self.cursor.execute('CREATE TABLE trends (id INTEGER PRIMARY KEY, '+self.type_str+')')
          
            
        except:
            traceback.print_exc()
            print u"Ошибка: Невозможно создать базу."
    def load(self): #Вывод ДБ на экран. Для тестирования.
       # self.connect_db()
        try:
            self.cursor.execute('SELECT * FROM trends ')
            trandlist = self.cursor.fetchall()  
            strret =  "\n".join(map(lambda x: "\n" +"; ".join(map(str, x)), trandlist))
            
            return trandlist
            #print(strr)
        except:
            traceback.print_exc()
            print "Ошибка: Не возможно вывести базу данных"
        #self.cursor.close()
    def add_rsh(self, trend1, trend2, comment, type):#добавление нового элемента в таблицу отношений
        data_str  = trend1 + u', '+ trend2+ u', ' + comment+u', '+ type
        try:
            self.cursor.execute('INSERT INTO relationships (id, base_trend, second_trend, comment, type) VALUES(NULL,'+data_str+')')
            self.connect.commit()
            
        except:
            traceback.print_exc()
            print u"Ошибка: Невозможно добавить данные в базу."
    def load_rsh(self):
        pass
    def upd_rsh(self, trend1,trend2,comment,type):
        self.cursor.execute('UPDATE relationships SET type = '+type+ ' WHERE base_trend LIKE '+trend1+ 'AND second_trend LIKE '+trend2)
        self.cursor.execute('UPDATE relationships SET comment = '+comment+ ' WHERE base_trend LIKE '+trend1+ 'AND second_trend LIKE '+trend2)
    def add_data(self, data_str): #Добавление нового элемента в таблицу трендов
        try:
            self.cursor.execute('INSERT INTO trends (id, trend_name, comment, sources, power, s_point, f_point) VALUES(NULL,'+data_str+')')
            self.connect.commit()
            
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
    def rsh_verty(self, trend1_name, trend2_name, type):
        self.cursor.execute('SELECT * FROM relationships WHERE base_trend LIKE '+trend1_name +' AND second_trend LIKE '+trend2_name+ 'AND type LIKE '+ type)
        v1 = self.cursor.fetchall()
        self.cursor.execute('SELECT * FROM relationships WHERE base_trend LIKE '+trend2_name +' AND second_trend LIKE '+trend1_name+ 'AND type LIKE '+ type)
        v2 = self.cursor.fetchall()
        if len(v1):
            return (trend1_name,  trend2_name)
        if len(v2):
            return (trend2_name, trend1_name)
        return False
    
    def search_string(self, key_value, key = "trend_name", table = "trends" ):
       # self.cursor = self.connect.cursor()
        self.cursor.execute('SELECT * FROM ' +table+ ' WHERE '+key+' LIKE '+key_value)
        found_trend = self.cursor.fetchall() 
        return found_trend
       # self.cursor.close()
    def verty_db(self):
        #self.cursor = self.connect.cursor()
        self.cursor.execute('DELETE FROM trends WHERE length(trend_name)<1')
        self.cursor.execute('DELETE FROM trends WHERE s_point<2000')
        self.cursor.execute('DELETE FROM trends WHERE f_point<2000')
        
    def update_str(self, column, data, key_status, key = "trend_name", table = "trends"):
        #self.cursor = self.connect.cursor()
        ex_str = 'UPDATE '+table+' SET '+column+ ' = '+data+' WHERE '+str(key)+' LIKE ' +str(key_status)
        self.cursor.execute(ex_str)
        #self.cursor.close()
    def delete_str(self, key_value, key = 'trend_name', table = 'trends'): 
        self.cursor.execute('DELETE FROM '+table +' WHERE '+ key + ' LIKE '+key_value)
        self.connect.commit()