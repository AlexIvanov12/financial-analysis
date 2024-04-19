import sqlite3

def init_db():
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            date TEXT,
            profit REAL,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_trade_db(symbol, date, profit, trade_type):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('INSERT INTO trades (symbol, date, profit, type) VALUES (?, ?, ?, ?)',
              (symbol, date, profit, trade_type))
    conn.commit()
    conn.close()



def calculate_performance_db():
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('SELECT profit FROM trades')
    profits = c.fetchall()
    if not profits:
        return "No trades to analyze."
    profits = [p[0] for p in profits]
    win_rate = sum(1 for profit in profits if profit > 0) / len(profits)
    average_profit = sum(profits) / len(profits)
    max_drawdown = min(profits)  # Simplistic drawdown calculation
    conn.close()
    return {
        "win_rate": win_rate,
        "average_profit": average_profit,
        "max_drawdown": max_drawdown
    }

