#-*- coding: utf8 -*-

'''
Created on 12.07.2012

@author: werer
'''
#from pysqlite2 import dbapi2 as sqlite
#подключение библиотек
import string
import thread
import db_interface #подключение модуля работы с базой данных
import FSA_interface #подключение графического интерфейса
from FSA_interface import fsainterface
def main():
    interface = fsainterface()
    type_string = "trend_name UTF8(100), comment UTF8(300),  sources TEXT(300), rsh TEXT(300), s_point INTEGER(32), f_point INTEGER(32)"
    trend_base = db_interface.base(type_string)
    #trend_base.delete_db()
    trend_base.connect_db()
    trend_base.create(1)
    #trend_base.refresh()
    nm = u"'Основы инорматики'"
    cm = u"'Тест тест'"
    sa = u"'http://ya.ru'"
    sv = u"'[2,4], [3,-2]'"
    s_p = u"30000"
    f_p = u"45555"
    interface.draw_text((200,300,0,0), "Text")
    trend_base.add_data(nm +u', '+ cm +u', '+ sa+',' + sv+u',' + s_p+u',' + f_p)
    trend_base.print_db()
    



main()
    