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
#№главный класс для работы с графическим интерфейсом
class Trend_dialog(object): #класс описывающий диалог внесения в базу нового тренда или редактирования существующего
    wTree = None
    def __init__(self, parent, arrow_ = None, Fill = False):
        self.parent = parent
        self.Fill = Fill #активно ли замещение текущий строки.
        self.power = 1 #Итоговая сила тренда
        ##Подключение элементов формы
        self.Arrow = arrow_
        self.wTree = gtk.glade.XML('new_trend_window3.glade')
        self.window = self.wTree.get_widget('new_trend_dialog')
        self.cansel_btn = self.wTree.get_widget('Cansel_btn')
        self.ok_btn = self.wTree.get_widget('Ok_btn')
        self.sp_rbtn = self.wTree.get_widget('Spower_radio_btn')
        self.up_rbtn = self.wTree.get_widget('Upower_radio_btn')
        self.mp_rbtn = self.wTree.get_widget('Mpower_radio_btn')
        self.fs_chk = self.wTree.get_widget('forse_chk')
        self.fs_chk2 = self.wTree.get_widget('forse_chk1')
        self.palitra = self.wTree.get_widget('palitra_1')
        self.s_year_text = self.wTree.get_widget('s_year_text')
        self.f_year_text = self.wTree.get_widget('f_year_text')
        self.years_scale = self.wTree.get_widget('years_scale')
        self.doc_text = self.wTree.get_widget('doc_text')
        self.srs_text = self.wTree.get_widget('srs_text')
        self.name_str = self.wTree.get_widget('name_str')
        color_sel_chbutn = self.wTree.get_widget('color_selection_on')
        self.f_year_text.set_text('2012')
        self.s_year_text.set_text('2000')
        random_color = self.parent.area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.palitra.set_current_color(random_color)
        self.last_entry = self.s_year_text

        def hide_show(obj, active):
            if active():    self.palitra.show()
            else:   self.palitra.hide()
                
        # print event
        color_sel_chbutn.connect('toggled', hide_show, color_sel_chbutn.get_active)
        
        def scale_show(obj_, event):
            if obj_ == self.s_year_text:
                self.last_entry = self.s_year_text #Последнее выбранное поле текста
                if int(self.s_year_text.get_text())<= int(self.f_year_text.get_text()):
                    self.years_scale.set_value(int(self.s_year_text.get_text()))
                else:
                    self.years_scale.set_value(int(self.f_year_text.get_text())-1)
                    self.f_year_text.set_text(str(int(self.f_year_text.get_text())-1))
            elif obj_ == self.f_year_text:
                self.last_entry = self.f_year_text
                if int(self.f_year_text.get_text())>= int(self.s_year_text.get_text())+1:
                    self.years_scale.set_value(int(self.f_year_text.get_text()))
                else:
                    self.years_scale.set_value(int(self.s_year_text.get_text())+1)
                    self.f_year_text.set_text(str(int(self.s_year_text.get_text())+1))
        def scale_hide(obj_, event):
            self.years_scale.hide()
        def set_data(obj_, t_ = None, m_ = None):        
            if self.last_entry == self.f_year_text:
                if int(self.f_year_text.get_text())>= int(self.s_year_text.get_text())+1:
                    self.last_entry.set_text(str(self.years_scale.get_value())[:4])
                else:
                    self.last_entry.set_text(str(int(self.s_year_text.get_text())+1))
                    self.years_scale.set_value(int(self.s_year_text.get_text())+1)
            else:
                if int(self.s_year_text.get_text())<= int(self.f_year_text.get_text()):
                    self.last_entry.set_text(str(self.years_scale.get_value())[:4])
                else:
                    self.last_entry.set_text(str(int(self.f_year_text.get_text())-1))
                    self.years_scale.set_value(int(self.f_year_text.get_text())-1)
        self.s_year_text.connect('focus-in-event', scale_show)
        self.f_year_text.connect('focus-in-event', scale_show)
        self.years_scale.connect_object('value_changed', set_data, self.last_entry)
        def set_pwr(widget_ ,E_arg):
            if E_arg == 0 and widget_.get_active(): #Возрастающая
                act = int(self.fs_chk2.get_active())
                self.fs_chk.show()
                self.fs_chk.set_sensitive(1)
                self.fs_chk.set_active(act)
                self.fs_chk2.set_sensitive(0)
                self.fs_chk2.hide()
                self.power = 1
            elif E_arg == 1: #Неопределенная
                self.fs_chk.hide()
                self.fs_chk2.hide()
                self.power = 0
            elif E_arg == 2 and widget_.get_active(): #убывающая
                act = int(self.fs_chk.get_active())
                self.fs_chk2.show()
                self.fs_chk2.set_sensitive(1)
                self.fs_chk2.set_active(act)
                self.fs_chk.set_sensitive(0)
                self.fs_chk.hide()
                self.power = -1     
        self.sp_rbtn.connect('toggled', set_pwr, 0)
        self.up_rbtn.connect('toggled', set_pwr, 1)
        self.mp_rbtn.connect('toggled', set_pwr, 2)
        self.ok_btn.connect('clicked', self.ok_click) #обработка нажатия клавиши 'Ок'
        self.cansel_btn.connect('clicked', self.quit_) #обработка нажатия клавиши 'Закрыть'
        if Fill:
            self.to_fill()
            self.years_scale.set_value(int(self.s_year_text.get_text())) #первичная инициализация значения ползунка.
        gtk.main()
    def to_fill(self):
        trend = self.Arrow
        if trend.power>0:
            if trend.power == 2:
                self.fs_chk.set_active(1)
            self.sp_rbtn.set_active(1)
        elif trend.power<0:
            if trend.power == -2:
                self.fs_chk2.set_active(1)
            self.mp_rbtn.set_active(1)
        else:
            self.up_rbtn.set_active(1)
        self.name_str.set_text(trend.name)
        self.name_str.set_sensitive(0)
        comment_buffer = gtk.TextBuffer(None)
        comment_buffer.set_text(trend.comment)
        self.doc_text.set_buffer(comment_buffer)
        sourses_buffer = gtk.TextBuffer(None)
        sourses_buffer.set_text(trend.sourses)
        self.srs_text.set_buffer(sourses_buffer)
        self.s_year_text.set_text(str(trend.s_time))
        self.f_year_text.set_text(str(trend.f_time))
        self.palitra.set_current_color(trend.color)
    def quit_(self, Ea = None, Ba = None):
        self.window.destroy()
    def ok_click(self, e_arg):
        plagiat = False # проверка на наличие тренда с таким названием
        name = self.name_str.get_text()
        if not self.Fill:
            for ar in self.parent.arrows:
                if ar.name == name:
                    plagiat = True
                    print 'Тенденция с таким названием уже существует'
                    print 'Возможные варианты названия:'
                    print name+" продолжение, ", name+" 1, ", name +" "+ str(self.f_year_text.get_text())
                    break
        if not plagiat:
            if len(name)<3:
                print 'Ошибка! Введите название!'
            else:
                comment_b = self.doc_text.get_buffer()
                comment =str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))
                sourses_b = self.srs_text.get_buffer()
                sourses =str(sourses_b.get_text(sourses_b.get_start_iter(), sourses_b.get_end_iter()))
                if self.fs_chk.get_active() or self.fs_chk2.get_active():
                    self.power*=2
                relationship = u'"[2,4], [3,-2]"'
                try:
                    int(self.s_year_text.get_text())
                    int(self.f_year_text.get_text())
                except:
                    print 'Ошибка: введите корректные даты!'
                    return 0
                if  int(self.s_year_text.get_text()) < int(self.f_year_text.get_text()) and int(self.s_year_text.get_text()) in range(2000,2055) and int(self.f_year_text.get_text()) in range(2000,2055): 
                    s_year =str(self.s_year_text.get_text())
                    f_year =str(self.f_year_text.get_text())
                    power = str(self.power)
                    color = self.palitra.get_current_color()
                    if self.Fill:
                        self.arrow_from_data(comment, sourses, f_year, s_year, relationship, color)
                    else:
                        self.Arrow = arrow(self.parent.area, self.parent.font, name, comment, sourses, relationship, power, s_year, f_year)
                        self.parent.arrows.append(self.Arrow)
                    self.parent.rendring()
                    self.quit_()
                else:
                    print 'Ошибка: введите корректные даты!'
    def arrow_from_data(self, comment, sourses, f_year, s_year, relationship, color):                        
        self.Arrow.comment = comment
        self.Arrow.sourses = sourses
        self.Arrow.f_time = int(f_year)
        self.Arrow.s_time = int(s_year)
        self.Arrow.relationship = relationship
        self.Arrow.color = self.parent.area.window.get_colormap().alloc(color)

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

            self.window.destroy()
        self.ok_btn.connect_object('clicked', OK_, None) #Обработка нажатия клавиши 'Ок'
        gtk.main()
        
    
class fsainterface(object):
    wTree = None
    def __init__(self):
       
        self.wTree = gtk.glade.XML( 'main_interface.glade' ) #подключение glade оболочки
        self.area = self.wTree.get_widget('MainDrawingArea')
        self.font = 'Sans 19'
        self.font_sel_btn = self.wTree.get_widget('font_select_btn')
        self.new_btn = self.wTree.get_widget('new_trend_btn')
        hruler1 = self.wTree.get_widget('hruler1')
        status_lbl = self.wTree.get_widget('status_lbl')
        self.load_btn = self.wTree.get_widget('normal_trend')
        self.upload_btn = self.wTree.get_widget('f_trend')
        self.arrows = [] #все 'стрелки'
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
            for arrow in self.arrows:
                if arrow.get_mouse_motion:
                    edit_dlg = Trend_dialog(self, arrow, True)
                    break

        self.area.connect_object('button_press_event', mouseclick, None)
        self.load_btn.connect('clicked', self.db_load_to_arrows) 
        self.upload_btn.connect('clicked', self.db_update_from_arrows)  
        self.font_sel_btn.connect('button_press_event', self.open_font_dialog)
        gtk.main()
    def open_font_dialog(self, widget, Emty_arg):#вызов диалога выбора шрифта
        fsw = Font_selection_window(self) 
    def new_trend_dialog_open(self,Emty_arg): #Вызов диалога 'новый тренд'
        ntw = Trend_dialog(self)
    def quit(self, widget): #выход (уничтожение окна)
        self.wTree.get_widget('MainWindow').destroy()
    def rendring(self):
        self.area.window.clear()
        hg = self.area.allocation.height
        n = len(self.arrows)
        y = 50
        k = hg/(n+1)
        self.render_v_lines()
        for ar in self.arrows:
            ar.rendring(y)
            y+=k
    def render_v_lines(self):
        drawable = self.area.window
        color = self.area.window.get_colormap().alloc(55535, 55535, 65535)
        gc = drawable.new_gc()
        gc.foreground = color
        x = 0.
        k = float(self.area.allocation.width)/22.
        heigth = self.area.allocation.height
        while x < self.area.allocation.width:
              drawable.draw_line(gc, int(x), 0, int(x), heigth)
              x+=k
            
    def db_visual(self,rebuilding_key = 0): #обращение к интерфейсу базы данных
        type_string = 'trend_name UTF8(100), comment UTF8(300),  sources TEXT(300), relationship TEXT(300), power INTEGER(2), s_point INTEGER(32), f_point INTEGER(32)'
        self.trend_base = db_interface.base(type_string)
        #trend_base.delete_db()
        self.trend_base.connect_db()
   #     self.trend_base.create(rebuilding_key)
    def db_load_to_arrows(self, e1 = None, e2 = None):
        trlist = self.trend_base.print_db()
        for trend in trlist:
            self.arrows.append(arrow(self.area, self.font, trend[1], trend[2], trend[3], trend[4], trend[5], trend[6], trend[7]))
        self.trend_base.cursor.close()
        self.rendring()
        #trend_base.refresh()
    def db_add_data(self, data_string = 'Name, comment, sourses, relationship, power, start_year, year_of_end'):
        self.trend_base.add_data(data_string)
    def db_update_from_arrows(self, e1 = None, e2 = None):
        self.trend_base.connect_db()
        for arrow_ in self.arrows:
            name ="'"+ arrow_.name + "'"
            sourses ="'" + str(arrow_.sourses) + "'"
            relationship = "'" + arrow_.relationship + "'"
            s_year ="'" + str(arrow_.s_time) + "'"
            f_year ="'" + str(arrow_.f_time) + "'"
            power = "'" + str(arrow_.power) + "'"
            comment ="'" + str(arrow_.comment) + "'"
            sourses ="'" + str(arrow_.sourses) + "'"
            relationship ="'" + str(arrow_.relationship) + "'"
            b_str = name + u", " + comment + u", " + sourses + u"," + relationship+u"," + power + u"," + s_year+u"," + f_year
            f_trend = self.trend_base.search_string(name)
            print 'found:', f_trend
            if len(f_trend) == 0:
                self.db_add_data(b_str)
            else:
               u_name = 'trend_name'
               u_comment =  'comment'
               u_sources =  'sources' 
               u_rsh = 'relationship'
               u_power = 'power'
               u_syear =  's_point' 
               u_fyear =  'f_point'
               self.trend_base.update_str(u_comment, comment, name)
               self.trend_base.update_str(u_sources, sourses, name)
               self.trend_base.update_str(u_rsh, relationship, name)
               self.trend_base.update_str(u_power, power, name)
               self.trend_base.update_str(u_syear, s_year, name)
               self.trend_base.update_str(u_fyear, f_year, name)
            
aa = fsainterface()
