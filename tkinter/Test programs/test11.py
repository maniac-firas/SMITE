import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Text Box with Scrollbar in 1/4th Screen")
root.geometry("400x400")  # Size of the window

# Create a frame for the Text widget and Scrollbar
frame = tk.Frame(root, width=100, height=100)
frame.place(relx=0, rely=0, relwidth=0.25, relheight=1)  # 1/4th of the screen width, full height

# Create the Text widget (text box)
text_box = tk.Text(frame, wrap=tk.WORD, height=15, width=25)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar widget linked to the Text widget
scrollbar = tk.Scrollbar(frame, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Connect the scrollbar to the text box
text_box.config(yscrollcommand=scrollbar.set)

# Start the Tkinter main loop
root.mainloop()
