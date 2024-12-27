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

# WINDOW CLEAR METHOD
def clear_window():
    for widget in root.winfo_children():
        if (isinstance(widget, Menu)):
            continue
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
    global startyear
    global startsem
    startsem = "Fall"
    year = 0
    try:
        year = int(txt.get())
        startsem = variable.get()
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

    btn = Button(root, text="Submit", fg="black", command=clicked, borderwidth=2, relief="solid")
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

    btn = Button(popup, text="Add", fg="black", command=lambda: added(xx, yy, code.get(), title.get(), cred.get(), variable.get(), sem, yer), borderwidth=2, relief="solid")
    btn.pack(side=BOTTOM, pady=50)

# COURSE ADDED BUTTON
def added(xx, yy, co, ti, cr, gr, se, ye):

    # Add course object to the list
    courses.append(Course(co, ti, cr, gr, se, ye))

    # Create the course frame
    frame = Frame(root, borderwidth=3, relief="raised", width=180, height=70, bg="lightgrey")
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


    btn = Button(root, text="+", fg="black", 
                     command=lambda: add(xx, yy + 75, se, ye), borderwidth=2, relief="solid")
    
    remov = Canvas(frame, width=14, height=15, bg="white", highlightthickness=2)
    remov.place(x=151, y=23)
    remov.create_text(9, 9, text="X", fill="red", font=("Helvetica", 15, "bold"), anchor="center")
    remov.bind("<Button-1>", lambda event: remove_confirm(frame, code.cget("text"), title.cget("text"), btn))

    if yy < 600:  # Limit vertical placement
        btn.place(x=xx + 70, y=yy + 100)

    # Close the popup window if it exists
    try:
        popup.destroy()
    except NameError:
        pass

# REMOVE POPUP CONFIRMATION
def remove_confirm(f, c, t, b):
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

    btn = Button(confirm, text="OK", command=lambda: remove(f, c, t, b), borderwidth=2, relief="solid")
    btn.pack(side=TOP, pady=10)

    confirm.lift()
    confirm.focus_force()

# REMOVE AND REFRESH
def remove(f, c ,t, b):
    confirm.destroy()
    i = 0
    seme = ""
    yea = 0
    while i < len(courses):
        if courses[i].code == c and courses[i].title == t:
            seme = courses[i].sem
            yea = courses[i].year
            courses.pop(i)
            break
        i += 1
    f.destroy()
    b.destroy()
    clear_window()
    course_page(startyear, startsem)
    temp = copy.deepcopy(courses)
    courses.clear()
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
        cury = 30 + len(existing_courses) * 75
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
            root.title("Ben's Course Planner ("+file.name+")")
            curx = 0
            cury = 30
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
                        cury = 30  # Fixed y position
                        global semester_offsets
                        semester_offsets = {
                            ("Fall", "Fall"): 0,
                            ("Fall", "Spring"): 210,
                            ("Fall", "Summer"): 210 + 225,
                            ("Spring", "Fall"): 225 + 240,
                            ("Spring", "Spring"): 0,
                            ("Spring", "Summer"): 225,
                            ("Summer", "Fall"): 240,
                            ("Summer", "Spring"): 240 + 210,
                            ("Summer", "Summer"): 0
                        }

                        global year_offset
                        year_offset = 210+225+240

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
                        cury = 30 + len(existing_courses) * 75
                        added(curx, cury, cCo, cTi, cCr, cGr, cSe, cYr)
                        l = 1  # Reset line count after processing the course

    root.focus_force()

#
# COURSE PAGE BUILD
#
def course_page(year, sem):

    st = str(sem) +" "+str(year)
    clear_window()
    i = 11
    j = 0
    cur = str(sem)
    while (i>0):
        nex = Label(root, text=cur +" "+str(year), borderwidth=2, relief="solid")
        nex.place(x=j, y=0)

        frame = Frame(root, borderwidth=5, relief="sunken", width=200, height=750)
        frame.place(x=j, y=20)

        btn = Button(root, text="+", fg="black", command=lambda x=j, s=cur, y=year: add(x, 30, s, y), borderwidth=2, relief="solid")
        btn.place(x=j+70, y=30)


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

#Array of courses
global courses
courses = []


start_win()
root.lift()
root.focus_force()

root.mainloop()

