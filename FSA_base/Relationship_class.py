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
        self.to_delete = False
        self.comment = comment
        self.parent = parent
        self.area = self.parent.area
        y1 = self.trend1.y
        y2 = max(-1, self.trend2.y)
        x1 = self.trend1.s_point + (self.trend1.f_point-self.trend1.s_point)/2
        x2 = self.trend2.s_point + (self.trend2.f_point-self.trend2.s_point)/2
        self.coord = (x1,y1,x2,y2)
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
        gc.line_width = 1  
        y1 = self.trend1.y
        y2 = self.trend2.y
        x1 = self.trend1.s_point + (self.trend1.f_point-self.trend1.s_point)/2
        x2 = self.trend2.s_point + (self.trend2.f_point-self.trend2.s_point)/2
        self.coord = (x1,y1,x2,y2)
        drawable.draw_line(gc, x1, y1, x2, y2)
    def mouse_motion_on(self): #Действия при наведении мыши
        x1,y1,x2,y2 = self.coord
        drawable = self.area.window
        color = self.area.window.get_colormap().alloc(55535, 25535, 535)
        gc = drawable.new_gc()
        gc.foreground = color
        drawable.draw_arc(gc, True, x1-8, y1+8, 8, 8, 0, 360*64)
        drawable.draw_arc(gc, True, x2-5, y2-10, 8, 8, 0, 360*64)
        self.get_mouse_motion = True
    def mouse_motion_off(self):
        x1,y1,x2,y2 = self.coord
       ##
        drawable = self.area.window
        bgcolor = self.area.window.get_colormap().alloc(62194, 61937, 61680)
        gc = drawable.new_gc()
        gc.foreground = bgcolor
        drawable.draw_arc(gc, True, x1-8, y1+8, 8, 8, 0, 360*64)
        drawable.draw_arc(gc, True, x2-5, y2-10, 8, 8, 0, 360*64)
        self.get_mouse_motion = False
    