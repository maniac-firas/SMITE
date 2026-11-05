import tkinter as tk
from tkinter import messagebox
import csv

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