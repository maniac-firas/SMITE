import tkinter as tk
from tkinter import messagebox
import csv

def center(window, dimensions):
    window.update_idletasks()
    di = dimensions.split('x')
    width, height = int(di[0]), int(di[1])
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
def change(data):    
    with open('Stock.csv', 'w') as f:
        fw = csv.writer(f)
        fw.writerows(data)
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
def OutStock(mydb, myc):
    myc.execute('Update Stock set Quantity = 0 where Status = "Out of Stock"')
    mydb.commit()
def dCheck(type=False, Comp = False):
    if type:    
        with open('Type Codes.txt', 'r') as f:
            fr = f.read().split('\n')
            for i in range(len(fr)):        fr[i] = fr[i][5::].title()
    if Comp:  
        with open('Company Codes.txt', 'r') as f:
            fr = f.read().split('\n')
            for i in range(len(fr)):        
                fr[i] = fr[i][7::]
                if fr[i] != 'IKEA': fr[i]=fr[i].title()
    return fr
def checkin(inputs):
        cond, cno = False, ''
        ents=[]
        for t in inputs:    
            if t.isspace() or t == '':  
                messagebox.showerror("Store Inventory", "Incorrect Input")
                return cond
            else:   ents.append(t)

        if ents[3].isnumeric():    cno = (chr(int(ents[3]) + 96)).upper()

        if all(char.isalpha() or char.isspace() for char in ents[0]) == False:                                                      messagebox.showerror("Incorrect Input", 'Product Name should not contain special symbols.')
        elif ents[1] not in dCheck(type=True):                                                                                      messagebox.showerror("Incorrect Input", 'Entered Type does not exist')
        elif ents[2] not in dCheck(Comp=True):                                                                                      messagebox.showerror("Incorrect Input", 'Entered Company does not exist')
        elif (not(ents[3].isnumeric())) and (len(ents[3]) != 1):                                                                    messagebox.showerror("Incorrect Input", 'Floor is a one digit number')
        elif len(ents[4]) != 2:                                                                                                     messagebox.showerror("Incorrect Input", 'Rack must contain a number and letter')
        elif (ents[4][0] != cno) or (ents[4][1].isnumeric() == False):                                                              messagebox.showerror("Incorrect Input", 'Rack must contain Floor letter code and Rack Number')
        elif not(ents[5].isnumeric() and ents[6].isnumeric() and ents[8].isnumeric()):                                              messagebox.showerror("Incorrect Input", 'MRP, Quantity or Delivery must be a number')
        elif ((ents[7][0:4] + ents[7][5:7] + ents[7][8::]).isnumeric() == False) or (ents[7][4] != '-') or (ents[7][7] != '-'):     messagebox.showerror("Incorrect Input", 'DOM is not in date format')
        elif ents[9] not in ['In Stock', 'Out of Stock', 'Out Of Stock']:                                                           messagebox.showerror("Incorrect Input", 'Status should be In Stock/Out of Stock')
        else:   cond = True
        return cond

dfont = ('Calibri', 22, 'normal')
sfont = ('Helvetica', 14, 'normal')
grey, orange, white = '#36454f', '#fb8b24', '#faf0e6'

def displayDatabase(root, mydb):
    try:
        myc = mydb.cursor()

        class Box():
            def __init__(self):
                self.scroll_bar = tk.Scrollbar(root, orient = tk.VERTICAL)
                self.scroll_bar.pack(side = tk.RIGHT, fill = 'y')
                self.Tb = tk.Text(root, width = 500, height = 500, bg=white, yscrollcommand=self.scroll_bar.set, wrap='none', font = ('Helvetica', 14, 'normal'))
                
            def insert(self, data):
                table = []
                slot1 = 0
                for row in data:
                    slot2,n = 0,0
                    table.append(list())
                    for t in row:
                        table[slot1].append(t)
                        if slot2 in [2, 3]:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'\t\t')
                        elif slot2 == 4:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'   ')
                        elif slot2 == 8:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'\t\t')
                        elif slot2 in [6, 7, 9]:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'\t')
                        elif slot2 not in [0, 1]:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'\t')
                        else:
                            self.Tb.insert(tk.END, str(table[slot1][slot2])+'\t\t\t')
                        slot2+=1
                        n+=1
                    self.Tb.insert(tk.END, '\n')
                    slot1+=1
                self.Tb.pack(side=tk.LEFT, fill = tk.BOTH, ipady=100)
                self.scroll_bar.config(command=self.Tb.yview)

            def delete(self):
                self.Tb.delete(1.0,tk.END)

        def printdata(filter):
            OutStock(mydb, myc)
            if filter in ['MRP', 'DOM']:
                query = "select * from stock order by "+filter+" desc"
            else:
                query = "select * from stock order by "+filter
            myc.execute(query)
            data = myc.fetchall()
            Tb.delete()
            Tb.insert(data)

        #Heading
        head = tk.Label(root, text='', font=dfont, height=3, width=480, bg=orange, bd=5)
        head.pack()

        label1 = tk.Label(root, text="Products",fg=white, bg=orange, font=('Georgia', 21, 'normal'))
        label1.place(relx=0.5, y=30, anchor=tk.CENTER)

        heading = ['SKU', 'Product Name','Type', 'Company', 'Floor', 'Rack', 'MRP', 'Qty', 'DOM', 'Duration', 'Delivery', 'Status']
        lbls = []
        for i in range(len(heading)):   lbls.append(tk.Button(root, text=heading[i], fg=white, bg=orange, bd = 0, cursor="hand2", font=dfont))

        def s1():
            lbls[0].place(x=55, y=55)
            lbls[1].place(x=250, y=55)
            lbls[2].place(x=520, y=55)
            lbls[3].place(x=695, y=55)
            lbls[4].place(x=850, y=55)
            lbls[6].place(x=960, y=55)
            lbls[7].place(x=1040, y=55)
            lbls[8].place(x=1150, y=55)
            lbls[10].place(x=1280, y=55)
            lbls[11].place(x=1400, y=55)

            lbls[4].config(text='Location')
        s1()
        Tb = Box()
        def s2():
            lbls[0].config(command = lambda:printdata(filter = 'SKU'))
            lbls[1].config(command = lambda:printdata(filter = 'product_name'))
            lbls[2].config(command = lambda:printdata(filter = 'Type'))
            lbls[3].config(command = lambda:printdata(filter = 'Company'))
            lbls[4].config(command = lambda:printdata(filter = 'Rack'))
            lbls[6].config(command = lambda:printdata(filter = 'MRP'))
            lbls[7].config(command = lambda:printdata(filter = 'Quantity'))
            lbls[8].config(command = lambda:printdata(filter = 'DOM'))
            lbls[10].config(command = lambda:printdata(filter = 'Delivery'))
            lbls[11].config(command = lambda:printdata(filter = 'Status'))
        s2()

        #Data Abstractors
        OutStock(mydb, myc)
        query = "select * from stock order by SKU"
        myc.execute(query)
        data = myc.fetchall()
        Tb.insert(data)

        tk.Button(root, text='UPDATE', cursor='hand2', command=lambda:  fUpdate(mydb)).place(x=1370, y=20)
        tk.Button(root, text='DELETE', cursor='hand2', command=lambda:  fDelete(mydb)).place(x=1440, y=20)
    except: pass

def fUpdate(mydb):
    myc = mydb.cursor()
    class major(tk.Toplevel):
        def __init__(self):
            tk.Toplevel.__init__(self)
            self.title('Update Order')
            center(self, '500x480')
            self.config(bg=grey)
            self._frame = None
            self.switch_frame(StartPage)

        def switch_frame(self, frameclass):
            new_frame = frameclass(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()

    # Label Writers
    class lblent():

        def __init__(self, master, content, default, fac):
            ypos = 60+30*fac 
            self.lbl = tk.Label(master, text=content, font=sfont).place(x=80, y=ypos)
            self.entvar = tk.StringVar()
            self.entvar.set(default)
            self.ent = tk.Entry(master, textvariable=self.entvar, font=sfont).place(x=280, y=ypos, width=150)

        def fetch(self):
            temp = self.entvar.get()
            return temp
    
    class StartPage(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            self.pack(fill = tk.BOTH, expand = True)
            tk.Label(self, text='Update Order', justify='center', fg=grey, font=('Helvetica', 18, 'bold')).pack(pady = 50, side = tk.TOP, fill=tk.BOTH, expand=True)
            tk.Label(self, text='Enter Order No', justify='center', fg=grey, font=dfont).pack(side = tk.TOP, fill=tk.BOTH, expand=True)
            self.var = tk.StringVar()
            tk.Entry(self, textvariable=self.var, font=('Calibri', 16, 'normal'), fg=grey, relief='raised').pack(side = tk.TOP, fill=tk.BOTH, expand=True)
            tk.Button(self, text='Submit', font=dfont, command=lambda: self.submit(master), fg=grey, justify='center').pack(side = tk.BOTTOM, pady=90)

        def submit(self, master):
            recs, nrec = [], 0
            myc.execute('select SKU from stock ORDER BY SKU')
            temp=myc.fetchall()
            for i in range(len(temp)): 
                recs.append(temp[i][0])
                recs[i] = int(recs[i][3:6])
                nrec = recs[i]
            if self.var.get() == '':    pass
            elif int(self.var.get()) > nrec or int(self.var.get()) not in recs:
                n = len(self.var.get())
                z = 3-n
                sk = 'SKU'+z*'0'+self.var.get()
                messagebox.showerror('Store Inventory', sk[0:len(sk)]+' does not exist') 
                jk.destroy()       
            else:
                varget(self.var.get())
                master.switch_frame(UpdatePage)
    # Frameworkers
    head = ['product_name','Type', 'Company', 'Floor', 'Rack', 'MRP', 'Quantity', 'DOM', 'Delivery', 'Status']
    # Functioners
    def varget(var):
        global OrderNo
        OrderNo = var
    def fetch(No):
        n = len(str(No))
        z = 3 - n
        beginningOfString = 'SKU' + z * '0' + str(No)
        query = "SELECT * FROM Stock WHERE SKU LIKE %s"
        myc.execute(query, (beginningOfString + '%',))
        temp = myc.fetchall()          
        return list(temp[0]) 
    def codegiver(No:int, Type:str, Company:str, Floor:str, Rack:str):
        Tcode, Ccode = '',''
        with open('Type Codes.txt', 'r') as f:
            for line in f.readlines():  
                data = line.split(' - ')
                data[1] = data[1][0:len(data[1])-1]   
                if data[1] == Type.upper():
                    Tcode = data[0]

        with open('Company Codes.txt', 'r') as f:
            for line in f.readlines():  
                data = line.split(' - ')
                data[1] = data[1][0:len(data[1])-1]  
                if data[1] == Company.upper():
                    Ccode = data[0]
        
        n = len(str(No))
        z = 3-n
        return 'SKU'+z*'0'+str(No)+'-'+Tcode+'-'+Ccode+'-'+Floor+Rack
    def pSKU(master, content, default, ypos):
        tk.Label(master, text=content, font=sfont).place(x=80, y=ypos)
        entvar = tk.StringVar()
        entvar.set(default)
        tk.Entry(master, textvariable=entvar, font=sfont, state=tk.DISABLED).place(x=280, y=ypos, width=150)

    class UpdatePage(tk.Frame): 
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            data = fetch(OrderNo)
            OgSKU=data[0]
            data = data[1::]
            self.ents = []
            self.pack(fill = tk.BOTH, expand = True)
            tk.Label(self, text='Update Information', font=('Helvetica', 16, 'bold')).place(x=157, y=20)
            pSKU(master, 'SKU', OgSKU, 60)
            for i in range(len(head)): self.ents.append(lblent(master, head[i], data[i], i+1))
            tk.Button(self, text='Submit', command = lambda:  self.accept(OgSKU), font=('Helvetica', 17, 'normal'), fg=grey, justify='center').pack(side = tk.BOTTOM, pady=15)

        def accept(self, OgSKU):
            t = []
            for i in range(len(head)):
                temp = self.ents[i].fetch()
                t.append(temp)
            cond = checkin(t)
            if cond:
                SKU = codegiver(OrderNo, t[1], t[2], t[3], t[4])
                t.insert(0, SKU)
                t=tuple(t)
                myc.execute('DELETE from Stock where SKU = %s', (OgSKU,))
                mydb.commit()
                myc.execute("insert into stock values "+str(t))
                mydb.commit() 
                OutStock(mydb, myc)           
                messagebox.showinfo('Product Updated Successfully')
                jk.destroy()
                jk.update()
                myc.execute('Select * from Stock')
                change(myc.fetchall())
            else:
                raise_above_all(jk)
    jk = major()
    jk.mainloop()

def fDelete(mydb):
    myc = mydb.cursor()

    class deletePage(tk.Toplevel):
        def __init__(self):
            tk.Toplevel.__init__(self)
            self.title('Delete Order')
            center(self, '500x480')
            tk.Label(self, text='Delete Order', justify='center', fg=grey, font=('Helvetica', 18, 'bold')).pack(pady = 50, side = tk.TOP, fill=tk.BOTH, expand=True)
            tk.Label(self, text='Enter Order No', justify='center', fg=grey, font=dfont).pack(side = tk.TOP, fill=tk.BOTH, expand=True)
            self.var = tk.StringVar()
            tk.Entry(self, textvariable=self.var, font=('Calibri', 16, 'normal'), fg=grey, relief='raised').pack(side = tk.TOP, fill=tk.BOTH, expand=True)
            tk.Button(self, text='Submit', font=dfont, command= self.submit, fg=grey, justify='center').pack(side = tk.BOTTOM, pady=90)

        def submit(self):
            No = self.var.get()
            n = len(str(No))
            z = 3 - n
            beginningOfString = 'SKU' + z * '0' + str(No)
            query = 'DELETE from STOCK where SKU LIKE %s'
            myc.execute(query, (beginningOfString + '%',))
            mydb.commit()
            messagebox.showinfo('Store Inventory', 'Order Deleted.')
            ko.destroy()
            ko.update()
            myc.execute('Select * from Stock')
            change(myc.fetchall())

    ko = deletePage()
    ko.mainloop()

