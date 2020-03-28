import tkinter
from tkinter import ttk

root = tkinter.Tk()
root.title('UI Test 3')
style = ttk.Style(root)
style.theme_use('classic')
style.configure('Test.TLabel', background='red')
text = ttk.Label(root, text='Hello', style='Test.TLabel')
text.grid()
root.mainloop()
