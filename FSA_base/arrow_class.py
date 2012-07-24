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
    def __init__(self, dw_area, font, name, comment, sourses, relationship, power, start_year, year_of_end):
        self.area = dw_area
        self.font = font
        self.color = dw_area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.name = name
        self.comment = comment
        self.sourses = sourses
        self.relationship = relationship
        self.power = power
     
        self.f_time = start_year
        self.l_time = year_of_end
        sf = float(self.area.allocation.width)
        st = float(self.f_time) - 2000.
        self.f_point = int(sf/55. * (st))
        self.l_piont = int(float(self.area.allocation.width)/55. * (self.l_time - 2000.))
        self.text_rnd = True
        self.arrow_rnd = True
    def rendring(self, y):
        self.y = y
        x1 = self.f_point
        x2 = self.l_piont 
        drawable = self.area.window
        #gc Graphics Context, т.е. параметры.
        gc = drawable.new_gc() 
        #цвет задается в интервале от 0 до 65535
        gc.foreground = self.color
        gc.line_width = abs(self.power)
        
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
        layout = self.area.create_pango_layout(self.name)
        layout.set_font_description(pango.FontDescription(self.font))
        font_size = int(self.font.split(" ")[1])*2
        drawable.draw_layout(gc, x1, self.y-font_size, layout)