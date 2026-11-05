import tkinter as tk
import mysql.connector as mys
from tkinter import messagebox
import csv

#Program Starters
dfont = ('Helvetica', 15, 'normal')
ddfont = ('Calibri', 22, 'normal')
dsfont = ('Helvetica', 14, 'normal')
pdfont = ('Helvetica', 17, 'normal')
phfont = ('Helvetica', 14, 'normal')
grey, orange, white = '#36454f', '#fb8b24', '#faf0e6'
mydb, myc = None, None

#Functions
def center(window, dimensions):
    window.update_idletasks()
    di = dimensions.split('x')
    width, height = int(di[0]), int(di[1])
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
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
def change(myc):
    myc.execute('Select * from Stock')
    data = myc.fetchall()
    with open('Stock.csv', 'w') as f:
        fw = csv.writer(f)
        fw.writerows(data)
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
def remove_items(list, item):  
    res = [i for i in list if i != item] 
    return res
def insertFile(Data): 
    with open('Picking.csv', 'a', newline='\n') as f:
        fw = csv.writer(f)
        fw.writerow(Data)
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

#For Pick/Refill
pslot1, ptable, phead = 0, [], ['SKU', 'Product Name', 'Company', 'Floor', 'Rack', 'Quantity']
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

#Creating table
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

#Windows
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
        head = tk.Label(root, text='', font=ddfont, height=3, width=480, bg=orange, bd=5)
        head.pack()

        label1 = tk.Label(root, text="Products",fg=white, bg=orange, font=('Georgia', 21, 'normal'))
        label1.place(relx=0.5, y=30, anchor=tk.CENTER)

        heading = ['SKU', 'Product Name','Type', 'Company', 'Floor', 'Rack', 'MRP', 'Qty', 'DOM', 'Duration', 'Delivery', 'Status']
        lbls = []
        for i in range(len(heading)):   lbls.append(tk.Button(root, text=heading[i], fg=white, bg=orange, bd = 0, cursor="hand2", font=ddfont))

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

    class lblent():

        def __init__(self, master, content, default, fac):
            ypos = 60+30*fac 
            self.lbl = tk.Label(master, text=content, font=dsfont).place(x=80, y=ypos)
            self.entvar = tk.StringVar()
            self.entvar.set(default)
            self.ent = tk.Entry(master, textvariable=self.entvar, font=dsfont).place(x=280, y=ypos, width=150)

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
        tk.Label(master, text=content, font=dsfont).place(x=80, y=ypos)
        entvar = tk.StringVar()
        entvar.set(default)
        tk.Entry(master, textvariable=entvar, font=dsfont, state=tk.DISABLED).place(x=280, y=ypos, width=150)

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

def fEnter(root, mydb):
    dfont = ('Helvetica', 17, 'normal')
    grey, orange, white = '#36454f', '#fb8b24', '#faf0e6'
    myc = mydb.cursor()

    #Entrees
    class Entrees(tk.Frame):
        ents = []
        def __init__(self, parent):
            self.frame = tk.Frame(parent, bg=white, height=700, width=1000).pack()
            tk.Canvas(root, bg=orange, height=150, width=1000).place(x=500, y=0, anchor=tk.CENTER)
            tk.Label(root, text = "Enter Product Information", fg='white', bg=orange, font=('Georgia', 20, 'normal')).place(x=520, y=40, anchor=tk.CENTER)            

        def create(self, content, xstart, ypos):
            self.lbl = tk.Label(self.frame, text=content, bg=white, font = dfont)
            self.var = tk.StringVar()
            Entrees.ents.append(self.var)
            self.ent = tk.Entry(self.frame, textvariable=self.var, font=dfont)
            l, e = xstart, xstart+230
            self.lbl.place(x=l, y=ypos)
            self.ent.place(x=e, y=ypos)
            return self.var

        def sbtn(self, content):
            self.sbtn = tk.Button(self.frame, text=content, command = submit, font=dfont)
            self.sbtn.place(x=500, y=670, anchor=tk.CENTER)
            root.bind("<Return>", submit)      

    #Frame
    Efr = Entrees(root)
    ents, fac = [], 0
    heading = ['Product Name','Type', 'Company', 'Floor', 'Rack', 'MRP', 'Quantity', 'DOM(YYYY-MM-DD)', 'Delivery(in days)', 'Status']
    for head in heading:
        ents.append(Efr.create(head, 270, 90+50*fac))
        fac+=1

    #SKU Creator
    def codegiver(Type:str, Company:str, Floor:str, Rack:str):
        Tcode, Ccode = '',''
        myc.execute('select SKU from stock ORDER BY SKU DESC LIMIT 1')
        No = int(myc.fetchall()[0][0][3:6]) + 1

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
    
    #Check Input
    def checkin(agents):
        cond, cno = False, ''
        ents=[]
        for agent in agents:    
            if agent.get().isspace() or agent.get() == '':  
                messagebox.showerror("Store Inventory", "Incorrect Input")
                return cond
            else:   ents.append(agent.get())

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

    #Submit Function
    def submit(event=None):
        dat = []
        cond = checkin(ents)

        if cond:
            for ent in ents:       
                dat.append(str(ent.get()))
                ent.set("")
            
            SKU = codegiver(dat[1], dat[2], dat[3], dat[4])
            dat.insert(0, SKU)
            dat = str(tuple(dat))

            q = "insert into stock values "+str(dat)
            myc.execute(q)
            mydb.commit()
            messagebox.showinfo("Store Inventory", "Record Inserted Successfully")
            change(myc)            

    Efr.sbtn("Submit")

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


#Main Screen
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
        center_main(self)
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

