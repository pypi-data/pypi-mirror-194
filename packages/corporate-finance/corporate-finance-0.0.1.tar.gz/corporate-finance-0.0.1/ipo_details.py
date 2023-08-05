import datetime
import yfinance as yf

import yfinance as yf

def ipo_date(ticker):
    # Use the Ticker class from the yfinance library to get the historical data for the stock
    stock = yf.Ticker(ticker.upper())
    # Get the maximum period of historical data available for the stock
    stock_history = stock.history(period="max")
    # Get the earliest available data, which is the first row of the stock_history data frame
    ipo_day = stock_history.head(1)
    # Get the year, month, and day of the IPO date
    year = ipo_day.index[0].year
    month = ipo_day.index[0].month
    day = ipo_day.index[0].day
    # Print the IPO date in the format "Company ticker '{ticker}' has Lauch their IPO on {day}-{month}-{year}"
    print(f"Company ticker '{ticker.upper()}' has Lauch their IPO on {day}-{month}-{year}")


'''The IPO tenure refers to the length of time that a company has been publicly traded since 
its initial public offering (IPO). The IPO tenure begins on the date of the company's IPO and
 continues until the present day.

The IPO tenure can be an important factor for investors as it provides information about the company's financial performance 
and stability since it went public. 

Companies that have been publicly traded for a long time are generally seen as being more established 
and credible than companies that have only recently gone public. 

The IPO tenure can also provide insight into the company's ability to attract 
and retain investors, as well as its ability to navigate the challenges of being a publicly traded company.

It's important to note that the IPO tenure is only one of many factors that investors should consider when evaluating a publicly traded company.
Other factors, such as the company's financial performance, management team, and industry conditions, 
are also important to consider when making investment decisions.'''

def ipo_tenture(ticker):

    # Use the Ticker class from the yfinance library to get the historical data for the stock
    stock = yf.Ticker(ticker.upper())
    # Get the maximum period of historical data available for the stock
    stock_history = stock.history(period="max")
    # Get the earliest available data, which is the first row of the stock_history data frame
    ipo_day = stock_history.head(1)
    # Get the year, month, and day of the IPO date
    year = ipo_day.index[0].year
    month = ipo_day.index[0].month
    day = ipo_day.index[0].day
    
    # Specify the date you want to calculate the difference from
    target_date = datetime.datetime(year, month, day)

    # Calculate the difference between the target date and today
    today = datetime.datetime.now()
    difference = today - target_date 

    # Print the number of days between today and the target date
    print(f"Number of days between today and {target_date.strftime('%Y-%m-%d')}: {difference.days} days")



def ipo_price(ticker):
    # Use the Ticker class from the yfinance library to get the historical data for the stock
    stock = yf.Ticker(ticker.upper())
    # Get the maximum period of historical data available for the stock
    stock_history = stock.history(period="max")
    # Get the earliest available data, which is the first row of the stock_history data frame
    ipo_inital = stock_history.Open[0]
    final_price = stock_history.Close[-1]

    # Print the number of days between today and the target date
    print(f"Initial price on launch {ipo_inital} and current price {final_price}")
