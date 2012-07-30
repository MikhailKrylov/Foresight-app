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
from Relationship_class import relationship #Класс "связи"
from new_trend_dialog import Trend_dialog 
from Rsh_interface import edit_rsh_dialog
from File_dialog import fildeialog

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
        self.font = 'Sans 16'
        self.wTree = gtk.glade.XML( 'main_interface.glade' ) #подключение glade оболочки
        self.area = self.wTree.get_widget('MainDrawingArea')
        self.window = self.wTree.get_widget('MainWindow')
        self.font_sel_btn = self.wTree.get_widget('font_select_btn')
        self.open_db_btn = self.wTree.get_widget('file_open_btn')
        hruler1 = self.wTree.get_widget('hruler1')
        status_lbl = self.wTree.get_widget('status_lbl')
        self.upload_btn = self.wTree.get_widget('file_save_btn')
        vpaned2 = self.wTree.get_widget("vpaned2")
        self.rsh_on = self.wTree.get_widget('new_rsh_tbtn')
        self.new_db_btn = self.wTree.get_widget('new_trend_btn')
        self.trand_on = self.wTree.get_widget('new_trend_tbtn')
        self.exit_menu_btn = self.wTree.get_widget('exit_menu_tg')
        self.new_btn = self.wTree.get_widget('new_e_btn')
        self.win_size = self.window.allocation
        self.rsh_points = ((0,False),(0, False))
        self.arrows = [] #все 'стрелки'
        self.rshps = [] #все связи между трендами
        self.db_name = "" #Название подключаемой БД
        if len(self.db_name)>5:
            self.db_visual(0) #подключение БД к интерфейсу 
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            if not self.rsh_on.get_active():
                for arrow in self.arrows:
                    if event.y in range(arrow.y-int(arrow.font.split(" ")[-1])-10, arrow.y+5):
                        if event.x in range(arrow.s_point, arrow.f_point):
                            arrow.mouse_motion_on()
                        else:
                            arrow.mouse_motion_off()
                    else:
                        arrow.mouse_motion_off()
            else:
                for rsh in self.rshps:
                    x1,y1 = float(rsh.coord[0]), float(rsh.coord[1])
                    x2,y2 = float(rsh.coord[2]), float(rsh.coord[3])
                    if x2-x1 and y2-y1:
                        d = abs(event.x/(x2-x1) - event.y/(y2-y1)+y1/(y2-y1)-x1/(x2-x1))/((1/(x2-x1)**2+ 1/(y2-y1)**2)**(1./2.))
                    if d < 2:
                        rsh.mouse_motion_on()
                    else:
                        rsh.mouse_motion_off()
            status_lbl.set_text(str(ruler.get_range()[2])[:4])   
            return ruler.emit('motion_notify_event', event)
        self.area.connect_object('motion_notify_event', motion_notify, hruler1) 
        self.open_db_btn.connect('activate', self.new_db_dialog) #обработка нажатия клавиши 'Создать'
        self.new_db_btn.connect('activate', self.new_db_dialog)
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
            if not self.rsh_on.get_active():
                for arrow in self.arrows:
                    if arrow.get_mouse_motion:
                            edit_dlg = Trend_dialog(self, arrow, True)
            else:
                for rsh in self.rshps:
                    if rsh.get_mouse_motion:
                            edit_dlg = edit_rsh_dialog(self, rsh)            
    
            #print  e1[2]-60,  new_rect.width
    
        def btn_switch(obj,scd =None):
            if obj == self.trand_on:
                if obj.get_active(): self.rsh_on.set_active(0)
            else:
                if obj.get_active(): self.trand_on.set_active(0)
                
        self.area.connect_object('button_press_event', mouseclick, None)
        self.upload_btn.connect('activate', self.db_update_from_arrows)  
        self.font_sel_btn.connect('activate', self.open_font_dialog)
        self.trand_on.connect('clicked',btn_switch)
        self.rsh_on.connect('clicked',btn_switch)
        self.exit_menu_btn.connect('activate', self.quit)
        
        self.new_btn.connect('clicked', self.new_trend_dialog_open)
        gtk.main()
    def new_db_dialog(self, obj = None, e2 = 0):
        if obj == self.new_db_btn:
            dialog = fildeialog(self, True)
        else:
            dialog = fildeialog(self)
            
    def open_font_dialog(self, widget = None, Emty_arg = None):#вызов диалога выбора шрифта
        fsw = Font_selection_window(self) 

    def new_trend_dialog_open(self,Emty_arg = None): #Вызов диалога 'новый тренд'
        if self.trand_on.get_active():
            ntw = Trend_dialog(self)
        else:
            aa = edit_rsh_dialog(self, None, False)
    def quit(self, widget, ar1 = None): #выход (уничтожение окна)
        self.trend_base.cursor.close()
        self.trend_base.connect.close()
        self.window.destroy()
    def rendring(self):
        self.area.window.clear()
        hg = self.area.get_allocation().height
        
        cont_list = list()
        for rsh in self.rshps:
            if rsh.type == 0:
                cont_list.append(rsh)
        n = len(self.arrows)#-len(cont_list)
        y = 20
        dy = 25
        k = hg/(n+2)
        self.render_v_lines()
        for ar in self.arrows:
            ar.y = y
            y +=k
        for rs in cont_list:
            if rs.trend1 == ar:
                if rs.trend1.y<rs.trend2.y:
                    dy = rs.trend1.y
                    rs.trend2.y = dy
                else:
                    dy = rs.trend2.y
                    rs.trend1.y = dy
                rs.trend1.rendring(dy)
                rs.trend2.rendring(dy)
                rs.trend1.render = True
                rs.trend2.render = True
        for ar in self.arrows:
            if not ar.render:
                ar.rendring(y)
        for ar in self.arrows:
            ar.render = False
        for rsh in self.rshps:
            if not rsh.to_delete:
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
        self.trend_base = db_interface.base(type_string, self.db_name, rebuilding_key)
        #trend_base.delete_db()
   #     self.trend_base.create(rebuilding_key)
    def db_load_to_arrows(self, e1 = 0, e2 = None): #Загрузка данных из ДБ
        self.trend_base.connect_db()
        for ar in self.arrows:
            del ar
            self.arrows = list()
        trlist = self.trend_base.load()
        for trend in trlist:
            self.arrows.append(arrow(self, trend[1], trend[2],  trend[3], trend[4], trend[5], trend[6], trend[0]))
        #self.trend_base.cursor.close()
        self.load_relationship()
        self.rendring()
        #trend_base.refresh()
    #Добавляет строку в БД
    def db_add_data(self, data_string = 'Name, comment, sourses , power, start_year, year_of_end'):
        self.trend_base.add_data(data_string)
    def db_load_from_rshps(self):
        for rsh in self.rshps:
            trend1_name ="'" + rsh.trend1.name + "'"
            trend2_name ="'" + rsh.trend2.name + "'"
            type = str(int(rsh.type))
            if not rsh.to_delete:
                comment ="'"+ rsh.comment + "'"
                fnd = self.trend_base.rsh_verty(trend1_name, trend2_name, type)
                if not fnd:
                    self.trend_base.add_rsh(trend1_name, trend2_name, comment, type)
                else:
                    trend1_name, trend2_name = fnd
                    self.trend_base.upd_rsh(trend1_name, trend2_name, comment, type)
            else:
                fnd = self.trend_base.rsh_verty(trend1_name, trend2_name, type)
                trend1_name, trend2_name = fnd
                self.trend_base.del_rsh(trend1_name, trend2_name, type)    
    def search_arrow(self, name):
        for ar in self.arrows:
            if ar.name == name:
                return ar                
    def load_relationship(self):
        self.trend_base.connect_db()
        for rsh in self.rshps:
            del rsh
            self.rshps = list()
        rshlist = self.trend_base.load_rsh()
        for rshl in rshlist:
            first_trend = self.search_arrow(rshl[1])
            second_trend = self.search_arrow(rshl[2])
            self.rshps.append(relationship(self, first_trend, second_trend, rshl[4], rshl[3]))
        #self.trend_base.cursor.close()
        self.rendring()
        #self.rshps.append(relationship(self, self.arrows[0], self.arrows[1], u'Автобусные астоновки', u'вот такой вот комментарий'))
    #Обновляет БД исходя из массива объектов Arrows
    def db_update_from_arrows(self, e1 = None, e2 = None):
        #self.trend_base.connect_db()
        self.db_load_from_rshps()
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
