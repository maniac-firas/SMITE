import tkinter as tk
from random import randint

root=tk.Tk()
root.title('test2')
root.geometry('400x400')
root.configure(bg='lightblue')

def randomclick():
             x=randint(50, 350)
             y=randint(50, 350)
             btn.place(x=x, y=y)

btn = tk.Button(root, text="Click Me!", cursor = 'hand2', bg='yellowgreen' , command=randomclick)
btn.config(width=15, height=6)
btn.pack()

root.mainloop()
