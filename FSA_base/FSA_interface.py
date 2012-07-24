#-*- coding: utf8 -*-
'''
Created on 16.07.2012

@author: Werer
'''

#подключение библиотек
import sys, random, pango, time
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
try:  
    import gtk  
    import gtk.glade  
except:  
    print("GTK Not Availible")
    sys.exit(1)
import db_interface #подключение модуля работы с базой данных
from arrow_class import arrow #Подключение класса "стрелки"
#главный класс для работы с графическим интерфейсом
class New_trend_dialog(object): #класс описывающий диалог внесения в базу нового тренда или редактирования существующего
    wTree = None
    def __init__(self, parent):
        self.parent = parent
        self.power = 1 #Итоговая сила тренда
        ##Подключение элементов формы
        self.wTree = gtk.glade.XML("new_trend_window3.glade")
        self.window = self.wTree.get_widget("new_trend_dialog")
        self.cansel_btn = self.wTree.get_widget("Cansel_btn")
        self.ok_btn = self.wTree.get_widget("Ok_btn")
        self.sp_rbtn = self.wTree.get_widget("Spower_radio_btn")
        self.up_rbtn = self.wTree.get_widget("Upower_radio_btn")
        self.mp_rbtn = self.wTree.get_widget("Mpower_radio_btn")
        self.fs_chk = self.wTree.get_widget("forse_chk")
        self.palitra = self.wTree.get_widget("palitra_1")
        self.s_year_text = self.wTree.get_widget("s_year_text")
        self.f_year_text = self.wTree.get_widget("f_year_text")
        self.years_scale = self.wTree.get_widget("years_scale")
        random_color = self.parent.area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.palitra.set_current_color(random_color)
        adj =  gtk.Adjustment(2000, 2000, 2055, 0, 0, 0)
        self.last_entry = self.s_year_text
        def scale_show(obj_, event):
            if obj_ == self.s_year_text:
                self.last_entry = self.s_year_text #Последнее выбранное поле текста
            elif obj_ == self.f_year_text:
                self.last_entry = self.f_year_text
        def scale_hide(obj_, event):
            self.years_scale.hide()
        def set_data(obj_):                   
            self.last_entry.set_text(str(self.years_scale.get_value())[:4])
        self.s_year_text.connect("focus-in-event",scale_show)
        self.f_year_text.connect("focus-in-event",scale_show)
        self.years_scale.connect("focus-in-event", scale_show)
        self.years_scale.connect_object("value_changed", set_data, self.last_entry)
        
        def set_pwr(widget_ ,E_arg):
            if E_arg == 0:
                self.fs_chk.show()
                self.power = 1
                #rect = gtk.gdk.Get_rectangle(self.fs_chk)
                #print self.fs_chk.get_allocation()
                #rect = self.fs_chk.Rectangle(361,61,100,30)
                #self.fs_chk.move_resize(rect)
                #self.fs_chk.set_position(190, 12)
            elif E_arg == 1:
                self.fs_chk.hide()
                self.power = 0
            elif E_arg == 2:
                self.fs_chk.show()
                self.power = -1
               # rect = gtk.gdk.get_rectangle(self.fs_chk)
               # self.fs_chk.move_resize(rect)
                #self.fs_chk.set_alignment(220,12)
        self.sp_rbtn.connect("toggled", set_pwr, 0)        
        self.sp_rbtn.connect("toggled", set_pwr, 0)
        self.up_rbtn.connect("toggled", set_pwr, 1)
        self.mp_rbtn.connect("toggled", set_pwr, 2)
        def quit_(Emty_arg): #выход
            self.window.destroy()
        self.ok_btn.connect("clicked", self.ok_click) #обработка нажатия клавиши "Закрыть"
        self.cansel_btn.connect("clicked", quit_) #обработка нажатия клавиши "ок"
        gtk.main()
    def quit_(self):
        self.window.destroy()
    def ok_click(self, e_arg):
        name ="'"+ self.wTree.get_widget("name_str").get_text()+"'"
        comment_b = self.wTree.get_widget("doc_text").get_buffer()
        comment ="'"+ str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))+"'"
        sourses_b = self.wTree.get_widget("srs_text").get_buffer()
        sourses ="'"+ str(sourses_b.get_text(sourses_b.get_start_iter(), sourses_b.get_end_iter()))+"'"
        if self.fs_chk.get_active():
            self.power*=2
        relationship = u"'[2,4], [3,-2]'"
        s_year ="'"+ str(self.s_year_text.get_text()) + "'"
        f_year ="'"+ str(self.f_year_text.get_text()) + "'"
        power = "'"+str(self.power)+"'"
        b_str = name +u', '+ comment +u', '+ sourses+u',' + relationship+u','+power+u',' + s_year+u',' + f_year
        self.parent.db_add_data(b_str)
        self.quit_()
    
class Font_selection_window(object): #класс описывающий диалог выбора шрифта
    wTree = None
    def __init__(self, parent):
        self.parent = parent #ссылка на "родителя"
        self.wTree = gtk.glade.XML( "Font_Selection_interface2.glade" ) #подключение glade оболочки
        self.window = self.wTree.get_widget("FontWindow")
        self.cansel_btn = self.wTree.get_widget("cancel_btn")
        self.ok_btn = self.wTree.get_widget("ok_btn")
        self.fontseldlg = self.wTree.get_widget("fontselection1")
        self.fontseldlg.set_font_name(parent.font)
        def quit_(Emty_arg): #выход
            self.window.destroy()
        self.cansel_btn.connect_object("clicked", quit_, None) #обработка нажатия клавиши "Закрыть"
        def OK_(Emty_arg): #Применить и выйти

            self.parent.font = self.window.get_font_name()

            self.window.destroy()
        self.ok_btn.connect_object("clicked", OK_, None) #Обработка нажатия клавиши "Ок"
        gtk.main()
        
    
class fsainterface(object):
    wTree = None
    def __init__(self):
        self.wTree = gtk.glade.XML( "main_interface.glade" ) #подключение glade оболочки
        self.area = self.wTree.get_widget("MainDrawingArea")
        self.font = "Sans 19"
        self.font_sel_btn = self.wTree.get_widget("font_select_btn")
        self.new_btn = self.wTree.get_widget("new_trend_btn")
        hruler1 = self.wTree.get_widget("hruler1")
        self.arrows = [] #все "стрелки"
        self.db_visual(0) #подключение БД к интерфейсу 
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify, hruler1) 
        self.new_btn.connect_object("activate", self.new_trend_dialog_open, None) #обработка нажатия клавиши "Создать"
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
            self.db_load_to_arrows()

        self.area.connect_object("button_press_event", mouseclick, None)  
        self.font_sel_btn.connect("button_press_event", self.open_font_dialog)
        gtk.main()
    def open_font_dialog(self, widget, Emty_arg):#вызов диалога выбора шрифта
        fsw = Font_selection_window(self) 
    def new_trend_dialog_open(self,Emty_arg): #Вызов диалога "новый тренд"
        ntw = New_trend_dialog(self)
    def quit(self, widget): #выход (уничтожение окна)
        self.wTree.get_widget("MainWindow").destroy()
    def rendring(self):
        self.area.window.clear()
        hg = self.area.allocation.height
        n = len(self.arrows)
        y = 50
        k = hg/(n+1)
        for ar in self.arrows:
            ar.rendring(y)
            y+=k
    def db_visual(self,rebuilding_key = 0): #обращение к интерфейсу базы данных
        type_string = "trend_name UTF8(100), comment UTF8(300),  sources TEXT(300), relationship TEXT(300), power INTEGER(2), s_point INTEGER(32), f_point INTEGER(32)"
        self.trend_base = db_interface.base(type_string)
        #trend_base.delete_db()
        self.trend_base.connect_db()
        self.trend_base.create(rebuilding_key)
    def db_load_to_arrows(self):
        trlist = self.trend_base.print_db()
        for trend in trlist:
            self.arrows.append(arrow(self.area, self.font, trend[1], trend[2], trend[3], trend[4], trend[5], trend[6], trend[7]))
        self.rendring()
        #trend_base.refresh()
    def db_add_data(self, data_string = "Name, comment, sourses, relationship, power, start_year, year_of_end"):
        self.trend_base.add_data(data_string)
        
        
aa = fsainterface()
