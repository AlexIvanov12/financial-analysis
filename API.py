from ib_insync import *
import datetime

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

stock = Stock('AAPL', 'SMART', 'USD')

market_data = ib.reqMktData(stock, '', False, False)
ib.sleep(1)
current_price = market_data.last

option = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)
option_chain = next((x for x in option if x.exchange == 'SMART'), None)

expiration_dates = sorted(option_chain.expirations)
strike_prices = sorted(option_chain.strikes)

target_expiration = expiration_dates[1]
target_strike = min(strike_prices, key = lambda x: abs(x - current_price))

risk_free_rate = 0.01
volatility = 0.20 #this is procent

expiration_date = datetime.datetime.strftime(target_expiration, '%Y%m%d')
days_to_expiration = (expiration_date - datetime.datetime.now()).days
time_to_expiration = days_to_expiration / 365.0

print(f'Current Price: {current_price}')
print(f'Strike Price: {target_strike}')
print(f'Risk-Free Rate: {risk_free_rate}')
print(f'Volatility: {volatility}')
print(f'Time to Expiration: {time_to_expiration}')

import time
from ib_insync import *
import logging

# Set up basic configuration for logging
logging.basicConfig(filename='trading_errors.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize the IB connection with error handling
def connect_to_ib():
    ib = IB()
    try:
        ib.connect('127.0.0.1', 7497, clientId=1, timeout=3)  # Set a timeout
    except ConnectionError as e:
        logging.error("Failed to connect to Interactive Brokers: %s", e)
        raise SystemExit(e)
    return ib

# Implement a retry mechanism for fetching market data
def fetch_market_data_with_retry(ib, stock, retries=3):
    for _ in range(retries):
        try:
            market_data = ib.reqMktData(stock, '', False, False)
            if market_data:
                return market_data
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            logging.warning("Error fetching market data, retrying...: %s", e)
    logging.error("Failed to fetch market data after retries.")
    return None

# Function to safely execute trades with error handling
def execute_trade(ib, order):
    try:
        trade = ib.placeOrder(order)
        ib.sleep(1)  # Wait for the order to process
        if trade.orderStatus.status == 'Filled':
            return trade
        else:
            logging.warning("Order not filled, status: %s", trade.orderStatus.status)
    except Exception as e:
        logging.error("Failed to execute trade: %s", e)
    return None

# Example trading system operation
def trading_system():
    ib = connect_to_ib()
    stock = Stock('AAPL', 'SMART', 'USD')
    market_data = fetch_market_data_with_retry(ib, stock)
    if market_data:
        print("Market data retrieved:", market_data)
        order = MarketOrder('BUY', 100)
        trade = execute_trade(ib, order)
        if trade:
            print("Trade executed successfully:", trade)
    else:
        print("Failed to retrieve market data.")

trading_system()
