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
        hruler1 = self.wTree.get_widget("hruler1")
        def motion_notify(ruler, event):
            return ruler.emit("motion_notify_event", event)
        self.wTree.get_widget("MainDrawingArea").connect_object("motion_notify_event", motion_notify, hruler1)
        gtk.main()
    def quit(self, widget):
        sys.exit(0)


aa = fsainterface()
        