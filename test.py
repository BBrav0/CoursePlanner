import tkinter as tk
from tkinter import messagebox

def on_closing():
    # Display a confirmation dialog
    if messagebox.askokcancel("Quit", "Do you really want to close the application?"):
        root.destroy()  # Close the application
    # Otherwise, the window stays open

root = tk.Tk()
root.title("Example Application")

# Intercept the close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Add some content
label = tk.Label(root, text="This is an example application.")
label.pack(pady=20)

# Run the main event loop
root.mainloop()
