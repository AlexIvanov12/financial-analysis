import json
import datetime

# Initialize a simple file-based logging for trades
def init_trade_log():
    with open('trade_log.json', 'w') as file:
        json.dump([], file)  # Initialize an empty list to store trades

# Log a trade to the JSON file
def log_trade(trade_data):
    with open('trade_log.json', 'r+') as file:
        trades = json.load(file)
        trades.append(trade_data)
        file.seek(0)  # Move to the start of the file
        json.dump(trades, file, indent=4)

# Calculate performance metrics based on logged trades
def calculate_performance():
    with open('trade_log.json', 'r') as file:
        trades = json.load(file)
        if not trades:
            return "No trades to analyze."
        profits = [trade['profit'] for trade in trades]
        win_rate = sum(1 for profit in profits if profit > 0) / len(profits)
        average_profit = sum(profits) / len(profits)
        max_drawdown = min(profits)  # Simplistic drawdown calculation
        return {
            "win_rate": win_rate,
            "average_profit": average_profit,
            "max_drawdown": max_drawdown
        }

# Example usage of logging and performance calculation
def perform_trade_simulation():
    init_trade_log()  # Initialize the log
    # Simulate some trades
    for _ in range(10):
        trade_result = {
            "date": str(datetime.datetime.now()),
            "symbol": "AAPL",
            "profit": np.random.uniform(-100, 100)  # Random profit or loss
        }
        log_trade(trade_result)
    
    # Calculate and print performance
    performance = calculate_performance()
    print("Performance Metrics:", performance)

perform_trade_simulation()
