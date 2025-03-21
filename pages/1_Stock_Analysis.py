import streamlit as st
import pandas as pd
import altair as alt
from statsmodels.tsa.seasonal import seasonal_decompose

google = pd.read_csv('C:/Users/HanDong/Documents/Study/Semester 4/DAPm391/assignment/Google_Stock_2020_2025.csv')
google['Year'] = pd.to_datetime(google['Year']).dt.strftime('%Y')

st.set_page_config(page_title='Stock Analysis')

st.header("Google stock price 2014 - 2025")
st.write("Comming soon")
#st.image()

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Moving Averages")

# Input rolling day:
ma = st.number_input("Number of moving averages day", min_value=1, max_value=500, value=30)

def moving_averages(number_of_day: int):
    google['Close_MA'] = google['Close'].rolling(window=number_of_day, min_periods=1).mean()
    df_melted = google.melt(id_vars=['Date', 'MonthYear'], value_vars=['Close', 'Close_MA'], var_name='Legend', value_name='Price')
    
    chart = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('Date:T', title="Time", axis=alt.Axis(format='%Y-%m')),
        y=alt.Y('Price:Q', title="Price (USD)"),
        color=alt.Color('Legend:N', scale=alt.Scale(scheme='category10')),
        tooltip=['Date', 'Legend', 'Price']
    ).properties(title=f"Stock Price & {number_of_day}-Day Moving Average", width=800, height=400).interactive()
    
    st.altair_chart(chart)

# Plot image
moving_averages(ma)

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Volatility")

# Input rolling:
rolling = st.number_input("Number of volatility day", min_value=1, max_value=500, value=30)

def volatility(number_of_day: int):
    google['Volatility'] = google['Close'].rolling(window=number_of_day).std()
    
    vol_chart = alt.Chart(google).mark_line(color='purple').encode(
        x=alt.X('Date:T', title="Time", axis=alt.Axis(format='%Y-%m')),
        y='Volatility:Q',
        tooltip=['Date', 'Volatility']
    ).properties(title=f"Google Stock Price Volatility ({number_of_day} Days)").interactive()
    
    st.altair_chart(vol_chart, use_container_width=True)

# Plot image
volatility(rolling)

# -----------------------------------------------------------------------------------------------------------
st.header("Seasonal Decomposition")
st.write("Comming soon")
#st.image()

# -----------------------------------------------------------------------------------------------------------
st.header("Scatter plot")

# Choose X and Y
X = st.selectbox("X axis", ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume'])
Y = st.selectbox("Y axis", ['Volume', 'Close', 'High', 'Low', 'Open', 'Adj Close'])

def scatter_plot(X, Y):
    scatter_chart = alt.Chart(google).mark_circle(size=60).encode(
        x=f'{X}:Q',
        y=f'{Y}:Q',
        color=f'{X}:Q',
        tooltip=['Date', X, Y]
    ).properties(title=f"{X} vs {Y}", width=750, height=400).interactive()
    
    st.altair_chart(scatter_chart)

# Show scatter plot
scatter_plot(X, Y)