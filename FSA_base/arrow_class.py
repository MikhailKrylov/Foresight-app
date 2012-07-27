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
    def __init__(self, dw_area, font, name, comment, sourses,  power, start_year, year_of_end, id = 0):
        self.id = id
        self.area = dw_area
        self.font = font
        self.color = dw_area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.name = name
        self.comment = comment
        self.sourses = sourses
        self.relationship = None
        self.power = power
        self.s_time = start_year
        self.f_time = year_of_end
        self.s_point = int(float(self.area.allocation.width)/55. * (float(self.s_time) - 2000.))
        self.f_point = int(float(self.area.allocation.width)/55. * (float(self.f_time) - 2000.))
        self.text_rnd = True
        self.arrow_rnd = True
        self.get_mouse_motion = False
        self.to_delete = False
    def __del__(self):
        pass
    def rendring(self, y):
        s_point = int(float(self.area.allocation.width)/55.0 * (float(self.s_time) - 2000.))
        f_point = int(float(self.area.allocation.width)/55.0 * (float(self.f_time) - 2000.))
        self.s_point, self.f_point = s_point, f_point
        self.y = y
        x1 = s_point
        x2 = f_point 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        gc.foreground = self.color
        gc.line_width = abs(int(self.power))+1  
        if self.to_delete:
            tx = x1+5
            while tx <= x2:
                gc.line_width = 1
                drawable.draw_line(gc, x1, self.y+3, tx, self.y-3)
                drawable.draw_line(gc, x1, self.y-3, tx, self.y+3)
                x1 = tx+5
                tx = x1+5
        elif self.power > 0:
            drawable.draw_line(gc, x1, self.y, x2, self.y)
        elif self.power <0:
            tx = x1+abs(int(self.power))*5
            while tx <= x2:
                drawable.draw_line(gc, x1, self.y, tx, self.y)
                x1 = tx+abs(int(self.power))*5
                tx = x1+abs(int(self.power))*5
        else:
            gc.line_width = 2
            tx = x1+10
            n = 1
            while x1 <= x2-10:
                drawable.draw_arc(gc, False, x1, y, 20, 4, 0, n*360*32)
                x1 +=22
                n = -1*n
            
        if self.text_rnd:
            self.render_text()
        if self.arrow_rnd:
            drawable.draw_line(gc, x2-abs(int(self.power)+3)*2, self.y-abs(int(self.power)+3)*2, x2, self.y+1)
            drawable.draw_line(gc, x2-abs(int(self.power)+3)*2, self.y+abs(int(self.power)+3)*2, x2, self.y-1)
    def render_text(self):
        s_point = int(float(self.area.allocation.width)/55.0 * (float(self.s_time) - 2000.))
        f_point = int(float(self.area.allocation.width)/55.0 * (float(self.f_time) - 2000.))
        self.s_point, self.f_point = s_point, f_point
        x1 = s_point
        drawable = self.area.window
        gc = drawable.new_gc() 
        gc.foreground = self.color
        if self.to_delete:
            gc.foreground =  self.area.window.get_colormap().alloc(65535,0,0)
            layout = self.area.create_pango_layout('!У! '+self.name +' !У!')
        else:
            layout = self.area.create_pango_layout(self.name)
        layout.set_font_description(pango.FontDescription(self.font))
        font_size = int(self.font.split(" ")[-1])*2
        drawable.draw_layout(gc, x1, self.y-font_size, layout)
    def selected(self):
        pass
    def mouse_motion_on(self): #Действия при наведении мыши
        s_point = int(float(self.area.allocation.width)/55.0 * (float(self.s_time) - 2000.))
        f_point = int(float(self.area.allocation.width)/55.0 * (float(self.f_time) - 2000.))
        self.s_point, self.f_point = s_point, f_point
        drawable = self.area.window
        color = self.area.window.get_colormap().alloc(55535, 25535, 535)
        gc = drawable.new_gc()
        gc.foreground = color
        drawable.draw_arc(gc, True, s_point-14, self.y-6, 12, 12, 0, 360*64)
        self.get_mouse_motion = True
    def mouse_motion_off(self):
        s_point = int(float(self.area.allocation.width)/55.0 * (float(self.s_time) - 2000.))
        f_point = int(float(self.area.allocation.width)/55.0 * (float(self.f_time) - 2000.))
        self.s_point, self.f_point = s_point, f_point
        drawable = self.area.window
        bgcolor = self.area.window.get_colormap().alloc(62194, 61937, 61680)
        gc = drawable.new_gc()
        gc.foreground = bgcolor
        drawable.draw_arc(gc, True, s_point-14, self.y-6, 12, 12, 0, 360*64)
        self.get_mouse_motion = False