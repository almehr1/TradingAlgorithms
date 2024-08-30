import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def day_trading_strategy(data):
    data['RSI'] = calculate_rsi(data)
    data['Signal'] = 0
    
    # Buy signal: RSI below 30 (Oversold condition)
    data.loc[data['RSI'] < 30, 'Signal'] = 1
    
    # Sell signal: RSI above 70 (Overbought condition)
    data.loc[data['RSI'] > 70, 'Signal'] = -1
    
    data['Position'] = data['Signal'].shift(1)  # Position on next day
    
    return data

def backtest_strategy(data, initial_balance=10000):
    balance = initial_balance
    position = 0
    for i in range(1, len(data)):
        if data['Position'][i] == 1 and position == 0:  # Buy
            position = balance / data['Close'][i]
            balance = 0
            print(f"Buy at {data['Close'][i]} on {data.index[i].date()}")
        
        elif data['Position'][i] == -1 and position > 0:  # Sell
            balance = position * data['Close'][i]
            position = 0
            print(f"Sell at {data['Close'][i]} on {data.index[i].date()}")
    
    final_balance = balance if balance > 0 else position * data['Close'].iloc[-1]
    print(f"Final balance: {final_balance}")
    return final_balance

# Example usage:
ticker = "AAPL"  # Choose the stock ticker
start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Download historical data
data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
data = day_trading_strategy(data)

# Backtest the strategy
final_balance = backtest_strategy(data)
