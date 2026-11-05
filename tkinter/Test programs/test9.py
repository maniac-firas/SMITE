import tkinter as tk

def open_toplevel():
    # Create a new Toplevel window
    top = tk.Toplevel()
    top.title("Toplevel Window")
    
    # Add content to the Toplevel window
    label = tk.Label(top, text="This is a Toplevel window", font=("Arial", 14))
    label.pack(padx=20, pady=20)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Main Window")
    
    # Create a Frame inside the main window
    frame = tk.Frame(root, width=300, height=200)
    frame.pack_propagate(False)  # Prevent the frame from resizing to fit its children
    frame.pack(padx=20, pady=20)
    
    # Add a button to the Frame that opens the Toplevel window
    open_button = tk.Button(frame, text="Open Toplevel", command=open_toplevel)
    open_button.pack(pady=20)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
