import tkinter
from tkinter import *

root = Tk()


def left_click(event: tkinter.Event):
    print("Left Mouse Button (LMB)", type(event))


def middle_click(event: tkinter.Event):
    print("Middle Mouse Button (MMB)", type(event))


def right_click(event: tkinter.Event):
    print("Right Mouse Button (RMB)", type(event))


root.title("Mouse Button Click Test")

frame = Frame(root, width=300, height=250)

# Button numbers are dependent on the OS.
# On Mac, Button #2 is a right click!
frame.bind("<Button-1>", left_click)
frame.bind("<Button-2>", right_click)
frame.bind("<Button-3>", middle_click)

frame.pack()

root.mainloop()
