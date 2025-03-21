import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

google = pd.read_csv('googl_data_2020_2025.csv')

st.set_page_config(page_title='Stock Analysis')

# -----------------------------------------------------------------------------------------------------------
st.header("Google stock price 2014 - 2025")
st.image()

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Moving Averages")

# Input rolling day:
rolling = st.number_input("Rolling", min_value=1, max_value=500, value=30)

def moving_averages(number_of_day: int):
    google.loc[:, "Close_MA"] = google["Close"].rolling(window=number_of_day, min_periods=1).mean()
    sns.lineplot(x=google['Date'], y=google["Close"], label="Closing Price", linewidth=2)
    sns.lineplot(x=google['Date'], y=google["Close_MA"], label=f"{number_of_day}-Day MA", linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title(f"Google Stock Price Moving Averages ({number_of_day} Days)")
    plt.legend()
    plt.grid()
    
# Plot image
ma_img = moving_averages(rolling)
st.image(ma_img)

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Volatility")

# Input rolling:
rolling = st.number_input("Rolling", min_value=1, max_value=500, value=30)

def volatility(number_of_day: int):
    google["Volatility"] = google["Close"].rolling(window=number_of_day).std()
    plt.plot(google['Date'], google["Volatility"], label=f"{number_of_day}-Day Volatility", color='purple')
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.title(f"Google Stock Price Volatility ({number_of_day} Days)")
    plt.legend()
    plt.grid()

# Plot image
volatility_img = volatility(rolling)
st.image(volatility_img)

# -----------------------------------------------------------------------------------------------------------
st.header("Seasonal Decomposition")
decomposition = seasonal_decompose(google["Close"], model="additive", period=252)   # 252 ngày giao dịch/năm

plt.figure(figsize=(12, 10))

plt.subplot(4, 1, 1)
plt.title("Google Stock Seasonal Decomposition")
plt.plot(google['Date'], decomposition.observed, label="Observed", color="blue")    # Observed (Dữ liệu gốc): Giá đóng cửa theo thời gian
plt.grid()
plt.legend()

plt.subplot(4, 1, 2) 
plt.plot(google['Date'], decomposition.trend, label="Trend", color="red")           # Trend (Xu hướng): Xu hướng dài hạn của giá cổ phiếu
plt.grid()
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(google['Date'], decomposition.seasonal, label="Seasonal", color="green")   # Seasonal (Thời vụ): Biến động có tính chu kỳ hàng năm
plt.grid()
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(google['Date'], decomposition.resid, label="Residual", color="orange")     # Residual (Phần dư): Phần không giải thích được bởi xu hướng và thời vụ
plt.grid()
plt.legend()

plt.tight_layout()
st.image()

# -----------------------------------------------------------------------------------------------------------
st.header("Scatter plot")

# Choose X and Y
X = st.selectbox("X", ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume'])
Y = st.selectbox("Y", ['Volume', 'Close', 'High', 'Low', 'Open', 'Adj Close'])

def scatter_plot(X,Y):
    sns.scatterplot(x=google[X], y=google[Y], alpha=0.5)
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.title(f"{X} vs {Y}")
    plt.grid()

# Show scatter plot
scatter_img = scatter_plot(X,Y)
st.image(scatter_img)