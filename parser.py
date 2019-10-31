import matplotlib.pyplot as plt
import webbrowser
import statistics
import requests
import time

from bs4 import BeautifulSoup

PAINT_MAP = {"Any": "0", "None": "N", "Painted": "A",
             "Burnt Sienna": "1", "Lime": "2", "Titanium White": "3", "Cobalt": "4",
             "Crimson": "5", "Forest Green": "6", "Grey": "7", "Orange": "8", "Pink": "9",
             "Purple": "10", "Saffron": "11", "Sky Blue": "12", "Black": "13"}

#Wrapper for an RL Item. Keeps track of the number in a trade, if its painted, and its name
class Item():
    def __init__(self, name, paint, amount):
        self.name = name
        self.paint = paint
        self.amount = str(amount)

    def __str__(self):
        return self.amount + "x " + self.paint + " " + self.name

    def __repr__(self):
        return self.amount + "x " + self.paint + " " + self.name

    def __eq__(self, other):
        if(other.paint == self.paint and other.name == self.name):
            return True

#Wrapper for a trade. Takes a list of items that a trade has, a list that it wants, and a link to that trade
class Trade():
    def __init__(self, items_in, items_out, link):
        self.items_in = items_in
        self.items_out = items_out

        self.link = link

    def __str__(self):
        return "Has: " + str(self.items_in) + ", Wants: " + str(self.items_out)

    def __repr__(self):
        return "Has: " + str(self.items_in) + ", Wants: " + str(self.items_out)

def plot_graph(key_list):
    buy_key_std_dev = statistics.stdev(key_list)
    buy_key_mean = statistics.mean(key_list)

    N, bins, patches = plt.hist([int(trade.items_in[0].amount) for trade in buy_orders], bins = max(key_list))

    for i,key in enumerate(key_list):
        if(key > buy_key_mean + 2*buy_key_std_dev):
            patches[i].set_facecolor('r')

    plt.show()

#Takes in a list of trades (rlg-trade-display-container is--user), and turns it into a list of Trade()'s
def parseTrades(trades):
    pairs = []

    for j,trade in enumerate(trades):
        link = trade.find("div", {"class": "rlg-trade-display-header"}).find('a')['href']

        have = trade.find_all("div", {"id": "rlg-youritems"})[0].find_all("a")
        want = trade.find_all("div", {"id": "rlg-theiritems"})[0].find_all("a")

        #If the trader has matched up keys with items (hopefully)
        #TODO: Add more checks to ensure its matching keys and not arbitrary items (do we care?)
        if(len(have) == len(want)):

            #For each item in the HAVE category
            for i,item in enumerate(have):

                #Get the number of that item. If the div doesn't exist, assume 1
                trade_in_amount = item.find('div', {"class": "rlg-trade-display-item__amount"})

                if trade_in_amount is not None:
                    trade_in_amount = int(trade_in_amount.text.strip("\n "))
                else:
                    trade_in_amount = 1

                trade_out_amount = want[i].find('div', {"class": "rlg-trade-display-item__amount"})
                if trade_out_amount is not None:
                    trade_out_amount = int(trade_out_amount.text.strip("\n "))
                else:
                    trade_out_amount = 1

                #Get the paint color of the item. If the div doesn't exist, assume None
                trade_in_paint = item.find('div', {"class": "rlg-trade-display-item-paint"})
                if(trade_in_paint is not None):
                    trade_in_paint = trade_in_paint["data-name"]
                else:
                    trade_in_paint = "None"

                trade_out_paint = want[i].find('div', {"class": "rlg-trade-display-item-paint"})
                if(trade_out_paint is not None):
                    trade_out_paint = trade_out_paint["data-name"]
                else:
                    trade_out_paint = "None"

                #Create the two items. item.find('img')['alt'] is the name of the item
                trade_in = Item(item.find('img')['alt'], trade_in_paint, trade_in_amount)
                trade_out = Item(want[i].find('img')['alt'], trade_out_paint, trade_out_amount)

                pairs.append(Trade([trade_in], [trade_out], link))

    return pairs

#Gets all pages on rocket-league.com related to the specific base_page.
#Once it collects all trades on one page, it parses all trades on that page.
#Returns the list of all parsed trades
def collectTrades(base_page):
    page = requests.get(base_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    #TODO: Edge case when there is only 1 page
    #Finds the number of max pages by either 1) getting the final button, or 2) the second to last button if button-end doesn't exist
    try:
        max_pages = int(soup.find('a', {'class': 'rlg-trade-pagination-button rlg-trade-pagination-button-end'}).text)
    except AttributeError as e:
        max_pages = int(soup.find_all('a', {'class': 'rlg-trade-pagination-button'})[-2].text)
    print("Max pages: " + str(max_pages))

    all_trades = []

    #For every trade page for this item
    for i in range(max_pages):
        print("Searching page " + str(i + 1))
        print(base_page + "&p=" + str(i + 1))

        #Get and parse the trade
        page = requests.get(base_page + "&p=" + str(i + 1))
        soup = BeautifulSoup(page.content, 'html.parser')

        #Get all divs that represent one trade
        trades = soup.find_all("div", {"class": "rlg-trade-display-container is--user"})

        #Extent the cumulative list by the parsed trades
        all_trades.extend(parseTrades(trades))

        #Delay to not make the site unhappy. Seems that the requests take longer than this anyways
        time.sleep(0.5)

    return all_trades

if(__name__ == "__main__"):

    #Determine which item we are searching for
    item_name = input("Item name (capitalization matters): ")
    item_id = int(input("Item id (get by doing a search on rocket-league.com): "))

    #TODO Add catch for invalid paint
    item_paint = input("Item paint (None, Any, Painted, or any paint color): ")

    item = Item(item_name, item_paint, 1)
    key = Item("Key", "None", 1)

    #Search for all trades that are buying said item
    for_keys = collectTrades("https://rocket-league.com/trading?filterItem=" + str(item_id) + "&filterCertification=0&filterPaint=" + PAINT_MAP[item_paint] + "&filterPlatform=1&filterSearchType=2")

    #Search for all trades that are selling said item
    for_items = collectTrades("https://rocket-league.com/trading?filterItem=" + str(item_id) + "&filterCertification=0&filterPaint=" + PAINT_MAP[item_paint] + "&filterPlatform=1&filterSearchType=1")

    buy_orders = []
    sell_orders = []

    for trade in for_keys:
        print(trade)
        if(trade.items_out[0] == item and trade.items_in[0] == key):
            buy_orders.append(trade)

    for trade in for_items:
        if(trade.items_in[0] == item and trade.items_out[0] == key):
            sell_orders.append(trade)

    buy_orders.sort(key = lambda trade: int(trade.items_in[0].amount), reverse = True)
    sell_orders.sort(key = lambda trade: int(trade.items_out[0].amount))

    print(buy_orders)
    print(sell_orders)

    #Determine the profit from connecting the max buy and the min sell
    profit = int(buy_orders[0].items_in[0].amount) - int(sell_orders[0].items_out[0].amount)

    print("Max buy: " + buy_orders[0].items_in[0].amount)
    print("Min sell: " + sell_orders[0].items_out[0].amount)

    #Determine whether there is a profit to be made by connecting the two trades.
    if(profit > 0):
        print("Profit found: " + str(profit) + " keys.\nTrade in: " + buy_orders[0].link + "\nTrade out: " + sell_orders[0].link)
    else:
        print("Profit (maybe?) not found. Profit is: " + str(profit) + " keys.\nTrade in: " + buy_orders[0].link + "\nTrade out: " + sell_orders[0].link)

    buy_key_counts = [int(trade.items_in[0].amount) for trade in buy_orders]

    plot_graph(buy_key_counts)

    input()

    #Open the two trades in chrome
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open_new_tab("https://rocket-league.com" + buy_orders[0].link)
    webbrowser.get(chrome_path).open_new_tab("https://rocket-league.com" + sell_orders[0].link)

    #If the user requests, find alternate buy/sell trades to display.
    i = 1
    new = input("Get new (buy/sell/end): ").lower()
    while(new != "end"):
        if(new == "buy"):
            print("Getting new buy: " + buy_orders[i].link)
            webbrowser.get(chrome_path).open_new_tab("https://rocket-league.com" + buy_orders[i].link)
        elif(new == "sell"):
            print("Getting new sell: " + sell_orders[i].link)
            webbrowser.get(chrome_path).open_new_tab("https://rocket-league.com" + sell_orders[i].link)

        i += 1
        new = input("Get new (buy/sell/end): ")
