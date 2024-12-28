from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy

class Course:
    def __init__(self, co, ti, cr, gr, se, ye):
        self.code = co
        self.title = ti
        self.credits = cr
        self.grade = gr
        self.sem = se
        self.year = ye
# MAKE CANVAS
def make_canvas():
   # Create A Main frame
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH,expand=1)
    sec = Frame(main_frame)
    sec.pack(fill=X,side=BOTTOM)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    x_scrollbar = ttk.Scrollbar(sec,orient=HORIZONTAL,command=my_canvas.xview)
    x_scrollbar.pack(side=BOTTOM,fill=X)
    my_canvas.configure(xscrollcommand=x_scrollbar.set)
    my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL))) 
    # Create Another Frame INSIDE the Canvas
    global canvas
    canvas = Frame(my_canvas)
    # Add that New Frame a Window In The Canvas
    my_canvas.create_window((0,0),window= canvas, anchor="nw")


# WINDOW CLEAR METHOD
def clear_window():
    for widget in root.winfo_children():
        if (isinstance(widget, Menu)):
            continue
        widget.destroy()

# START DRAG INFO
def drag_start_info(cod, tit):
    global dragged_code
    dragged_code = cod
    global dragged_title
    dragged_title = tit

# START DRAGGING
def drag_start(event, cod, tit):
    drag_start_info(cod, tit)
    widget = event.widget
    widget.lift()
    global drag_start_x
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    drag_start_x = widget.winfo_x()

# WHILE DRAGGING
def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

# DONE DRAGGING
def drag_stop(event):
    widget = event.widget
    x = widget.winfo_x()  # Final x position
    y = widget.winfo_y()  # Final y position
    x_offset = x-drag_start_x
    if (x_offset > 150 or x_offset < -150):
        mark_unsaved()
        i = int(x_offset/190)
        j = 0
        cours = Course(0,0,0,0,0,0)
        for c in courses:
            if c.code == dragged_code and c.title == dragged_title:
                cours = Course(c.code, c.title, c.credits, c.grade, c.sem, c.year)
                courses.remove(c)
                break
        if i>0:
            while not (j==i):
                temp = forward_one(cours.sem, cours.year)
                cours.sem = temp[0]
                cours.year = int(temp[1])
                j+=1
        elif i<0:
            while not (j==i):
                temp = back_one(cours.sem, cours.year)
                cours.sem = temp[0]
                cours.year = int(temp[1])
                j-=1
        courses.append(cours)
    refresh()
    
    #THRESHOLD SHOULD BE +150 X OR -150 X

# BACK ONE SEMESTER HELPER METHOD
def back_one(sem, year):
    n_sem = ""
    year = int(year)
    match sem:
        case "Fall":
            n_sem = "Summer"
        case "Summer":
            n_sem = "Spring"
        case "Spring":
            n_sem = "Fall"
            year-=1
    return [n_sem, str(year)]

# FORWARD ONE SEMESTER HELPER METHOD
def forward_one(sem, year):
    n_sem = ""
    year = int(year)
    match sem:
        case "Fall":
            n_sem = "Spring"
            year+=1
        case "Summer":
            n_sem = "Fall"
        case "Spring":
            n_sem = "Summer"
    return [n_sem, str(year)]

# SUBMIT BUTTON ON MAIN PAGE METHOD
def start_coursepage():
    global startyear
    global startsem
    startsem = "Fall"
    startyear = 0
    try:
        startyear = int(txt.get())
        startsem = variable.get()
        root.title("Ben's Course Planner (Not Saved)")
        mark_unsaved()
        course_page(startyear, startsem)
    except ValueError:
        lbl.configure(text="Incorrect input. Please try again")

#
# START PAGE BUILD
#
def start_win():
    clear_window()

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

    btn = Button(root, text="Submit", fg="black", command=start_coursepage, borderwidth=2, relief="solid")
    btn.pack(side=TOP, padx=10, pady=10)

# ADD COURSE BUTTON
def add(xx, yy, sem ,yer):
    global popup
    popup = Toplevel(root)
    popup.title("Add Course")
    popup.geometry('600x400')

    popup.lift()
    popup.focus_force()

    nex = Label(popup, text="Course Code", borderwidth=2, relief="solid")
    nex.place(x=0, y=0)

    nex = Label(popup, text="Course Title", borderwidth=2, relief="solid")
    nex.place(x=0, y=50)

    nex = Label(popup, text="Credits", borderwidth=2, relief="solid")
    nex.place(x=0, y=100)

    nex = Label(popup, text="Grade", borderwidth=2, relief="solid")
    nex.place(x=0, y=150)

    grades = ["","A","A-","B+","B","B-","C+","C","C-","F"]

    variable = StringVar(root)
    variable.set(grades[0])

    grade = OptionMenu(popup, variable, *grades)
    grade.place(x=100, y=150)

    code = Entry(popup, width=15, borderwidth=2, relief="solid")
    code.place(x=100, y=0)

    title = Entry(popup, width=20, borderwidth=2, relief="solid")
    title.place(x=100, y=50)

    cred = Entry(popup, width=5, borderwidth=2, relief="solid")
    cred.place(x=100, y=100)

    btn = Button(popup, text="Add", fg="black", command=lambda: (mark_unsaved(), added(xx, yy, code.get(), title.get(), cred.get(), variable.get(), sem, yer)), borderwidth=2, relief="solid")
    btn.pack(side=BOTTOM, pady=50)
    button_references.append(btn)

# COURSE ADDED BUTTON
def added(xx, yy, co, ti, cr, gr, se, ye):

    # Add course object to the list
    courses.append(Course(co, ti, cr, gr, se, ye))
    # Create the course frame
    frame = Frame(canvas, borderwidth=3, relief="raised", width=180, height=70, bg="lightgrey")
    frame.place(x=xx + 10, y=yy)

    # Display course details
    code = Label(frame, text=co, fg="black", font=("Helvetica", 12, "bold"), bg="lightgrey")
    code.place(x=5, y=5)

    title = Label(frame, text=ti, fg="black", font=("Helvetica", 14), bg="lightgrey", wraplength=150)
    title.place(x=5, y=20)

    credits = Label(frame, text=f"{cr} credits", fg="black", font=("Helvetica", 12, "bold"), bg="lightgrey")
    credits.place(x=120, y=40)

    grade = Label(frame, text=gr, fg="black", font=("Helvetica", 12, "bold"), bg="lightgrey")
    grade.place(x=150, y=5)

    root.update_idletasks()
    for b in button_references:
        try:
            if b.winfo_x()==70+xx:
                b.destroy()
        except TclError:
            pass
    btn = Button(canvas, text="+", fg="black", 
                     command=lambda: (add(xx, yy + 70, se, ye)), borderwidth=2, relief="solid")

    

    remov = Canvas(frame, width=14, height=15, bg="white", highlightthickness=2)
    remov.place(x=151, y=23)
    remov.create_text(9, 9, text="X", fill="red", font=("Helvetica", 15, "bold"), anchor="center")
    remov.bind("<Button-1>", lambda event: remove_confirm(code.cget("text"), title.cget("text")))

    frame.bind("<Button-1>", lambda event: drag_start(event, co, ti))
    frame.bind("<B1-Motion>", drag_motion)
    frame.bind("<ButtonRelease-1>", drag_stop)
    frame_references.append(frame)
    if yy < 650: 
        btn.place(x=xx + 70, y=yy + 100)

    button_references.append(btn)
    try:
        popup.destroy()
    except NameError:
        pass

# REMOVE POPUP CONFIRMATION
def remove_confirm(c, t):
    global confirm

    confirm = Toplevel(root)
    confirm.title("Remove Course")
    confirm.geometry('400x200')

    nex = Label(confirm, text="Remove Course?",font=("Helvetica", 20, "bold"), borderwidth=0, relief="solid",fg="red")
    nex.pack(side=TOP, pady=10)

    nex = Label(confirm, text=c,font=("Helvetica", 14, "bold"), borderwidth=0, relief="solid",fg="black")
    nex.pack(side=TOP, pady=10)

    nex = Label(confirm, text=t,font=("Helvetica", 15), borderwidth=0, relief="solid",fg="black")
    nex.pack(side=TOP, pady=10)

    btn = Button(confirm, text="OK", command=lambda: remove(c, t), borderwidth=2, relief="solid")
    btn.pack(side=TOP, pady=10)

    confirm.lift()
    confirm.focus_force()

# MARK UNSAVED
def mark_unsaved():
    if not (root.wm_title()[-1] == "*"):
        root.title(root.wm_title()+"*")

# REMOVE
def remove(c ,t):
    confirm.destroy()
    i = 0
    seme = ""
    yea = 0
    mark_unsaved()
    while i < len(courses):
        if courses[i].code == c and courses[i].title == t:
            seme = courses[i].sem
            yea = courses[i].year
            courses.pop(i)
            break
        i += 1
    refresh()

# REFRESH COURSE PAGE    
def refresh():
    clear_window()
    make_canvas()
    course_page(startyear, startsem)
    temp = copy.deepcopy(courses)
    courses.clear()
    frame_references.clear()
    for cur in temp:
        sSem = startsem
        cSe = cur.sem
        cYr = cur.year
        sYr=startyear
        cCo = cur.code
        cTi = cur.title
        cCr = cur.credits
        cGr = cur.grade

        match startsem:
            case "Spring":
                curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr) *year_offset)
            case "Summer":
                match cSe:
                    case "Summer":
                        curx=semester_offsets.get((sSem, cSe) , 0)+(cYr-sYr)*year_offset
                    case "Fall":
                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)*year_offset)
                    case "Spring":
                        curx=semester_offsets.get((sSem, cSe) , 0)+(((cYr-sYr)-1)*year_offset)
            case "Fall":
                match cSe:
                    case "Summer":
                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)-1)*year_offset
                    case "Fall":
                        curx=semester_offsets.get((sSem, cSe) , 0)+(cYr-sYr)*year_offset
                    case "Spring":
                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)-1)*year_offset
        existing_courses = [c for c in courses if c.sem == cSe and c.year == cYr]
        cury = 40 + len(existing_courses) * 70
        added(curx, cury, cCo, cTi, cCr, cGr, cSe, cYr)

# SAVE METHOD
def save():
    with open(file_path, 'w') as file:
        root.title("Ben's Course Planner ("+file.name+")")
        file.write(startsem+" "+str(startyear)+"\n")
        for c in courses:
            file.write("code="+c.code+"\n")
            file.write("title="+c.title+"\n")
            file.write("credits="+c.credits+"\n")
            file.write("grade="+c.grade+"\n")
            file.write("semester="+c.sem+"\n")
            file.write("year="+str(c.year)+"\n")

# SAVE AS METHOD
def save_as():
    global file_path
    item.entryconfig('Save', state="normal")
    file_path = filedialog.asksaveasfilename(
    title="Save As",
    defaultextension=".txt",  # Set default file extension
    filetypes=[("Text Files", "*.txt")],  # File type filters
    )

# Check if a file path was selected
    if file_path:

        # Save file operation
        with open(file_path, 'w') as file:
            root.title("Ben's Course Planner ("+file.name+")")
            file.write(startsem+" "+str(startyear)+"\n")
            for c in courses:
                file.write("code="+c.code+"\n")
                file.write("title="+c.title+"\n")
                file.write("credits="+c.credits+"\n")
                file.write("grade="+c.grade+"\n")
                file.write("semester="+c.sem+"\n")
                file.write("year="+str(c.year)+"\n")
    root.focus_force()

# OPEN FILE METHOD
def open_file():
    global file_path
    item.entryconfig('Save', state="normal")
    file_path = filedialog.askopenfilename(
        title="Open",
        defaultextension=".txt",  # Set default file extension
        filetypes=[("Text Files", "*.txt")],  # File type filters
    )

    if file_path:
        with open(file_path, "r") as file:
            courses.clear()
            clear_window()
            make_canvas()
            root.title("Ben's Course Planner ("+file.name+")")
            curx = 0
            cury = 40
            l = 0
            sSem = "Fall"
            sYr = 0
            cCo = ""
            cTi = ""
            cCr = 0
            cGr = "A"
            cSe = "Fall"
            cYr = 0
            global startsem
            global startyear
            for line in file:
                match l:
                    case 0:
                        cur = line.split()
                        sYr = int(cur[1])
                        sSem = cur[0]
                        startyear = sYr
                        startsem = sSem
                        course_page(sYr, sSem)
                        l += 1
                    case 1:
                        cCo = line.split('=')[1].strip()
                        l += 1
                    case 2:
                        cTi = line.split('=')[1].strip()
                        l += 1
                    case 3:
                        cCr = line.split('=')[1].strip()
                        l += 1
                    case 4:
                        cGr = line.split('=')[1].strip()
                        l += 1
                    case 5:
                        cSe = line.split('=')[1].strip()
                        l += 1
                    case 6:
                        cYr = line.split('=')[1].strip()
                        if len(cYr) == 2:  # Two-digit year fix
                            cYr = "20" + cYr  # Convert "23" to "2023"
                        cYr = int(cYr)

                        # Adjust curx based on semester and year
                        curx = 0
                        cury = 40  # Fixed y position

                        match sSem:
                            case "Spring":
                                curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr) *year_offset)
                            case "Summer":
                                match cSe:
                                    case "Summer":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+(cYr-sYr)*year_offset
                                    case "Fall":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)*year_offset)
                                    case "Spring":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+(((cYr-sYr)-1)*year_offset)
                            case "Fall":
                                match cSe:
                                    case "Summer":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)-1)*year_offset
                                    case "Fall":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+(cYr-sYr)*year_offset
                                    case "Spring":
                                        curx=semester_offsets.get((sSem, cSe) , 0)+((cYr-sYr)-1)*year_offset

                        existing_courses = [c for c in courses if c.sem == cSe and c.year == cYr]
                        cury =40 + len(existing_courses) * 70
                        added(curx, cury, cCo, cTi, cCr, cGr, cSe, cYr)
                        l = 1  # Reset line count after processing the course

    root.focus_force()

#
# COURSE PAGE BUILD
#
def course_page(year, sem):
    st = str(sem) + " " + str(year)
    clear_window()
    i = 11
    j = 0
    cur = str(sem)
    make_canvas()
    while i > 0:
        nex = Label(canvas, text=cur + " " + str(year), font=("Helvetica", 20), borderwidth=0, relief="solid")
        nex.grid(column=j, row=0, padx=10, pady=0)  # Add padding for spacing

        frame = Frame(canvas, borderwidth=5, relief="sunken", width=200, height=750)
        frame.grid(column=j, row=1, padx=10, pady=10)  # Add padding for spacing
        frame.pack_propagate(False)

        btn = Button(frame, text="+", fg="black", command=lambda x=j, s=cur, y=year: add(x, 40, s, y), borderwidth=2, relief="solid")
        btn.pack(side=TOP,pady=10)  # Add padding for spacing
        button_references.append(btn)

        # Update semester and year
        if cur == "Fall":
            cur = "Spring"
            year += 1
        elif cur == "Spring":
            cur = "Summer"
        else:
            cur = "Fall"
        
        i -= 1
        j += 1  # Keep incrementing the column number
    pass

        
#
# WINDOW SETUP
#

global root
root = Tk()
root.title("Ben's Course Planner")
root.geometry('1920x1080')  

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

menu = Menu(root)
global item
item = Menu(menu, tearoff=0) 
item.add_command(label='New', command=start_win)
item.add_command(label='Save', command=save, state="disabled")
item.add_command(label='Save as', command=save_as)
item.add_command(label='Open', command=open_file)
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# BIG GLOBALS
global canvas
make_canvas()

global courses
courses = []

global button_references
button_references = []

global frame_references
frame_references = []

global semester_offsets
semester_offsets = {
    ("Fall", "Fall"): 0,
     ("Fall", "Spring"): 210,
     ("Fall", "Summer"): 210 + 210,
     ("Spring", "Fall"): 210 + 210,
  ("Spring", "Spring"): 0,
    ("Spring", "Summer"): 210,
     ("Summer", "Fall"): 210,
     ("Summer", "Spring"): 210 + 210,
    ("Summer", "Summer"): 0
                        }

global year_offset
year_offset = 210+210+210

start_win()
root.lift()
root.focus_force()

root.mainloop()

