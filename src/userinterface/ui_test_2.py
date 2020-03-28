"""Multi-line comments work like this.
Explain how the class works here!
"""


import tkinter as tk
from tkinter import ttk


class Application(tk.Frame):
    title = None
    hi_there = None
    print_info = None
    entry_field = None
    contents = None
    quit = None

    def __init__(self, master=None):
        super().__init__(master)
        # self.hi_there = None
        # Note: The program or application main loop should
        # probably define the application frame title.
        self.master.title("UI Test 2")

        # Configure style - workaround for MacOSX Aqua theme.
        # (At this time, this does nothing.
        style = ttk.Style(master)
        style.theme_use('classic')
        # style.configure('Test.TLabel', background='red')

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.print_info = tk.Button(self)
        self.print_info["text"] = "Print Info"
        self.print_info["command"] = self.print_info_fun
        self.print_info.pack(side="top")

        self.entry_field = tk.Entry()
        self.entry_field.pack()

        self.contents = tk.StringVar()
        self.contents.set("Kevin")
        # tell the entry widget to watch this variable
        self.entry_field["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entry_field.bind('<Key-Return>', self._print_contents)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit["bg"] = "yellow"
        self.quit.pack(side="bottom")

    @staticmethod
    def say_hi():
        """Not sure why this should be static??"""
        print("hi there, everyone!")

    def print_info_fun(self):
        print("Frame.Config:", self.config())
        print("Button.Config:", self.hi_there.config())

    def _print_contents(self, _event):
        """Internal function."""
        print("Hi. contents of entry is now ---->",
              self.contents.get())


root = tk.Tk()
app = Application(master=root)
app.mainloop()
