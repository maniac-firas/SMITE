import tkinter as tk
import mysql.connector as mys


#Program Starters
mydb = mys.connect(host='localhost', user='root', passwd = '', database='Store')
myc = mydb.cursor()

root = tk.Tk()
root.title('Scrollbar')
root.geometry('768x460')
root.config(bg='white')

#Scrollbar
scroll_bar = tk.Scrollbar(root, orient=tk.VERTICAL)
scroll_bar.pack(side = tk.RIGHT, fill = 'y')

TBox = tk.Text(root,  height = 500,  width = 500, yscrollcommand = scroll_bar.set, wrap = "none", font=('Calibri', 22, 'normal'))
TBox = tk.Text(root,  height = 500,  width = 500, yscrollcommand = scroll_bar.set, wrap = "none", font=('Calibri', 22, 'normal'))

for i in range(100):
    TBox.insert(tk.END, str(i))
    TBox.insert(tk.END, 3*'\t'+str(i)+'\n')
    

TBox.pack(side=tk.LEFT, fill = tk.BOTH)
scroll_bar.config(command=TBox.yview)

root.mainloop()