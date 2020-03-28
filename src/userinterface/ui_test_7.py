from tkinter import *

root = Tk()


def leftClick(event):
    print("Left")


def middleClick(event):
    print("Middle")


def rightClick(event):
    print("Right")


root.title("Button Click Test")

frame = Frame(root, width=300, height=250)

# Button numbers are dependent on the OS.
# On Mac, Button #2 is a right click!
frame.bind("<Button-1>", leftClick)
frame.bind("<Button-2>", rightClick)
frame.bind("<Button-3>", middleClick)

frame.pack()

root.mainloop()
