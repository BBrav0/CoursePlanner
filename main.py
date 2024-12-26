from tkinter import *
from tkinter import ttk

# WINDOW CLEAR METHOD
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# MISC METHOD
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

# MISC METHOD
def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

# MISC METHOD
def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

# SUBMIT BUTTON ON MAIN PAGE METHOD
def clicked():
    try:
        year = int(txt.get())
        course_page(year)
    except ValueError:
        lbl.configure(text="Incorrect input. Please try again")

#
# START PAGE BUILD
#
def start_win():
    global lbl 
    lbl = Label(root, text="Please enter your start year (e.g. '2022') and semester", borderwidth=2, relief="solid")
    lbl.pack(side=TOP, padx=10, pady=10)

    global txt
    txt = Entry(root, width=10, borderwidth=2, relief="solid")
    txt.pack(side=TOP, padx=10, pady=10)

    sems = ["Fall","Summer","Spring"]

    global variable
    variable = StringVar(root)
    variable.set(sems[0])

    drp = OptionMenu(root, variable, *sems)
    drp.pack(side=TOP, padx=10, pady=10)

    btn = Button(root, text="Submit", fg="black", command=clicked, borderwidth=2, relief="solid")
    btn.pack(side=TOP, padx=10, pady=10)

# ADD COURSE BUTTON
def add():
    popup = Tk()
    popup.title("Add Course")
    popup.geometry('800x800')

    popup.lift()
    popup.focus_force()

    root.mainloop()

#
# COURSE PAGE BUILD
#
def course_page(year):
    st = str(variable.get()) +" "+str(year)
    clear_window()
    i = 11
    j = 0
    cur = str(variable.get())
    while (i>0):
        nex = Label(root, text=cur +" "+str(year), borderwidth=2, relief="solid")
        nex.place(x=j, y=0)

        btn = Button(root, text="+", fg="black", command=add, borderwidth=2, relief="solid")
        btn.place(x=j, y=30)

        if(cur == "Fall"):
            j+=210
            cur = "Spring"
            year+=1
        elif(cur == "Spring"):
            j+=225
            cur = "Summer"
        else:
            j+=240
            cur = "Fall"
        i-=1
        
#
# WINDOW SETUP
#
root = Tk()
root.title("Ben's Course Planner")
root.geometry('1280x720')  

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

menu = Menu(root)
item = Menu(menu, tearoff=0) 
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)


start_win()
root.lift()
root.focus_force()

root.mainloop()

