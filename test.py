from tkinter import ttk
import tkinter as tk
import tkinter


root = tk.Tk()
root.title('Full Window Scrolling X Y Scrollbar Example')
root.geometry("1350x400")

# Create A Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH,expand=1)

# Create Frame for X Scrollbar
sec = tk.Frame(main_frame)
sec.pack(fill=tk.X,side=tk.BOTTOM)

# Create A Canvas
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# Add A Scrollbars to Canvas
x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)
x_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)
y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

# Configure the canvas
my_canvas.configure(xscrollcommand=x_scrollbar.set)
my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(tk.ALL))) 

# Create Another Frame INSIDE the Canvas
canvas = tk.Frame(my_canvas)

# Add that New Frame a Window In The Canvas
my_canvas.create_window((0,0),window= canvas, anchor="nw")

nex = tk.Label(canvas, text="balls", font=("Helvetica", 20), borderwidth=0, relief="solid")
nex.grid(row=5, column=5)
frame = tk.Frame(canvas, borderwidth=5, relief="sunken", width=200, height=750)
frame.place(x=0, y=30)#20

root.lift()
root.focus_force()

root.mainloop()