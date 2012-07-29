#-*- coding: utf8 -*-
"""
Created on 16.07.2012

@author: Werer
"""

#подключение библиотек
import sys, random, pango, time
#from curses.ascii import NUL
try:  
    import pygtk  
    pygtk.require('2.0')  
except:  
    pass  
try:  
    import gtk  
    import gtk.glade  
except:  
    print('GTK Not Availible')
    sys.exit(1)
import db_interface #подключение модуля работы с базой данных
from arrow_class import arrow #Подключение класса 'стрелки'
from Relationship_class import relationship
from new_trend_dialog import Trend_dialog


class Font_selection_window(object): #класс описывающий диалог выбора шрифта
    wTree = None
    def __init__(self, parent):
        self.parent = parent #ссылка на 'родителя'
        self.wTree = gtk.glade.XML( 'Font_Selection_interface2.glade' ) #подключение glade оболочки
        self.window = self.wTree.get_widget('FontWindow')
        self.cansel_btn = self.wTree.get_widget('cancel_btn')
        self.ok_btn = self.wTree.get_widget('ok_btn')
        self.fontseldlg = self.wTree.get_widget('fontselection1')
        self.fontseldlg.set_font_name(parent.font)
        def quit_(Emty_arg): #выход
            self.window.destroy()
        self.cansel_btn.connect_object('clicked', quit_, None) #обработка нажатия клавиши 'Закрыть'
        def OK_(Emty_arg): #Применить и выйти

            self.parent.font = self.window.get_font_name()
            for ar in self.parent.arrows:
                ar.font = self.parent.font
            self.parent.rendring()
            self.window.destroy()
        self.ok_btn.connect_object('clicked', OK_, None) #Обработка нажатия клавиши 'Ок'
        gtk.main()
        
##главный класс для работы с графическим интерфейсом    
class fsainterface(object):  #Главный класс работы с интерфейсом.
    wTree = None
    def __init__(self):
        self.wTree = gtk.glade.XML( 'main_interface.glade' ) #подключение glade оболочки
        self.area = self.wTree.get_widget('MainDrawingArea')
        self.window = self.wTree.get_widget('MainWindow')
        self.font = 'Sans 19'
        self.font_sel_btn = self.wTree.get_widget('font_select_btn')
        self.new_btn = self.wTree.get_widget('new_trend_btn')
        hruler1 = self.wTree.get_widget('hruler1')
        status_lbl = self.wTree.get_widget('status_lbl')
        self.load_btn = self.wTree.get_widget('normal_trend')
        self.upload_btn = self.wTree.get_widget('f_trend')
        vpaned2 = self.wTree.get_widget("vpaned2")
        self.rsh_on = self.wTree.get_widget('new_rsh_tbtn')
        self.trand_on = self.wTree.get_widget('new_trend_tbtn')
        self.exit_menu_btn = self.wTree.get_widget('exit_menu_tg')
        self.win_size = self.window.allocation
        self.rsh_points = ((0,False),(0, False))
        self.arrows = [] #все 'стрелки'
        self.rshps = [] #все связи между трендами
        self.db_name = "fs_db2.db" #Название подключаемой БД
        self.db_visual(0) #подключение БД к интерфейсу 
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            for arrow in self.arrows:
                if event.y in range(arrow.y-int(arrow.font.split(" ")[-1])-10, arrow.y+5):
                    if event.x in range(arrow.s_point, arrow.f_point):
                        arrow.mouse_motion_on()
                    else:
                        arrow.mouse_motion_off()
                else:
                    arrow.mouse_motion_off()
            status_lbl.set_text(str(ruler.get_range()[2])[:4])   
            return ruler.emit('motion_notify_event', event)
        self.area.connect_object('motion_notify_event', motion_notify, hruler1) 
        self.new_btn.connect_object('activate', self.new_trend_dialog_open, None) #обработка нажатия клавиши 'Создать'
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
         #   if not self.rsh_points[0][1]:
         #       print event
            for arrow in self.arrows:
                if arrow.get_mouse_motion:
                    if not self.rsh_on.get_active():
                        edit_dlg = Trend_dialog(self, arrow, True)
                  #  else:
                  #      drawable = self.area.window
                  #      gc = drawable.new_gc()
                  #      gc.foreground = self.area.window.get_colormap().alloc(0, 55535, 0)                 
                  #      drawable.draw_line(gc, int(x), 0, int(x), heigth) 
             #   if self.trand_on.get_active():
             #       drawable = self.area.window
             #       gc = drawable.new_gc()
             #       gc.foreground = self.area.window.get_colormap().alloc(0, 55535, 0)                 
             # #      drawable.draw_line(gc, int(x), 0, int(x), heigth) 
    
            #print  e1[2]-60,  new_rect.width
        def btn_switch(obj,scd =None):
            if obj == self.trand_on:
                if obj.get_active(): self.rsh_on.set_active(0)
            else:
                if obj.get_active(): self.trand_on.set_active(0)
                
        self.area.connect_object('button_press_event', mouseclick, None)
        self.load_btn.connect('clicked', self.db_load_to_arrows) 
        self.upload_btn.connect('clicked', self.db_update_from_arrows)  
        self.font_sel_btn.connect('activate', self.open_font_dialog)
        self.trand_on.connect('clicked',btn_switch)
        self.rsh_on.connect('clicked',btn_switch)
        self.exit_menu_btn.connect('activate', self.quit)
        gtk.main()
        
    def open_font_dialog(self, widget, Emty_arg):#вызов диалога выбора шрифта
        fsw = Font_selection_window(self) 

    def new_trend_dialog_open(self,Emty_arg): #Вызов диалога 'новый тренд'
        ntw = Trend_dialog(self)
    def quit(self, widget, ar1 = None): #выход (уничтожение окна)
        self.trend_base.cursor.close()
        self.trend_base.connect.close()
        self.window.destroy()
    def rendring(self):
        self.area.window.clear()
        hg = self.area.get_allocation().height
        n = len(self.arrows)
        y = 50
        k = hg/(n+1)
        self.render_v_lines()
        for ar in self.arrows:
            ar.rendring(y)
            y+=k
        for rsh in self.rshps:
            rsh.rendring()
    def render_v_lines(self):
        drawable = self.area.window
        color = self.area.window.get_colormap().alloc(55535, 55535, 65535)
        gc = drawable.new_gc()
        gc.foreground = color
        x = 0.
        k = float(self.area.get_allocation().width)/22.
        heigth = self.area.get_allocation().height
        while x < self.area.get_allocation().width:
              drawable.draw_line(gc, int(x), 0, int(x), heigth)
              x+=k
    def db_visual(self,rebuilding_key = 0): #обращение к интерфейсу базы данных
        type_string = 'trend_name UTF8(100), comment UTF8(300),  sources TEXT(300), power INTEGER(2), s_point INTEGER(32), f_point INTEGER(32)'
        self.trend_base = db_interface.base(type_string, self.db_name)
        #trend_base.delete_db()
   #     self.trend_base.create(rebuilding_key)
    def db_load_to_arrows(self, e1 = 0, e2 = None): #Загрузка данных из ДБ
        self.trend_base.connect_db()
        for ar in self.arrows:
            del ar
            self.arrows = list()
        trlist = self.trend_base.load()
        for trend in trlist:
            self.arrows.append(arrow(self.area, self.font, trend[1], trend[2],  trend[3], trend[4], trend[5], trend[6], trend[0]))
        #self.trend_base.cursor.close()
        self.load_relationship()
        self.rendring()
        #trend_base.refresh()
    #Добавляет строку в БД
    def db_add_data(self, data_string = 'Name, comment, sourses , power, start_year, year_of_end'):
        self.trend_base.add_data(data_string)
    def load_relationship(self):
        pass
        #self.rshps.append(relationship(self, self.arrows[0], self.arrows[1], u'Автобусные астоновки', u'вот такой вот комментарий'))
    #Обновляет БД исходя из массива объектов Arrows
    def db_update_from_arrows(self, e1 = None, e2 = None):
        #self.trend_base.connect_db()
        for arrow_ in self.arrows:
            name ="'"+ arrow_.name + "'"
            sourses ="'" + str(arrow_.sourses) + "'"
            s_year ="'" + str(arrow_.s_time) + "'"
            f_year ="'" + str(arrow_.f_time) + "'"
            power = "'" + str(arrow_.power) + "'"
            comment ="'" + str(arrow_.comment) + "'"
            sourses ="'" + str(arrow_.sourses) + "'"
            relationship ="'" + str(arrow_.relationship) + "'"
            b_str = name + u", " + comment + u", " + sourses + u"," + power + u"," + s_year+u"," + f_year
            f_trend = self.trend_base.search_string(name)
            if arrow_.to_delete:
                self.trend_base.delete_str(name)
            else:
                if len(f_trend) == 0:
                    self.db_add_data(b_str)
                else:
                   u_name = 'trend_name'
                   u_comment =  'comment'
                   u_sources =  'sources' 
                   u_power = 'power'
                   u_syear =  's_point' 
                   u_fyear =  'f_point'
                   self.trend_base.update_str(u_comment, comment, name)
                   self.trend_base.update_str(u_sources, sourses, name)
                   self.trend_base.update_str(u_power, power, name)
                   self.trend_base.update_str(u_syear, s_year, name)
                   self.trend_base.update_str(u_fyear, f_year, name)
                   self.trend_base.connect.commit()
            
aa = fsainterface()
