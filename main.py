# Import neccesary libraries
import requests as r
from datetime import datetime
from plotly import graph_objects

# Get the voinbase api link + granularity (how long you want candle stick time period)
COINBASE_API_CANDLESTICKS_URL = \
    'https://api.pro.coinbase.com/products/{}/candles?granularity={}'


# Define main program functionality 
def main():
    resp = r.get(
        COINBASE_API_CANDLESTICKS_URL.format(
            'ADA-USD', # Give the crypto (ticker) you want + currency
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
            "text": "ADA/GDP Daily Chart"
        })
    )
    
    # Display the graph
    figure.show()

if __name__ == "__main__":
    main()