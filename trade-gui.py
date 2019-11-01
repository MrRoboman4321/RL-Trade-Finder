import tkinter as tk
import tkinter.ttk as ttk

import webbrowser

import TradeParser

PAINT_MAP = {"Any": "0", "None": "N", "Painted": "A",
             "Burnt Sienna": "1", "Lime": "2", "Titanium White": "3", "Cobalt": "4", "Crimson": "5", "Forest Green": "6",
             "Grey": "7", "Orange": "8", "Pink": "9", "Purple": "10", "Saffron": "11", "Sky Blue": "12", "Black": "13"}

PAINTS = list(PAINT_MAP.keys())


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

        self.go_button = ttk.Button(master, text="Search", command=lambda: self.spawn_orders())

        self.name_label.grid(row=0, column=0)
        self.id_label.grid(row=1, column=0)
        self.paint_label.grid(row=2, column=0)

        self.name_input.grid(row=0, column=1)
        self.id_input.grid(row=1, column=1)
        self.paint_select.grid(row=2, column=1)

        self.go_button.grid(row=3, column=1)

    def spawn_orders(self):
        buy_orders = TradeParser.getSortedBuyOrders(self.name.get(), self.id.get(), self.paint.get())
        sell_orders = TradeParser.getSortedBuyOrders(self.name.get(), self.id.get(), self.paint.get())

        print(buy_orders)

        self.orders_window = tk.Toplevel(self.master)
        self.buy_orders = OrderView(self.orders_window, buy_orders, "Buy Orders", self.name.get())


class OrderView():
    def __init__(self, master, orders, order_type, name):
        self.master = master
        self.master.minsize(400, 400)

        self.orders = orders

        self.item_label = tk.Label(self.master, text=f"{order_type} for {name}")
        self.key_label = tk.Label(self.master, text="Key count")
        self.link_label = tk.Label(self.master, text="Link")

        self.key_list = tk.Listbox(self.master)
        self.link_list = tk.Listbox(self.master, selectmode="SINGLE")

        self.link_list.bind("<<ListboxSelect>>", self.openTrade)

        for order in self.orders:
            keys = str(order.items_in[0].amount)

            self.key_list.insert(tk.END, keys)
            self.link_list.insert(tk.END, order.link)

        self.item_label.grid(row=0, column=0, sticky="nesw")
        self.key_label.grid(row=1, column=0, sticky="nesw")
        self.link_label.grid(row=1, column=1, sticky="nesw")

        self.key_list.grid(row=2, column=0, sticky="nesw")
        self.link_list.grid(row=2, column=1, sticky="nesw")

    def openTrade(self, event):
        link = self.link_list.get(self.link_list.curselection())
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open_new_tab("https://rocket-league.com" + link)

root = tk.Tk()
trade_gui = TradeGUI(root)
root.mainloop()
