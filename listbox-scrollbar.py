from tkinter import *


class Application:
    def __init__(self,  master):
        self.master = master
        self.master.minsize(400, 400)

        self.data = Listbox(self.master, bg='red')

        Grid.columnconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 1, weight=1)
        #Grid.rowconfigure(self.master, 0, weight=1)

        self.scrollbar = Scrollbar(command=self.data.yview, orient=VERTICAL)
        self.data.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.data.yview)

        for i in range(1000):
            self.data.insert(END, str(i))

        self.data.grid(row=0, column=0, sticky="nesw")

        self.scrollbar.grid(row=0, column=1, sticky="ns")


root = Tk()
a = Application(root)

root.mainloop()
