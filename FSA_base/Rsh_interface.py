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
    def __init__(self, parent, rsh = None, Fill = True):
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
        self.comment_txt = self.wTree.get_widget('comment_txt')
        self.ok_btn = self.wTree.get_widget('ok_btn')
        self.cansel_btn.connect('clicked', self.quit_)
        self.delete_btn.connect('clicked', self.del_rsh)
        self.ok_btn.connect('clicked', self.save_)
        self.fill = Fill
        if Fill:
            self.trends_cmb_box_load(self.trend_box1, self.rsh.trend1)
            self.trends_cmb_box_load(self.trend_box2, self.rsh.trend2)
            self.type = self.rsh.type
            self.ed_res_rb.set_active(self.type)
            comment_buffer = gtk.TextBuffer(None)
            comment_buffer.set_text(self.rsh.comment)
            self.comment_txt.set_buffer(comment_buffer)
        else:
            self.new_dlg()
        gtk.main()
    def new_dlg(self):
        self.trends_cmb_box_load(self.trend_box1)
        self.trends_cmb_box_load(self.trend_box2)
    def get_ind_from_text(self, trend, cmbbox):
        model = cmbbox.get_model()
        for idex in range(len(model)):
            if model[idex][0] == trend.name:
                return idex
        return None
    def del_rsh(self, obj = None, e = None):
        self.rsh.to_delete = True
        #self.parent.rshps.remove(self.rsh)
        #del self.rsh
        self.parent.rendring()
        self.quit_()
    def get_active_text(self,combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]
    def trends_cmb_box_load(self, cmb_box, trend = None):
        #self.trend_list_box.set_wrap_width(1)
        for ar in self.parent.arrows:
            cmb_box.append_text(ar.name)
        if self.fill:
            cmb_box.set_active(self.get_ind_from_text(trend, cmb_box))
        else:
            cmb_box.set_active(0)
    def save_(self, obj = None):
        if self.fill:
            pr = [False, False]
            for ar in self.parent.arrows:
                if self.get_active_text(self.trend_box1) == ar.name:
                    self.rsh.trend1 = ar
                    pr[0] = True
                elif self.get_active_text(self.trend_box2) == ar.name:
                    self.rsh.trend2 = ar
                    pr[1] = True
            if pr[0] and pr[1]:
                comment_b = self.comment_txt.get_buffer()
                comment =str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))
                self.rsh.comment = comment
                self.rsh.type = self.ed_res_rb.get_active()
                self.parent.rendring()
                self.quit_()
            else:
                print "Выберите корректные значения."
        else:
            if self.trend_box1.get_active() and self.trend_box2.get_active():
                if self.trend_box1.get_active() != self.trend_box2.get_active():
                    trend_txt1 = self.get_active_text(self.trend_box1)
                    trend_txt2 = self.get_active_text(self.trend_box2)
                    trend1 = self.search_arrow(trend_txt1)
                    trend2 = self.search_arrow(trend_txt2)
                    comment_b = self.comment_txt.get_buffer()
                    comment =str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))
                    type = self.ed_res_rb.get_active()
                    self.rsh = relationship(self.parent, trend1, trend2, type, comment)
                    self.parent.rshps.append(self.rsh)
                    self.parent.rendring()
                    self.quit_()
    def search_arrow(self, name):
        for ar in self.parent.arrows:
            if ar.name == name:
                return ar      
    def quit_(self,e = None):
        self.window.destroy()