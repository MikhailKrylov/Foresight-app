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

class fildeialog(object):
    wTree = None
    def __init__(self, parent, new_key = False, visible = True):
        self.new_key = new_key
        self.parent = parent #ссылка на 'родителя'
        self.wTree = gtk.glade.XML( 'file_dlg.glade' ) #подключение glade оболочки
        self.window = self.wTree.get_widget('db_chned_dialog')
        self.cls_btn = self.wTree.get_widget('fd_close')
        self.ok_btn = self.wTree.get_widget('fd_ok')
        if visible:
            self.window.show()
        self.cls_btn.connect('clicked', self.quit_)
        self.ok_btn.connect('clicked', self.ok_)
        gtk.main()
    def quit_(self,e = None):
        self.window.destroy()
    def ok_(self, obj = None):
        filename = self.window.get_filename()
        if filename[-3:]!='.db':
            print "Выберите файл с расширением .db"
        else:
            if not self.new_key:
                self.parent.db_name = filename
                try:
                    self.parent.db_visual(0)
                    self.parent.db_load_to_arrows()
                except:
                    print "выберите корректный файл или создайте новую БД"
            else:
                self.parent.db_name = filename
                self.parent.db_visual(1)
                self.parent.db_load_to_arrows()
            self.quit_()