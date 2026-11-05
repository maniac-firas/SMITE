import tkinter as tk
from random import choice

root=tk.Tk()
root.geometry('400x400')
root.title('test3')
root.configure(bg='lightcoral')

lbl = tk.Label(root, text='Image Swapper', bg='lightcoral', font=('Calibri', 20))
lbl.pack(pady=20)

bitmaps = ['error', 'gray75', 'gray50', 'gray25', 'gray12', 'hourglass', 'info', 'questhead', 'question', 'warning']

for bit in bitmaps:
    btn = tk.Button(root, relief='raised', bitmap=bit, width=50, height=50)
    btn.pack(pady=10)

root.mainloop()

