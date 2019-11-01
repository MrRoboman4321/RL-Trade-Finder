# Tk_ListBoxScroll1.py
# simple example of Tkinter listbox with scrollbar
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class ListboxScrollbar:
    def __init__(self, master):
        self.master = master
        self.master.minsize(400, 400)

        self.friend_list = ['Stew', 'Tom', 'Jen', 'Adam', 'Ethel', 'Barb', 'Tiny',
                            'Tim', 'Pete', 'Sue', 'Egon', 'Swen', 'Albert']

        # create the listbox (height/width in char)
        self.listbox = tk.Listbox(root, width=20, height=6)
        self.listbox.grid(row=0, column=0)

        yscroll = tk.Scrollbar(command=self.listbox.yview, orient=tk.VERTICAL)
        yscroll.grid(row=0, column=1, sticky='ns')
        self.listbox.configure(yscrollcommand=yscroll.set)

        for item in self.friend_list:
            # insert each new item to the end of the listbox
            self.listbox.insert('end', item)
        # optionally scroll to the bottom of the listbox
        lines = len(self.friend_list)


root = tk.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.title('listbox with scrollbar')

test = ListboxScrollbar(root)


root.mainloop()