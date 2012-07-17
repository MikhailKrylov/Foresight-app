#-*- coding: utf8 -*-
'''
Created on 16.07.2012

@author: Werer
'''

#подключение библиотек
import sys, random
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
    
#главный класс для работы с графическим интерфейсом
class Font_selection_window(object):
    wTree = None
    def __init__(self, parent):
        self.wTree = gtk.glade.XML( "Font_Selection_interface.glade" ) #подключение glade оболочки
        dic = { 
            "quit" : self.quit,
            "Ok_btn_clicked" : self.font_windows_OK,
            "Close_btn_clicked": self.quit
        }
        self.wTree.signal_autoconnect(dic)
        self.window = self.FontWindow = self.wTree.get_widget("FontWindow")
        self.window
        self.parent = parent
        self.fontseldlg = self.wTree.get_widget("fontselection1")
        gtk.main()
    def quit(self, widget): #выход
        sys.getrefcount(self)
    def font_windows_OK(self,widget): 
        print "AAA"
        self.parent.font_name = self.fontseldlg.get_font_name()
        sys.getrefcount(self)
    
    
class fsainterface(object):
    wTree = None
    def __init__(self):
        self.wTree = gtk.glade.XML( "main_interface.glade" ) #подключение glade оболочки
        dic = {     
            "quit" : self.quit,
            "open_font_dialog": self.open_font_dialog
            
        }
        self.FontWindow = self.wTree.get_widget("FontWindow")
        #self.FontWindow.show()
        #self.point = (-1,-1)
        self.wTree.signal_autoconnect(dic)
        self.area = self.wTree.get_widget("MainDrawingArea")
        self.font_name = None
        self.font_sel_btn = self.wTree.get_widget("font_select_btn")
        #self.fontseldlg.show()
        hruler1 = self.wTree.get_widget("hruler1")
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify, hruler1)
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
            coord = (int(event.x), int(event.y),0,0)
            #self.draw_text(coord)
            
            if self.point == (-1, -1):
                self.point = (int(event.x), int(event.y))
            else:
                coord = (self.point[0],self.point[1], int(event.x), int(event.y))
                self.drawing_(coord)
                self.point = (-1,-1)
            
        self.area.connect_object("button_press_event", mouseclick, None)  
        self.font_sel_btn.connect_object("button_press_event", self.open_font_dialog, self.FontWindow) 
        def font_windows_OK(): #Обработка нажатия клавиши ОК на форме выбора шрифта
            self.FontWindow.hide()
       # self.wTree.get_widget("Font_d_Ok_btn").connect_object(button_press_event)
        def font_windows_Close(link_, event): #Обработка нажатия клавиши Отмена на форме выбора шрифта
            pass         
        gtk.main()
    def open_font_dialog(self, widget, ttt):
        fsw = Font_selection_window(self) 
    def quit(self, widget): #выход
        sys.exit(0)
    def drawing_(self, coord):
        x1, y1, x2, y2 = coord 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        color = drawable.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))        
        gc.foreground =color
        gc.line_width = random.randint(1,10)
        drawable.draw_line(gc, x1, y1, x2, y2)
    def draw_text(self, coord):
        x1, y1, x2, y2 = coord 
        drawable = self.area.window
        color = drawable.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        gc = drawable.new_gc() 
        gc.foreground = color
        print gtk.Style
        drawable.draw_string = (font, gc, x1, y1 , "Hello, World!")
    
        
aa = fsainterface()
        