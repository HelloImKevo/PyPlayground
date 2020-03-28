"""Multi-line comments work like this.
Explain how the class works here!
"""


import tkinter as tk


class BuckyButtons:

    def __init__(self, master=None):
        frame = tk.Frame(master)
        frame.pack()

        self.print_button = tk.Button(frame, text="Print Message",
                                      command=self._print_message)
        self.print_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(frame, text="Quit",
                                     command=frame.quit)
        self.quit_button.pack(side=tk.LEFT)

    # noinspection PyMethodMayBeStatic
    def _print_message(self):
        """Internal function."""
        print("Wow, this actually worked!")


root = tk.Tk()
b = BuckyButtons(master=root)
root.mainloop()
