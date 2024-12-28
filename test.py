from tkinter import *
import random
  
def randomColor ():
    randomRed = ("00" + hex(random.randint(0, 255))[2:])[-2]
    randomGreen = ("00" + hex(random.randint(0, 255))[2:])[-2]
    randomBlue = ("00" + hex(random.randint(0, 255))[2:])[-2]
    return "#{}{}{}".format(randomRed, randomGreen, randomBlue)
  
class RandomColorNestedFramesApp:
  
    def __init__(self, master):
        self.master = master
        self.master.geometry("1024x1024+50+50")
        self.bgFrame = Frame(self.master, bg = randomColor())
        self.bgFrame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        self.addFrameButton = Button(self.bgFrame, text = "add sub-frame", bg = "#FF00CC", fg = "black", font = "Times 11", command = self.addDaughterFrame)
        self.addFrameButton.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 0.07)
        self.frameList = []
  
    def addDaughterFrame (self):
        if len(self.frameList) < 2:
            self.frameList.append(Frame(self.bgFrame, bg = randomColor()))
  
        else:
            self.frameList.append(Frame(self.frameList[-2], bg = randomColor()))
  
        self.frameList[-1].place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.96, relheight = 0.96)
  
if __name__ == "__main__":
    root = Tk()
    theApp = RandomColorNestedFramesApp(root)
    root.mainloop()