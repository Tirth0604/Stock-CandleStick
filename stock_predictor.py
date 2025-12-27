import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Take stock name from user
stock = input("Enter Indian Stock Name (RELIANCE, TCS, INFY): ").upper()
ticker = stock + ".NS"

# Download last 7 days data
df = yf.download(ticker, period="7d", interval="1d", auto_adjust=False)

# If stock name is wrong
if df.empty:
    print("No data found")
    quit()

# Fix column names if MultiIndex
if hasattr(df.columns, 'get_level_values'):
    df.columns = df.columns.get_level_values(0)

# Convert to numpy arrays for faster processing
opens = np.array(df['Open'])
closes = np.array(df['Close'])
highs = np.array(df['High'])
lows = np.array(df['Low'])

# Calculate colors using numpy (1 for green, 0 for red)
colors = np.where(closes >= opens, 'green', 'red')

# Calculate bar heights and bottoms using numpy
bar_heights = np.abs(closes - opens)
bar_bottoms = np.minimum(opens, closes)

# Create figure
plt.figure(figsize=(10, 5))

# Draw candlesticks using numpy arrays
x_positions = np.arange(len(df))

for i in x_positions:
    # High–Low line
    plt.plot([i, i], [lows[i], highs[i]], color='black', linewidth=1)
    # Open–Close bar
    plt.bar(i, bar_heights[i], bottom=bar_bottoms[i], color=colors[i], width=0.6)
    # Display close price on top of each candle
    plt.text(i, highs[i], f'₹{closes[i]:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Show dates on x-axis
plt.xticks(x_positions, df.index.strftime('%d-%b'), rotation=45)
plt.title(f"{stock} - Last 7 Days Candlestick Chart")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.grid(True, alpha=0.3)

# Add some space at the top for price labels
y_range = highs.max() - lows.min()
plt.ylim(lows.min() - y_range * 0.05, highs.max() + y_range * 0.15)

plt.tight_layout()

# Display current price
current_price = closes[-1]
print(f"\nCurrent Price of {stock}: ₹{current_price:.2f}")

plt.show()