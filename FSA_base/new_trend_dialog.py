#-*- coding: utf8 -*-
"""
Created on 16.07.2012

Модуль содержит класс описывающий поведение диалога создания/редактирования
тенденции.

@author: Werer
"""

#подключение библиотек
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
from arrow_class import arrow #Подключение класса 'стрелки'
from Relationship_class import relationship
class Trend_dialog(object): #класс описывающий диалог внесения в базу нового тренда или редактирования существующего
    wTree = None
    def __init__(self, parent, arrow_ = None, Fill = False):
        self.parent = parent
        self.Fill = Fill #активно ли замещение текущий строки.
        self.power = 1 #Итоговая сила тренда
        ##Подключение элементов формы
        self.Arrow = arrow_
        self.wTree = gtk.glade.XML('new_trend_window3.glade')
        self.window = self.wTree.get_widget('new_trend_dialog')
        if self.Arrow:
            if self.Arrow.to_delete:
                self.to_delete_dialog()
        self.cansel_btn = self.wTree.get_widget('Cansel_btn')
        self.ok_btn = self.wTree.get_widget('Ok_btn')
        self.sp_rbtn = self.wTree.get_widget('Spower_radio_btn')
        self.up_rbtn = self.wTree.get_widget('Upower_radio_btn')
        self.mp_rbtn = self.wTree.get_widget('Mpower_radio_btn')
        self.fs_chk = self.wTree.get_widget('forse_chk')
        self.fs_chk2 = self.wTree.get_widget('forse_chk1')
        self.palitra = self.wTree.get_widget('palitra_1')
        self.s_year_text = self.wTree.get_widget('s_year_text')
        self.f_year_text = self.wTree.get_widget('f_year_text')
        self.years_scale = self.wTree.get_widget('years_scale')
        self.doc_text = self.wTree.get_widget('doc_text')
        self.srs_text = self.wTree.get_widget('srs_text')
        self.name_str = self.wTree.get_widget('name_str')
        self.to_del_btn = self.wTree.get_widget('to_delete_btn')
        color_sel_chbutn = self.wTree.get_widget('color_selection_on')
        self.error_dialog = self.wTree.get_widget('Error_dialog')
        self.trend_list_box = self.wTree.get_widget('trendlist_box')
        self.rsh_ctinue_rb = self.wTree.get_widget('cont_rb')
        self.rsh_res_rb = self.wTree.get_widget('e_res_rb')
        self.rsh_comment = self.wTree.get_widget('rsh_comment')
        self.all_add_btn = [self.wTree.get_widget('add_new_btn')]#список всех кнопок для добавления новых связей
        self.all_slctd_trds = list() #Список всех созданных ComboBox с трендами
        self.all_dis_btn = list() #Список всеъ кнопок "убрать строку"
        self.selected_trends = [list(), list(), list()] #Список всех выбранных трендов для установки связей
        
        
        self.all_slctd_trds.append(self.trend_list_box)
        self.f_year_text.set_text('2012')
        self.s_year_text.set_text('2000')
        random_color = self.parent.area.window.get_colormap().alloc(random.randint(0,65535), random.randint(0,65535), random.randint(0,65535))
        self.palitra.set_current_color(random_color)
        self.last_entry = self.s_year_text
        def hide_show(obj, active):
            if active():    self.palitra.show()
            else:   self.palitra.hide()
                
        # print event
        color_sel_chbutn.connect('toggled', hide_show, color_sel_chbutn.get_active)
        
        def scale_show(obj_, event):
            if obj_ == self.s_year_text:
                self.last_entry = self.s_year_text #Последнее выбранное поле текста
                if int(self.s_year_text.get_text())<= int(self.f_year_text.get_text()):
                    self.years_scale.set_value(int(self.s_year_text.get_text()))
                else:
                    self.years_scale.set_value(int(self.f_year_text.get_text())-1)
                    self.f_year_text.set_text(str(int(self.f_year_text.get_text())-1))
            elif obj_ == self.f_year_text:
                self.last_entry = self.f_year_text
                if int(self.f_year_text.get_text())>= int(self.s_year_text.get_text())+1:
                    self.years_scale.set_value(int(self.f_year_text.get_text()))
                else:
                    self.years_scale.set_value(int(self.s_year_text.get_text())+1)
                    self.f_year_text.set_text(str(int(self.s_year_text.get_text())+1))
        def object_hide(obj_, event = None):
            if event:
                event.hide()
            else:
                obj_.hide()
        def set_data(obj_, t_ = None, m_ = None):        
            if self.last_entry == self.f_year_text:
                if int(self.f_year_text.get_text())>= int(self.s_year_text.get_text())+1:
                    self.last_entry.set_text(str(self.years_scale.get_value())[:4])
                else:
                    self.last_entry.set_text(str(int(self.s_year_text.get_text())+1))
                    self.years_scale.set_value(int(self.s_year_text.get_text())+1)
            else:
                if int(self.s_year_text.get_text())<= int(self.f_year_text.get_text()):
                    self.last_entry.set_text(str(self.years_scale.get_value())[:4])
                else:
                    self.last_entry.set_text(str(int(self.f_year_text.get_text())-1))
                    self.years_scale.set_value(int(self.f_year_text.get_text())-1)
        self.s_year_text.connect('focus-in-event', scale_show)
        self.f_year_text.connect('focus-in-event', scale_show)
        self.years_scale.connect_object('value_changed', set_data, self.last_entry)
        def set_pwr(widget_ ,E_arg):
            if E_arg == 0 and widget_.get_active(): #Возрастающая
                act = int(self.fs_chk2.get_active())
                self.fs_chk.show()
                self.fs_chk.set_sensitive(1)
                self.fs_chk.set_active(act)
                self.fs_chk2.set_sensitive(0)
                self.fs_chk2.hide()
                self.power = 1
            elif E_arg == 1: #Неопределенная
                self.fs_chk.hide()
                self.fs_chk2.hide()
                self.power = 0
            elif E_arg == 2 and widget_.get_active(): #убывающая
                act = int(self.fs_chk.get_active())
                self.fs_chk2.show()
                self.fs_chk2.set_sensitive(1)
                self.fs_chk2.set_active(act)
                self.fs_chk.set_sensitive(0)
                self.fs_chk.hide()
                self.power = -1     
        def to_delete(obj_, e = None):
            if self.to_del_btn.get_active():
                self.doc_text.set_sensitive(0)
                self.s_year_text.set_sensitive(0)
                self.f_year_text.set_sensitive(0)
                self.years_scale.set_sensitive(0)
                self.srs_text.set_sensitive(0)
                self.palitra.set_sensitive(0)
                self.fs_chk.set_sensitive(0)
                self.up_rbtn.set_sensitive(0)
                self.mp_rbtn.set_sensitive(0)
                self.sp_rbtn.set_sensitive(0)
            else:
                self.doc_text.set_sensitive(1)
                self.s_year_text.set_sensitive(1)
                self.f_year_text.set_sensitive(1)
                self.years_scale.set_sensitive(1)
                self.srs_text.set_sensitive(1)
                self.palitra.set_sensitive(1)
                self.fs_chk.set_sensitive(1)
                self.up_rbtn.set_sensitive(1)
                self.mp_rbtn.set_sensitive(1)
                self.sp_rbtn.set_sensitive(1)
        self.sp_rbtn.connect('toggled', set_pwr, 0)
        self.up_rbtn.connect('toggled', set_pwr, 1)
        self.mp_rbtn.connect('toggled', set_pwr, 2)
        self.ok_btn.connect('clicked', self.ok_click) #обработка нажатия клавиши 'Ок'
        self.cansel_btn.connect('clicked', self.quit_) #обработка нажатия клавиши 'Закрыть'
        self.to_del_btn.connect('clicked', to_delete)
        self.wTree.get_widget('erd_ok_btn').connect('clicked',object_hide, self.error_dialog)
        self.all_add_btn[-1].connect('clicked', self.add_new_rsh_string)
        self.all_slctd_trds[-1].connect('changed',self.cmb_changed_event)
        if Fill:
            self.to_fill()
            self.years_scale.set_value(int(self.s_year_text.get_text())) #первичная инициализация значения ползунка.

        self.trends_cmb_box_load(self.all_slctd_trds[-1])
       
        gtk.main()
    
    def cmb_changed_event(self, combobox, cc = None):
        model = combobox.get_model()
        active = combobox.get_active()
        if active != 0:
            self.all_add_btn[-1].set_sensitive(1)
        else:
            self.all_add_btn[-1].set_sensitive(0)
    def removie_rsh_string(self, btn = None):
        if self.selected_trends[1][-1] == 0:
            self.rsh_ctinue_rb.set_sensitive(1)
            self.rsh_ctinue_rb.set_active(1)
        else:
            self.rsh_res_rb.set_active(1)
        rsh_cm_buffer = gtk.TextBuffer(None)
        rsh_cm_buffer.set_text(self.selected_trends[2][-1])
        self.rsh_comment.set_buffer(rsh_cm_buffer)
        self.selected_trends[0] = self.selected_trends[1][:-1]
        self.selected_trends[1] = self.selected_trends[1][:-1]
        adbt = self.all_add_btn[-1]
        self.all_add_btn.remove(adbt)
        adbt.destroy()
        slt= self.all_slctd_trds[-1]
        self.all_slctd_trds.remove(slt)
        slt.destroy()
        dbt = self.all_dis_btn[-1]
        self.all_dis_btn.remove(dbt)
        dbt.destroy()
        self.all_add_btn[-1].set_sensitive(1)
        self.all_slctd_trds[-1].set_sensitive(1)
        if len(self.all_dis_btn):
            self.all_dis_btn[-1].set_sensitive(1)
    def add_new_rsh_string(self, btn = None):
        self.all_add_btn[-1].set_sensitive(0)
        self.all_slctd_trds[-1].set_sensitive(0)
        if len(self.all_dis_btn):
            self.all_dis_btn[-1].set_sensitive(0)
        self.selected_trends[0].append(self.get_active_text(self.all_slctd_trds[-1]))
        if self.rsh_ctinue_rb.get_active():
            self.selected_trends[1].append(0)
            self.rsh_ctinue_rb.set_sensitive(0)
            self.rsh_res_rb.set_active(1)
        else:
            self.selected_trends[1].append(1)
        comment_b = self.rsh_comment.get_buffer()
        comment =str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))    
        self.selected_trends[2].append(comment)
        rsh_cm_buffer = gtk.TextBuffer(None)
        rsh_cm_buffer.set_text('')
        self.rsh_comment.set_buffer(rsh_cm_buffer)
        min_btn = gtk.Button("  -  ")
        add_btn = gtk.Button("  +  ")
        add_btn.set_sensitive(0)
        combobox = gtk.combo_box_new_text()
        py = self.all_add_btn[-1].allocation.y
        self.wTree.get_widget("fixed4").put(add_btn, 10,py+35)
        self.wTree.get_widget("fixed4").put(combobox,50,py+35)
        combobox.append_text("Выберите тренд:                               ")
        self.trends_cmb_box_load(combobox)
        self.wTree.get_widget("fixed4").put(min_btn, 310, py+35)
        self.all_dis_btn.append(min_btn)
        self.all_add_btn.append(add_btn)
        self.all_slctd_trds.append(combobox)
        self.all_add_btn[-1].connect('clicked', self.add_new_rsh_string)
        self.all_dis_btn[-1].connect('clicked', self.removie_rsh_string)
        self.all_slctd_trds[-1].connect('changed',self.cmb_changed_event)
            
        self.wTree.get_widget("fixed4").show_all()
        #print "AA 2", self.get_active_text(self)
        pp = []
        for ar in self.parent.arrows:
            if ar != self.Arrow and not (ar.name in self.selected_trends[0]):
                pp.append(ar.name)
        if len(pp)<2:
            self.all_add_btn[-1].hide()
    
    def get_active_text(self,combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]
    def trends_cmb_box_load(self, cmb_box):
        #self.trend_list_box.set_wrap_width(1)
        for ar in self.parent.arrows:
            if ar != self.Arrow and not (ar.name in self.selected_trends[0]):
                cmb_box.append_text(ar.name)
        cmb_box.set_active(0)
    def to_delete_dialog(self):
        del_wrng = self.wTree.get_widget("Delete_warning")
        del_wrng.show()
        ok_btn = self.wTree.get_widget("yes_clr_btn")
        no_btn = self.wTree.get_widget("no_cls_btn")
        def ok_click(obj_, e = None):
            self.Arrow.to_delete = False
            self.parent.rendring()
            del_wrng.destroy()
        def no_click(obj_, e = None):
            del_wrng.destroy()
            self.quit_()
        ok_btn.connect("clicked", ok_click)
        no_btn.connect("clicked", no_click)
    def to_fill(self):
        trend = self.Arrow
        if trend.power>0:
            self.sp_rbtn.set_active(1)
            if trend.power == 2:
                self.fs_chk.set_active(1)
            
        elif trend.power<0:
            self.mp_rbtn.set_active(1)
            if trend.power == -2:
                self.fs_chk2.set_active(1)
            
        else:
            self.up_rbtn.set_active(1)
        self.name_str.set_text(trend.name)
        self.name_str.set_sensitive(0)
        comment_buffer = gtk.TextBuffer(None)
        comment_buffer.set_text(trend.comment)
        self.doc_text.set_buffer(comment_buffer)
        sourses_buffer = gtk.TextBuffer(None)
        sourses_buffer.set_text(trend.sourses)
        self.srs_text.set_buffer(sourses_buffer)
        self.s_year_text.set_text(str(trend.s_time))
        self.f_year_text.set_text(str(trend.f_time))
        self.palitra.set_current_color(trend.color)
    def quit_(self, Ea = None, Ba = None):
        self.window.destroy()
    def get_ind_from_text(self, text, cmbbox):
        model = cmbbox.get_model()
        for idex in range(len(model)):
            if model[idex][0] == text:
                return idex
        return None
    def save_rshs(self):
        slctd_txt = self.get_active_text(self.all_slctd_trds[-1])
        if self.get_ind_from_text(slctd_txt,self.all_slctd_trds[-1])!= 0:
                self.selected_trends[0].append(self.get_active_text(self.all_slctd_trds[-1]))
                comment_b = self.rsh_comment.get_buffer()
                comment = str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))    
                self.selected_trends[2].append(comment)
                if self.rsh_ctinue_rb.get_active():
                    self.selected_trends[1].append(0)
                else:
                    self.selected_trends[1].append(1)
        for r_indx in range(len(self.selected_trends[0])):
            for ar in self.parent.arrows:
                if ar.name == self.selected_trends[0][r_indx]:
                    f_tr = ar
                    break
            rsh = relationship(self.parent, f_tr, self.Arrow, self.selected_trends[1][r_indx], self.selected_trends[2][r_indx])
            rsh.comment = self.selected_trends[2][r_indx]
            self.parent.rshps.append(rsh)
            
    def ok_click(self, e_arg):
        if self.to_del_btn.get_active():
            self.Arrow.to_delete = True
        plagiat = False # проверка на наличие тренда с таким названием
        name = self.name_str.get_text()
        if not self.Fill:
            for ar in self.parent.arrows:
                if ar.name == name:
                    plagiat = True
                    self.error_dialog.show()
                    self.wTree.get_widget('error_lbl1').set_text('Тенденция с таким названием уже существует')
                    self.wTree.get_widget('error_lbl2').set_text('Возможные варианты названия:')
                    self.wTree.get_widget('error_lbl3').set_text(name+" продолжение, " + name+" 1, "+ name +" "+ str(self.f_year_text.get_text()))
                    break
        if not plagiat:
            if len(name)<3:
                self.error_dialog.show()
                self.wTree.get_widget('error_lbl1').set_text('')
                self.wTree.get_widget('error_lbl2').set_text('Ошибка! Введите название!')
                self.wTree.get_widget('error_lbl3').set_text('')
           
            else:
                comment_b = self.doc_text.get_buffer()
                comment =str(comment_b.get_text(comment_b.get_start_iter(), comment_b.get_end_iter()))
                sourses_b = self.srs_text.get_buffer()
                sourses =str(sourses_b.get_text(sourses_b.get_start_iter(), sourses_b.get_end_iter()))
                if self.fs_chk.get_active() or self.fs_chk2.get_active():
                    self.power*=2
                try:
                    int(self.s_year_text.get_text())
                    int(self.f_year_text.get_text())
                except:
                    self.error_dialog.show()
                    self.wTree.get_widget('error_lbl1').set_text('')
                    self.wTree.get_widget('error_lbl2').set_text('Ошибка: введите корректные даты!')
                    self.wTree.get_widget('error_lbl3').set_text('')
                    return 0
                if  int(self.s_year_text.get_text()) < int(self.f_year_text.get_text()) and int(self.s_year_text.get_text()) in range(2000,2055) and int(self.f_year_text.get_text()) in range(2000,2055): 
                    s_year =str(self.s_year_text.get_text())
                    f_year =str(self.f_year_text.get_text())
                    power = self.power
                    color = self.palitra.get_current_color()
                    if self.Fill:
                        self.arrow_from_data(comment, sourses, f_year, s_year, color)
                        #if len(self.selected_trends[0])>=1:
                        self.save_rshs()
                    else:
                        self.Arrow = arrow(self.parent, name, comment, sourses, power, s_year, f_year)
                        self.parent.arrows.append(self.Arrow)
                        #if len(self.selected_trends[0])>=1:
                        self.save_rshs()
                    self.parent.rendring()
                    
                    self.quit_()
                else:
                    self.error_dialog.show()
                    self.wTree.get_widget('error_lbl1').set_text('')
                    self.wTree.get_widget('error_lbl2').set_text('Ошибка: введите корректные даты!')
                    self.wTree.get_widget('error_lbl3').set_text('')
    def arrow_from_data(self, comment, sourses, f_year, s_year, color):                        
        self.Arrow.comment = comment
        self.Arrow.sourses = sourses
        self.Arrow.f_time = int(f_year)
        self.Arrow.s_time = int(s_year)
        self.Arrow.color = self.parent.area.window.get_colormap().alloc(color)