#-*- coding: utf8 -*-
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

class relationship(object):
    '''
    classdocs
    '''


    def __init__(self, parent, first_trend, second_trend, type, comment, pos = None):
        self.trend1 = first_trend
        self.trend2 = second_trend
        self.type = type
        self.comment = comment
        self.parent = parent
        self.area = self.parent.area
        if type == 1: 
            self.color  = self.area.window.get_colormap().alloc(0, 65535, 0)
        else:
            self.color  = self.area.window.get_colormap().alloc(0, 0, 65535)
    def __del__(self):
        pass
    def rendring(self):
        drawable = self.area.window
        gc = drawable.new_gc() 
        gc.foreground = self.color
        gc.line_width = 2  
        y1 = self.trend1.y
        y2 = self.trend2.y
        x1 = self.trend1.s_point + (self.trend1.f_point-self.trend1.s_point)/2
        x2 = self.trend2.s_point + (self.trend2.f_point-self.trend2.s_point)/2
        drawable.draw_line(gc, x1, y1, x2, y2)