#-*- coding: utf8 -*-
import sys, random, pango, time
#from curses.ascii import NUL
try:  
    import pygtk  
    pygtk.require('2.0')  
except:  
    pass  
try:  
    import gtk  
    import gtk.glade  
except:  
    print('GTK Not Availible')
    sys.exit(1)
from arrow_class import arrow
from Relationship_class import relationship
class edit_rsh_dialog(object):
    wTree = None
    def __init__(self, parent, rsh = None):
        self.rsh = rsh
        self.parent = parent #ссылка на 'родителя'
        self.wTree = gtk.glade.XML( 'rsh_edit.glade' ) #подключение glade оболочки
        self.window = self.wTree.get_widget('edit_trend_dialog')
        self.cansel_btn = self.wTree.get_widget('canсel_btn')
        self.trend_box1 = self.wTree.get_widget('trend_bx1')
        self.trend_box2 = self.wTree.get_widget('trend_bx2')
        self.cont_rb = self.wTree.get_widget('cont_prev_rb')
        self.ed_res_rb = self.wTree.get_widget('ed_res_rb')
        self.delete_btn = self.wTree.get_widget('del_btn')
        self.cansel_btn.connect('clicked', self.quit_)
        self.delete_btn.connect('clicked', self.del_rsh)
        self.trends_cmb_box_load(self.trend_box1, self.rsh.trend1)
        self.trends_cmb_box_load(self.trend_box2, self.rsh.trend2)
        self.type = self.rsh.type
        self.ed_res_rb.set_active(self.type)
        gtk.main()
    def get_ind_from_text(self, trend, cmbbox):
        model = cmbbox.get_model()
        for idex in range(len(model)):
            if model[idex][0] == trend.name:
                return idex
        return None
    def del_rsh(self, obj = None, e = None):
        self.rsh.to_delete = True
        self.parent.rshps.remove(self.rsh)
        del self.rsh
        self.parent.rendring()
        self.quit_()
    def get_active_text(self,combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]
    def trends_cmb_box_load(self, cmb_box, trend):
        #self.trend_list_box.set_wrap_width(1)
        for ar in self.parent.arrows:
            cmb_box.append_text(ar.name)
        cmb_box.set_active(self.get_ind_from_text(trend, cmb_box))
        
    def quit_(self,e = None):
        self.window.destroy()