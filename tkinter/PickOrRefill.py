import tkinter as tk
from tkinter import messagebox
import csv

pdfont = ('Helvetica', 17, 'normal')
phfont = ('Helvetica', 14, 'normal')
grey, orange, white = '#36454f', '#fb8b24', '#faf0e6'

def center_main(win):
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
def center(window, dimensions):
    window.update_idletasks()
    di = dimensions.split('x')
    width, height = int(di[0]), int(di[1])
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def remove_items(list, item):  
    res = [i for i in list if i != item] 
    return res
def insertFile(Data): 
    with open('Picking.csv', 'a', newline='\n') as f:
        fw = csv.writer(f)
        fw.writerow(Data)
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
def refresh(pB):
    pB.delete_all()
    with open('Picking.csv', 'r') as f:
        fr = csv.reader(f)
        pB.insert(fr)
def pickSKU():
    temp = []
    with open('Picking.csv', 'r') as f:
        fr = list(csv.reader(f))
        fr = remove_items(fr, [])
        for rec in fr:  temp.append(int(rec[0][3:6]))
    return temp

ptable = []
pslot1 = 0
phead = ['SKU', 'Product Name', 'Company', 'Floor', 'Rack', 'Quantity']

class pBox():
    def __init__(self, parent):
        self.scroll_bar = tk.Scrollbar(parent, orient = tk.VERTICAL)
        self.scroll_bar.pack(side = tk.RIGHT)
        self.Tb = tk.Text(parent, width = 500, height = 500, bg=white, yscrollcommand=self.scroll_bar.set, wrap='none', font = ('Helvetica', 17, 'normal'))
        
    def insert(self, data):
        text=self.Tb.get("1.0",tk.END)
        text=text[:-4]
        self.Tb.delete('1.0', tk.END)
        self.Tb.insert(tk.INSERT,text)

        global ptable, pslot1
        for row in data:
            if row == []: continue
            slot2 = 0
            ptable.append(list())
            for t in row:
                ptable[pslot1].append(t)
                self.Tb.insert(tk.END, '        '+phead[slot2]+' : '+str(ptable[pslot1][slot2])+'\n')                
                slot2+=1
            self.Tb.insert(tk.END, '_'*100+'\n')
            pslot1+=1

        self.Tb.insert(tk.END, '\n\n\n')
        self.Tb.pack(side=tk.LEFT)
        self.scroll_bar.config(command=self.Tb.yview)

    def delete(self, start):
        self.Tb.delete(float(start),float(start+2))
        self.Tb.update()

    def delete_all(self):
        self.Tb.delete(1.0,tk.END)
        self.Tb.update()

def fPOR(root, mydb):
    myc = mydb.cursor()

    def PickPage(tp):
        tp.destroy()
        tp.update()

        class fPick(tk.Toplevel):
            def __init__(self):
                tk.Toplevel.__init__(self, bg=orange)
                self.title('Picking')
                tk.Label(self, text='Picking Orders', bg=orange, fg=white, font=('Georgia', 20, 'normal')).place(x=410, y=10)
                center(self, '1000x550')
                frame = tk.Frame(self, width=1000, height=1000)
                frame.place(y=100, relx=0, rely=0, relwidth=1, relheight=1)
                tk.Button(self, text='Place Order', font=pdfont, width=15, bd=3, command=lambda: self.addData(pB)).place(x=300, y=50)
                tk.Button(self, text='Approve Order', font=pdfont, width=15, bd=3, command=lambda: self.removeData(pB)).place(x=500, y=50)
                pB = pBox(frame)
                with open('Picking.csv', 'r') as f:
                    fr = csv.reader(f)
                    pB.insert(fr)

            def addData(self, tB):
                class Amajor(tk.Toplevel):
                    def __init__(self):
                        tk.Toplevel.__init__(self)
                        self.title('Update Order')
                        center(self, '500x400')
                        self.config(bg=grey)
                        self._frame = None
                        self.switch_frame(AStartPage)                    

                    def switch_frame(self, frameclass):
                        new_frame = frameclass(self)
                        if self._frame is not None:
                            self._frame.destroy()
                        self._frame = new_frame
                        self._frame.pack()

                class AStartPage(tk.Frame):
                    def __init__(self, master):
                        tk.Frame.__init__(self, master)
                        self.pack(fill = tk.BOTH, expand = True)
                        tk.Label(self, text='Order for Picking', justify='center', fg=grey, font=('Helvetica', 18, 'bold')).pack(pady = 50, side = tk.TOP, fill=tk.BOTH, expand=True)
                        tk.Label(self, text='Enter Order No', justify='center', fg=grey, font=pdfont).pack(side = tk.TOP, fill=tk.BOTH, expand=True)
                        self.var = tk.StringVar()
                        tk.Entry(self, textvariable=self.var, font=('Calibri', 16, 'normal'), fg=grey, relief='raised').pack(side = tk.TOP, fill=tk.BOTH, expand=True)
                        tk.Button(self, text='Submit', font=pdfont, width=10, height=15, command=lambda: self.submit(master), fg=grey, justify='center').pack(side = tk.BOTTOM, pady=90)

                    def submit(self, master):
                        No = self.var.get()
                        n = len(str(No))
                        z = 3-n
                        Beg = 'SKU'+z*'0'+str(No)
                        recs, orecs, nrec = [], [], 0
                        myc.execute('select SKU from stock ORDER BY SKU')
                        temp=myc.fetchall()
                        myc.execute('select SKU from stock where Status = "Out of Stock"')
                        OS = myc.fetchall()
                        print(OS)
                        for i in range(len(temp)): 
                            recs.append(temp[i][0])
                            recs[i] = int(recs[i][3:6])
                            nrec = recs[i]
                        for i in range(len(OS)): 
                            orecs.append(OS[i][0])
                            orecs[i] = int(orecs[i][3:6])
                        print(orecs)
                        if self.var.get() == '':    pass
                        elif int(self.var.get()) > nrec or int(self.var.get()) not in recs:
                            messagebox.showerror('Store Inventory', Beg[0:len(Beg)]+' does not exist')
                            raise_above_all(jk)
                        elif int(self.var.get()) in pickSKU():
                            messagebox.showerror('Store Inventory', Beg[0:len(Beg)]+' is already added')
                            raise_above_all(jk)
                        elif int(self.var.get()) in orecs:
                            messagebox.showerror('Store Inventory', Beg[0:len(Beg)]+' is not available(Out of Stock)')
                            raise_above_all(jk)
                        else:
                            query = "SELECT SKU, product_name, company, Floor, Rack, quantity FROM Stock WHERE SKU LIKE %s"
                            myc.execute(query, (Beg + '%',))
                            t=myc.fetchall()
                            tB.insert(t)
                            insertFile(t[0])                        
                            messagebox.showinfo('Store Inventory', 'Record updated for picking')    
                            master.destroy()
                            raise_above_all(jk)
                            

                Amajor().mainloop()

            def removeData(self, tB):
                class Rmajor(tk.Toplevel):
                    def __init__(self):
                        tk.Toplevel.__init__(self)
                        self.title('Update Order')
                        center(self, '500x400')
                        self.config(bg=grey)
                        self._frame = None
                        self.switch_frame(RStartPage)                    

                    def switch_frame(self, frameclass):
                        new_frame = frameclass(self)
                        if self._frame is not None:
                            self._frame.destroy()
                        self._frame = new_frame
                        self._frame.pack()

                class RStartPage(tk.Frame):
                    def __init__(self, master):
                        tk.Frame.__init__(self, master)
                        self.pack(fill = tk.BOTH, expand = True)
                        tk.Label(self, text='Order for approval', justify='center', fg=grey, font=('Helvetica', 18, 'bold')).pack(pady = 50, side = tk.TOP, fill=tk.BOTH, expand=True)
                        tk.Label(self, text='Enter Order No', justify='center', fg=grey, font=pdfont).pack(side = tk.TOP, fill=tk.BOTH, expand=True)
                        self.var = tk.StringVar()
                        tk.Entry(self, textvariable=self.var, font=('Calibri', 16, 'normal'), fg=grey, relief='raised').pack(side = tk.TOP, fill=tk.BOTH, expand=True)
                        tk.Button(self, text='Submit', font=pdfont, width=10, height=15, command=lambda: self.submit(master), fg=grey, justify='center').pack(side = tk.BOTTOM, pady=90)

                    def submit(self, master):
                        No = self.var.get()
                        n = len(str(No))
                        z = 3-n
                        Beg = 'SKU'+z*'0'+str(No)
                        with open('Picking.csv', mode = 'r') as f:
                            fr = csv.reader(f)
                            temp = list(fr)
                            for data in temp: 
                                if data != []: 
                                    if data[0][0:6] == Beg:  
                                        tB.delete(temp.index(data))
                                        temp.remove(data)
                        temp = remove_items(temp, [])
                        with open('Picking.csv', mode = 'w') as f:
                            fw = csv.writer(f)
                            for row in temp:    fw.writerow(row)
                        refresh(tB)                       
                        messagebox.showinfo('Store Inventory', 'Record updated for picking')    
                        master.destroy()
                        raise_above_all(jk)                       
                        

                Rmajor().mainloop()

        jk = fPick()
        jk.mainloop()
        

    def RefillPage(tp):
        tp.destroy()
        tp.update()

        class fRefill(tk.Toplevel):
            def __init__(self):
                tk.Toplevel.__init__(self, bg=orange)
                self.title('Refill')
                tk.Label(self, text='Refill Orders', bg=orange, fg=white, font=('Georgia', 20, 'normal')).place(x=410, y=10)
                center(self, '1000x550')
                frame = tk.Frame(self, width=100, height=100)
                frame.place(y=50, relx=0, rely=0, relwidth=1, relheight=1)
                rB = pBox(frame)
                myc.execute("SELECT SKU, product_name, company, Floor, rack FROM Stock WHERE Status = 'Out of Stock'")
                rB.insert(myc.fetchall())

        jp = fRefill()
        jp.mainloop()

    tp = tk.Toplevel(root)
    tp.title('Picking/Refill')
    tp.config(width=250, height=250, bg=orange)
    center_main(tp)
    tk.Label(tp, text='Picking/Refill', bg=orange, fg=white, font=('Georgia', 18, 'normal')).place(x=50, y=20)
    tk.Button(tp, text='Picking', cursor='hand2', command=lambda: PickPage(tp), font=phfont).place(x=85, y=80)
    tk.Button(tp, text='Refill', cursor='hand2', command=lambda: RefillPage(tp), font=phfont).place(x=95, y=140)


