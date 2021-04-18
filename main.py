# Import neccesary libraries
import requests as r
from datetime import datetime
from plotly import graph_objects
import tkinter as tk
from playsound import playsound
import os

# Define the gui variables
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 110
WINDOW_TITLE = "Crypto Coin Daily Price Chart"
BUTTON_CLICK_SOUND = "clicks.wav"

# Get the voinbase api link + granularity (how long you want candle stick time period)
# The {} are used so we can pass the values in later
COINBASE_API_CANDLESTICKS_URL = \
    'https://api.pro.coinbase.com/products/{}/candles?granularity={}'

class CryptoCoinAnalysis:
    
    def __init__(self):
        # Define the format of the GUI
        self.window = tk.Tk()
        self.window.geometry("{}x{}".format(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.window.configure(bg="#FF0000")
        self.window.title(WINDOW_TITLE)
        self.window.iconbitmap("images/icon.ico")
        
        # Create Label
        self.header_label = tk.Label(self.window, text = "SELECT ONE OF THE AVALIABLE CRYPTO CURRENCIES BELOW", width=58)
        self.header_label.grid(column = 0, row = 1)
        # Create buttons
        self.ada_button = tk.Button(self.window, text = "ADA", command=lambda: self.__analysis("ADA"), width = 13)
        self.ada_button.grid(column = 0, row = 2)
        self.btc_button = tk.Button(self.window, text = "BTC", command=lambda: self.__analysis("BTC"), width = 13)
        self.btc_button.grid(column = 0, row = 3)
        self.eth_button = tk.Button(self.window, text = "ETH", command=lambda: self.__analysis("ETH"), width = 13)
        self.eth_button.grid(column = 0, row = 4)
        
        return

    # Define main program functionality 
    def __analysis(self, option):
        playsound(BUTTON_CLICK_SOUND)

        resp = r.get(
            COINBASE_API_CANDLESTICKS_URL.format(
                f'{option}-USD', # Give the crypto (ticker) you want + currency
                86400 # Give granularity in seconds (86400 seocnds in a day)
            )
        )
        resp_json = resp.json()

        # Define arrays to store data from coinbase
        dates = []
        lows = []
        highs = []
        opens = []
        closes = []

        # resp_json will contains data in below order, so we can loop through and
        # add the data at the correct index to appropriate (array) candle stick attribute above
        for candle_stick_data in resp_json:
            dates.append(datetime.fromtimestamp(candle_stick_data[0]))
            lows.append(candle_stick_data[1])
            highs.append(candle_stick_data[2])
            opens.append(candle_stick_data[3])
            closes.append(candle_stick_data[4])

        # Make the graph using built in plotly Candlestick functions
        figure = graph_objects.Figure(
            data = [ graph_objects.Candlestick(
                x=dates, 
                open=opens, 
                high=highs, 
                low=lows, 
                close=closes
                ) 
            ],
            layout = graph_objects.Layout(title={
                "text": f"{option}/USD Daily Chart"
            })
        )

        # Display the graph
        figure.show()
        
        return
    
    def run_app(self):
        self.window.mainloop()
        return

if __name__ == "__main__":
    app = CryptoCoinAnalysis()
    app.run_app()