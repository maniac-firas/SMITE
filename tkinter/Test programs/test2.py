import tkinter as tk

root=tk.Tk()
root.title('test2')
root.geometry('400x400')
root.configure(bg='lightblue')

text=tk.Entry(root, width=45, bg='white')
text.pack(pady=10)
text.bind('<return>')

def text_updation(word):
	text.delete(0, tk.END)
	text.insert(0, word)

button_dict={}
words=['a', 'b', 'c', 'd']

for word in words:
	def action(x=word):
		return text_updation(x)
	button_dict[word] = tk.Button(root, text=word, width = 10, bg='green', cursor='star',command=action)
	button_dict[word].pack(pady=10)

root.mainloop()
