"""Grid Layout Demo, with User & Password
Entry fields, and a Checkbox
"""


from tkinter import *


def login(event):
    print("Login not implemented!")


root = Tk()

root.title("Grid Layout")

label_1 = Label(root, text="User")
label_2 = Label(root, text="Password")
entry_1 = Entry(root)
entry_2 = Entry(root)

# E = East
label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)

btn_login = Button(root, text="Login")
btn_login.bind("<Button-1>", login)
btn_login.grid(columnspan=2)

root.mainloop()
