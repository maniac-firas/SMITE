import tkinter as tk

root=tk.Tk()
root.geometry('400x400')
root.title('test3')
root.configure(bg='lightcoral')


lbl = tk.Label(root, text='The switch is on', fg='black', bg='lightcoral', font=('Times New Roman', 18, 'bold'))
lbl.pack(pady=15)

is_on = True

c=tk.Canvas(root, height=100, width=200, bg='lightblue')
c.place(x=100, y=50)


def switch():
    global is_on

    if not(is_on):
        btn.config(image=on)
        lbl.config(text='The switch is on')
        is_on=True

    else:
        btn.config(image=off)
        lbl.config(text='The switch is off')
        is_on=False

on = tk.PhotoImage(file = 'Test programs/on.png')
off = tk.PhotoImage(file = 'Test programs/off.png')

btn = tk.Button(root, image=on, command=switch)
btn.pack(pady=20, padx=50)

root.mainloop()