from tkinter import *
from tkinter import ttk

def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
# Function to display user text when button is clicked

def clicked():
    try:
        tem = txt.get()
        yea = int(tem)
        lbl.configure(text="Thank you, your course map is loading...")
    except ValueError:
        lbl.configure(text="Incorrect input. Please Try again")
    


# Create root window
root = Tk()

#TK_SILENCE_DEPRECATION = 1
# Root window title and dimension
root.title("Ben's Course Planner")
root.geometry('1280x720')  # Set geometry (width x height)



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
lbl = Label(root, text="Please enter your start year (e.g. '2022') and semester", borderwidth=2, relief="solid")
lbl.pack(side=TOP, padx=10, pady=10)

txt = Entry(root, width=10, borderwidth=2, relief="solid")
txt.pack(side=TOP, padx=10, pady=10)

sems = ["Fall","Summer","Spring"]

variable = StringVar(root)
variable.set(sems[0]) # default value

drp = OptionMenu(root, variable, *sems)
drp.pack(side=TOP, padx=10, pady=10)

btn = Button(root, text="Submit", fg="red", command=clicked, borderwidth=2, relief="solid")
btn.pack(side=TOP, padx=10, pady=10)




# Execute Tkinter
root.lift()
root.focus_force()

root.mainloop()
