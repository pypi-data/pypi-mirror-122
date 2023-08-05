from tkinter import Menu

class MenuBar(Menu):
    def __init__(self, tk):
        super().__init__(tk)
        
        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="train")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit")
        self.add_cascade(label="File", menu=filemenu)

