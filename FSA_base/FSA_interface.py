#-*- coding: utf8 -*-
'''
Created on 16.07.2012

@author: Werer
'''

#подключение библиотек
import sys, random, pango
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
        self.wTree = gtk.glade.XML( "Font_Selection_interface2.glade" ) #подключение glade оболочки
        self.window = self.FontWindow = self.wTree.get_widget("FontWindow")
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
        self.font_sel_btn = self.wTree.get_widget("font_select_btn")
        hruler1 = self.wTree.get_widget("hruler1")
        def motion_notify(ruler, event): #обработка движения мыши по зоне рисования
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify, hruler1)
        def mouseclick(Empty_arg,event = None): #обработка щелчка мыши по зоне рисования
            coord = (int(event.x), int(event.y),0,0)
            self.draw_text(coord)
            '''
            if self.point == (-1, -1):
                self.point = (int(event.x), int(event.y))
            else:
                coord = (self.point[0],self.point[1], int(event.x), int(event.y))
                self.drawing_(coord)
                self.point = (-1,-1)
            '''
        self.area.connect_object("button_press_event", mouseclick, None)  
        self.font_sel_btn.connect("button_press_event", self.open_font_dialog) 
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
        #color = drawable.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        gc = drawable.new_gc() 
        #gc.foreground = color
        font = gtk.gdk.Font(self.font)
        gc.font = font
        layout = self.area.create_pango_layout("Text")
        layout.set_font_description(pango.FontDescription(self.font))
        drawable.draw_layout(gc, x1, y1, layout)
        
aa = fsainterface()
        