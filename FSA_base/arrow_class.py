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
class arrow(object): 
    def __init__(self, dw_area, font, name, comment, sourses, relationship, power, start_year, year_of_end, id = 0):
        self.id = id
        self.area = dw_area
        self.font = font
        self.color = dw_area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.name = name
        self.comment = comment
        self.sourses = sourses
        self.relationship = relationship
        self.power = power
        self.s_time = start_year
        self.f_time = year_of_end
        #sf = float(self.area.allocation.width)
        #st = float(self.s_time) - 2000.
        self.s_point = int(float(self.area.allocation.width)/55. * (float(self.s_time) - 2000.))
        self.f_point = int(float(self.area.allocation.width)/55. * (self.f_time - 2000.))
        self.text_rnd = True
        self.arrow_rnd = True
        self.get_mouse_motion = False
    def rendring(self, y):
        self.s_point = int(float(self.area.allocation.width)/55.0 *(float(self.s_time) - 2000.))
        self.f_point = int(float(self.area.allocation.width)/55.0 * (self.f_time - 2000.))
        self.y = y
        x1 = self.s_point
        x2 = self.f_point 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        gc.foreground = self.color
        gc.line_width = abs(self.power)+1  
        if self.power == 0: gc.line_width = 2
        if self.power > 0:
            drawable.draw_line(gc, x1, self.y, x2, self.y)
        elif self.power <0:
            tx = x1+abs(self.power)*5
            while tx <= x2:
                drawable.draw_line(gc, x1, self.y, tx, self.y)
                x1 = tx+abs(self.power)*5
                tx = x1+abs(self.power)*5
        else:
            tx = x1+10
            n = 1
            while x1 <= x2-10:
                drawable.draw_arc(gc, False, x1, y, 20, 4, 0, n*360*32)
                x1 +=22
                n = -1*n
            
        if self.text_rnd == True:
            self.render_text()
        if self.arrow_rnd == True:
            drawable.draw_line(gc, x2-abs(self.power+3)*2, self.y-abs(self.power+3)*2, x2, self.y+1)
            drawable.draw_line(gc, x2-abs(self.power+3)*2, self.y+abs(self.power+3)*2, x2, self.y-1)
    def render_text(self):
        x1 = self.s_point
        drawable = self.area.window
        gc = drawable.new_gc() 
        gc.foreground = self.color
        layout = self.area.create_pango_layout(self.name)
        layout.set_font_description(pango.FontDescription(self.font))
        font_size = int(self.font.split(" ")[-1])*2
        drawable.draw_layout(gc, x1, self.y-font_size, layout)
    def selected(self):
        pass
    def mouse_motion_on(self): #Действия при наведении мыши
        drawable = self.area.window
        color = self.area.window.get_colormap().alloc(55535, 25535, 535)
        gc = drawable.new_gc()
        gc.foreground = color
        drawable.draw_arc(gc, True, self.s_point-14, self.y-6, 12, 12, 0, 360*64)
        self.get_mouse_motion = True
    def mouse_motion_off(self):
        drawable = self.area.window
        bgcolor = self.area.window.get_colormap().alloc(62194, 61937, 61680)
        gc = drawable.new_gc()
        gc.foreground = bgcolor
        drawable.draw_arc(gc, True, self.s_point-14, self.y-6, 12, 12, 0, 360*64)
        self.get_mouse_motion = False