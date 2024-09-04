import yfinance as yf
import pandas as pd

# Laden der historischen Preisdaten für ein Symbol (z.B. AAPL)
symbol = "AAPL"
data = yf.download(symbol, start="2022-01-01", end="2023-01-01")

# Berechnung des gleitenden Durchschnitts
short_window = 50
long_window = 200

data['SMA50'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['SMA200'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Erstellen einer Signalspalte
data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['SMA50'][short_window:] > data['SMA200'][short_window:], 1, 0)

# Erstellen einer Positionsspalte
data['Position'] = data['Signal'].diff()

# Ausgabe der Kauf- und Verkaufssignale
buy_signals = data[data['Position'] == 1]
sell_signals = data[data['Position'] == -1]

print("Buy Signals:")
print(buy_signals[['Close', 'SMA50', 'SMA200']])

print("\nSell Signals:")
print(sell_signals[['Close', 'SMA50', 'SMA200']])
