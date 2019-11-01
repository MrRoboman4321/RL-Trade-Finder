import tkinter as tk
import tkinter.ttk as ttk

PAINT_MAP = {"Any": "0", "None": "N", "Painted": "A",
             "Burnt Sienna": "1", "Lime": "2", "Titanium White": "3", "Cobalt": "4",
             "Crimson": "5", "Forest Green": "6", "Grey": "7", "Orange": "8", "Pink": "9",
             "Purple": "10", "Saffron": "11", "Sky Blue": "12", "Black": "13"}

PAINTS = list(PAINT_MAP.keys())

def findTrades():
    print("Finding trades (placeholder)")

class TradeGUI:
    def __init__(self, master):
        self.master = master
        master.title("RL Trader")

        self.name_label = ttk.Label(master, text="Item name:")
        self.id_label = ttk.Label(master, text="Item id:")
        self.paint_label = ttk.Label(master, text="Item paint:")

        self.name = tk.StringVar(master)
        self.id = tk.StringVar(master)
        self.paint = tk.StringVar(master)

        self.paint.set(PAINTS[0])

        self.name_input = ttk.Entry(master, textvariable=self.name)
        self.id_input = ttk.Entry(master, textvariable=self.id)
        self.paint_select = ttk.OptionMenu(master, self.paint, PAINTS[0], *PAINTS)

        self.go_button = ttk.Button(master, text="Search", command=lambda: findTrades())


        self.name_label.grid(row=0, column=0)
        self.id_label.grid(row=1, column=0)
        self.paint_label.grid(row=2, column=0)

        self.name_input.grid(row=0, column=1)
        self.id_input.grid(row=1, column=1)
        self.paint_select.grid(row=2, column=1)

        self.go_button.grid(row=3, column=1)

root = tk.Tk()
trade_gui = TradeGUI(root)
root.mainloop()
