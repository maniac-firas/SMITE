import tkinter as tk
import mysql.connector as mys

#Program Starters
mydb = mys.connect(host='localhost', user='root', passwd = 'Firas@1704', database='Store')
myc = mydb.cursor()

#Frameworkers
class major(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('200x150')
        self._frame = None
        self.switch_frame(StartPage)
    
    def switch_frame(self, frameclass):
        new_frame = frameclass(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is a start page").pack()
        tk.Button(self, text='Open Page One', command=lambda: master.switch_frame(PageOne)).pack()
    
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack()
        tk.Button(self, text='Open Start Page', command=lambda: master.switch_frame(StartPage)).pack()

class major1(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry('200x150')
        self._frame = None
        self.switch_frame(StartPage1)
    
    def switch_frame(self, frameclass):
        new_frame = frameclass(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is a start page").pack()
        tk.Button(self, text='Open Page One', command=lambda: master.switch_frame(PageOne1)).pack()
    
class PageOne1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack()
        tk.Button(self, text='Open Start Page', command=lambda: master.switch_frame(StartPage1)).pack()

App1 = major()
App1.mainloop()