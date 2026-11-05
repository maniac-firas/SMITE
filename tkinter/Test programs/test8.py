import tkinter as tk
root = tk.Tk()
root.geometry('250x150')
tk.Label(root, text='root window').pack(pady=20)

def open():
    t1 = tk.Toplevel()  
    t1.geometry('250x150+1-0')
    t1.title('Window 1')
    tk.Label(t1, text='new window').pack(pady=20)

tk.Button(root, text='New Window', command=open).pack(pady=20)

tk.mainloop()