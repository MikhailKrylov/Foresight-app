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
class trend_class(object): 
    def __init__(self, dw_area, font, parameters = 0):
        self.area = dw_area
        self.power = 2
        self.font = font
        self.color = dw_area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.f_time = 2010
        self.l_time = 2050
        self.f_point = int(float(self.area.allocation.width)/55. * (self.f_time - 2000.))
        self.l_piont = int(float(self.area.allocation.width)/55. * (self.l_time - 2000.))
        self.text = u"Эколофт"
        self.y = 300
        self.text_rnd = True
        self.arrow_rnd = True
    def rendring(self):
        x1 = self.f_point
        x2 = self.l_piont 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        gc.foreground = self.color
        gc.line_width = self.power*2
        drawable.draw_line(gc, x1, self.y, x2, self.y)
        if self.text_rnd == True:
            self.render_text()
        if self.arrow_rnd == True:
            drawable.draw_line(gc, x2-self.power*5, self.y-self.power*5, x2, self.y+1)
            drawable.draw_line(gc, x2-self.power*5, self.y+self.power*5, x2, self.y-1)
    def render_text(self):
        x1 = self.f_point
        drawable = self.area.window
        gc = drawable.new_gc() 
        gc.foreground = self.color
        layout = self.area.create_pango_layout(self.text)
        layout.set_font_description(pango.FontDescription(self.font))
        font_size = int(self.font.split(" ")[1])*2
        drawable.draw_layout(gc, x1, self.y-font_size, layout)
#главный класс для работы с графическим интерфейсом
class New_trend_dialog(object): #класс описывающий диалог внесения в базу нового тренда или редактирования существующего
    wTree = None
    def __init__(self, parent):
        self.parent = parent
        self.wTree = gtk.glade.XML("new_trend_window3.glade")
        self.window = self.wTree.get_widget("new_trend_dialog")
        self.cansel_btn = self.wTree.get_widget("Cansel_btn")
        def quit_(Emty_arg): #выход
            self.window.destroy()
        self.cansel_btn.connect("clicked", quit_) #обработка нажатия клавиши "Закрыть"
        gtk.main()
    def quit_(self):
        self.window.destroy()
    
class Font_selection_window(object): #класс описывающий диалог выбора шрифта
    wTree = None
    def __init__(self, parent):
        self.wTree = gtk.glade.XML( "Font_Selection_interface2.glade" ) #подключение glade оболочки
        self.window = self.wTree.get_widget("FontWindow")
        self.cansel_btn = self.wTree.get_widget("cancel_btn")
        self.ok_btn = self.wTree.get_widget("ok_btn")
        self.parent = parent
        self.fontseldlg = self.wTree.get_widget("fontselection1")
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
        self.point = (-1,-1)
        self.area = self.wTree.get_widget("MainDrawingArea")
        self.font = "Sans 19"
        #self.area.allocation.height
        self.font_sel_btn = self.wTree.get_widget("font_select_btn")
        self.new_btn = self.wTree.get_widget("new_trend_btn")
        hruler1 = self.wTree.get_widget("hruler1")
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify, hruler1) 
        self.new_btn.connect_object("activate", self.new_trend_dialog_open, None) #обработка нажатия клавиши "Создать"
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
            coord = (int(event.x), int(event.y),0,0)
            self.db_visual(coord)
            if self.point == (-1, -1):
                self.point = (int(event.x), int(event.y))
            else:
                coord = (self.point[0],self.point[1], int(event.x), int(event.y))
                #self.drawing_line(coord)
                aa = trend_class(self.area, self.font)

        self.area.connect_object("button_press_event", mouseclick, None)  
        self.font_sel_btn.connect("button_press_event", self.open_font_dialog)
        gtk.main()
    def open_font_dialog(self, widget, Emty_arg):#вызов диалога выбора шрифта
        fsw = Font_selection_window(self) 
    def new_trend_dialog_open(self,Emty_arg): #Вызов диалога "новый тренд"
        ntw = New_trend_dialog(self)
    def quit(self, widget): #выход (уничтожение окна)
        self.wTree.get_widget("MainWindow").destroy()
    def drawing_line(self, coord, color):
        x1, y1, x2, y2 = coord 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        color = drawable.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))        
        gc.foreground = color
        gc.line_width = random.randint(1,10)
        drawable.draw_line(gc, x1, y1, x2, y2)
    def draw_text(self, coord, text):  #Функция отображения текса в Drawing Area
      pass
    def db_visual(self,coord): #обращение к интерфейсу базы данных
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
        trend_base.add_data(nm +u', '+ cm +u', '+ sa+',' + sv+u',' + s_p+u',' + f_p)
        drstr = trend_base.print_db()
        self.draw_text(coord, drstr)
aa = fsainterface()
