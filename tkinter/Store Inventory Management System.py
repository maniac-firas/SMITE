import tkinter as tk
import mysql.connector as mys
from tkinter import messagebox
import csv
from Display import displayDatabase
from Enter import fEnter
from PickOrRefill import fPOR

#Program Starters
dfont = ('Helvetica', 15, 'normal')
grey, orange, white = '#36454f', '#fb8b24', '#faf0e6'
mydb, myc = None, None

def remove_items(list, item):  
    res = [i for i in list if i != item] 
    return res
def establish_table(mydb, myc):
    myc.execute('Drop Table if exists Stock;')
    q1 = """CREATE TABLE stock (
        SKU VARCHAR(50) NOT NULL PRIMARY KEY,
        product_name VARCHAR(40),
        Type VARCHAR(30),
        Company VARCHAR(30),
        Floor CHAR(1),
        Rack VARCHAR(3),
        MRP VARCHAR(5),
        Quantity VARCHAR(2),
        DOM DATE,
        Delivery VARCHAR(2),
        Status VARCHAR(15)
    )"""
    myc.execute(q1)
    mydb.commit()
    
    with open('Stock.csv', 'r') as f:
        csv_reader = list(csv.reader(f))
        csv_reader = remove_items(csv_reader, [])

        for row in csv_reader:
            q2 = """INSERT INTO stock (SKU, product_name, Type, Company, Floor, Rack, MRP, Quantity, DOM, Delivery, Status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            myc.execute(q2, row)            
            mydb.commit()

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class major(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.config(bg=grey)
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(LoginPage, 'S.M.I.T.E', '1000x700')
    
    def switch_frame(self, frameclass, heading, dimensions):
        self.geometry(dimensions)
        self.title(heading)
        center(self)
        new_frame = frameclass(self)
        if self._frame is not None: self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def kill(self):
        self.destroy()

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_geometry()
        self.pack(fill = tk.BOTH, expand = True)
        self.config(bg=orange)
        tk.Canvas(self, bg=white, bd=4, height=500, width=800, relief=tk.RAISED).place(x=500, y=350, anchor=tk.CENTER)
        tk.Label(self, bg=white, fg=grey, text='Store Management Inventory Techonological Environment', font = ('Georgia', 22, 'normal')).place(rely=0.25, relx=0.5, anchor=tk.CENTER)
        tk.Label(self, bg=white, fg=grey, text='(S.M.I.T.E.)', font = ('Georgia', 22, 'normal')).place(rely=0.3, relx=0.5, anchor=tk.CENTER)
        
        self.lbl = tk.Label(master, text='MySQL Password', bg=white, font=('Georgia', 17, 'normal')).place(x=300, y=350)
        self.entvar = tk.StringVar()
        self.entvar.set('')
        self.ent = tk.Entry(master, textvariable=self.entvar, font=('Georgia', 17, 'normal'), show='*').place(x=500, y=350, width=200)
        self.sbtn = tk.Button(master, text='Submit', command = lambda:  self.submit(master), font=('Georgia', 17, 'normal')).place(x=400, y=400, width=200)

    def submit(self, master):
        global mydb, myc
        try:
            mydb = mys.connect(host='localhost', user='root', passwd = self.entvar.get())
            myc = mydb.cursor()
            myc.execute('create database if not exists store')
            myc.execute('Use Store')
            master.switch_frame(StartPage, 'S.M.I.T.E.', '1000x700')
        except:
            messagebox.showwarning('Connection Paused', 'Password is not correct')
        establish_table(mydb, myc)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_geometry()
        self.pack(fill = tk.BOTH, expand = True)
        self.config(bg=white)
        tk.Canvas(self, bg=orange, height=200, width=1000).place(x=500, y=50, anchor=tk.CENTER)
        tk.Label(self, bg=orange, fg=white, text='Store Management Inventory Techonological Environment', font = ('Georgia', 25, 'normal')).place(rely=0.15, relx=0.5, anchor=tk.CENTER)

        #Display
        image = tk.PhotoImage(file='Bitmaps/Displaydatabase.png')
        img = image.subsample(3, 3)
        tk.Button(self, bg='#e1d9d1', bd=2, cursor='hand2', width=int((5/4)*20), height=int((5/4)*9), command=lambda: master.switch_frame(DisplayPage, 'Display Products', '1800x700')).place(x=200, y=300, anchor=tk.CENTER)
        tk.Label(self, bg=white, text='Display Products', font=dfont).place(x=203, y=410, anchor=tk.CENTER)

        tk.Button(self, bg='#e1d9d1', bd=2, cursor='hand2', width=int((5/4)*20), height=int((5/4)*9), command=lambda: master.switch_frame(EnterPage, 'Enter New Product','1000x700')).place(x=500, y=300, anchor=tk.CENTER)
        tk.Label(self, bg=white, text='Enter Product', font=dfont).place(x=503, y=410, anchor=tk.CENTER)

        tk.Button(self, bg='#e1d9d1', bd=2, cursor='hand2', width=int((5/4)*20), height=int((5/4)*9), command=lambda: PORPage(master)).place(x=800, y=300, anchor=tk.CENTER)
        tk.Label(self, bg=white, text='Picking/Refill', font=dfont).place(x=803, y=410, anchor=tk.CENTER)

class DisplayPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        displayDatabase(self, mydb)
        tk.Button(master, text='BACK', cursor='hand2', command=lambda: master.switch_frame(StartPage, 'S.M.I.T.E', '1000x700')).place(x=40, y=20)
        tk.Button(master, text='REFRESH', cursor='hand2', command=lambda:  master.switch_frame(DisplayPage, 'Display Products', '1800x700')).place(x=100, y=20)

class EnterPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        fEnter(self, mydb)
        tk.Button(master, text='BACK', cursor='hand2', command=lambda: master.switch_frame(StartPage, 'S.M.I.T.E', '1000x700')).place(x=30, y=20)   

def PORPage(master):
    fPOR(master, mydb)

if __name__ == '__main__':
    App = major()
    App.mainloop()

