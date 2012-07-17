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
class fsainterface(object):
    wTree = None
    def __init__(self):
        self.wTree = gtk.glade.XML( "main_interface.glade" ) #подключение glade оболочки
        dic = { 
            "quit" : self.quit,
        }
        self.point = (-1,-1)
        self.wTree.signal_autoconnect( dic )
        self.area = self.wTree.get_widget("MainDrawingArea")
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
        gtk.main()
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
        font = gtk.gdk.Font("Sans")
        drawable.draw_string = (font, gc, x1, y1 , "Hello, World!")
        
aa = fsainterface()
        