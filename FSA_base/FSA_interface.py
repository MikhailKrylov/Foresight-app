'''
Created on 16.07.2012

@author: Werer
'''
#-*- coding: utf8 -*-
import sys
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

class fsainterface(object):
    wTree = None
    def __init__(self):
        self.wTree = gtk.glade.XML( "main_interface.glade" )
        dic = { 
            "quit" : self.quit,
        }
        self.wTree.signal_autoconnect( dic )
        self.area = self.wTree.get_widget("MainDrawingArea")
        hruler1 = self.wTree.get_widget("hruler1")
        def motion_notify(ruler, event):
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify, hruler1)
        # self.drawing_(coord)
        def mouseclick(Empty_arg,event = None):
            coord = (0,0, int(event.x), int(event.y))
            self.drawing_(coord)
            
        self.area.connect_object("button_press_event", mouseclick, None)   
        gtk.main()
    def quit(self, widget):
        sys.exit(0)
    def drawing_(self, coord):
        x1, y1, x2, y2 = coord
        style = self.area.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        drawable = self.area.window
        drawable.draw_line(gc, x1, y1, x2, y2)

aa = fsainterface()
        