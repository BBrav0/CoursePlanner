import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from tkinter import *

# Create root window
root = Tk()

# Root window title and dimension
root.title("Welcome to GeekForGeeks")
root.geometry('350x200')  # Set geometry (width x height)

# Configure grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Add menu bar
menu = Menu(root)
item = Menu(menu, tearoff=0)  # `tearoff=0` prevents menu from being detachable
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# Add widgets
lbl = Label(root, text="Are you a Geek?", borderwidth=2, relief="solid")
lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")

txt = Entry(root, width=10, borderwidth=2, relief="solid")
txt.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Function to display user text when button is clicked
def clicked():
    res = "You wrote: " + txt.get()
    lbl.configure(text=res)

btn = Button(root, text="Click me", fg="red", command=clicked, borderwidth=2, relief="solid")
btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

# Execute Tkinter
root.mainloop()
