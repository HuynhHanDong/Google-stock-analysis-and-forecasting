import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='Stock Analysis Dashboard')

# Load dataset
google = pd.read_csv('C:/Users/HanDong/Documents/Study/Semester 4/DAPm391/assignment/Google_Stock_2020_2025.csv')
google['MonthYear'] = pd.to_datetime(google['Date']).dt.strftime('%Y-%m')

st.header("Google stock price 2014 - 2025")

# User selection for column and year
columns = ['Close', 'Open', 'High', 'Low', 'Adj Close', 'Volume']
selected_column = st.selectbox("Select column to visualize", columns)
selected_year = st.selectbox("Select year", ['2020-2025', 2020, 2021, 2022, 2023, 2024])

# Filter data based on selection
if selected_year == '2020-2025':
    filtered_df = google
else:
    filtered_df = google[google['Year'] == selected_year]

# Create Altair chart
price_chart = alt.Chart(filtered_df).mark_line().encode(
        x='Date:T',
        y=alt.Y(selected_column, title=f"{selected_column} Price"),
        tooltip=['Date', selected_column]
    ).properties(title=f"Google {selected_column} stock price {selected_year}", width=800, height=400).interactive()

# Display chart
st.altair_chart(price_chart, use_container_width=True)

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Moving Averages")

# User input for number of moving average day:
ma = st.number_input("Number of moving averages day", min_value=1, max_value=500, value=30)

# Filter data based on selection
google['Close_MA'] = google['Close'].rolling(window=ma, min_periods=1).mean()
df_melted = google.melt(id_vars=['Date', 'MonthYear'], value_vars=['Close', 'Close_MA'], var_name='Legend', value_name='Price')

# Create Altair chart
ma_chart = alt.Chart(df_melted).mark_line().encode(
    x=alt.X('Date:T', title="Time", axis=alt.Axis(format='%Y-%m')),
    y=alt.Y('Price:Q', title="Price (USD)"),
    color=alt.Color('Legend:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Date', 'Legend', 'Price']
).properties(title=f"Stock Price & {ma}-Day Moving Average", width=800, height=400).interactive()

# Display chart
st.altair_chart(ma_chart)

# -----------------------------------------------------------------------------------------------------------
st.header("Stock Price Volatility")

# user input for number of volatility day:
vol = st.number_input("Number of volatility day", min_value=1, max_value=500, value=30)

# Filter data based on selection
google['Volatility'] = google['Close'].rolling(window=vol).std()
    
# Create Altair chart
vol_chart = alt.Chart(google).mark_line(color='purple').encode(
    x=alt.X('Date:T', title="Time", axis=alt.Axis(format='%Y-%m')),
    y='Volatility:Q',
    tooltip=['Date', 'Volatility']
).properties(title=f"Google Stock Price Volatility ({vol} Days)").interactive()

# Display chart
st.altair_chart(vol_chart, use_container_width=True)

# -----------------------------------------------------------------------------------------------------------
st.header("Seasonal Decomposition")

# Show image
st.image("seasonal_decomposition.png")

# -----------------------------------------------------------------------------------------------------------
st.header("Scatter plot")

# User selection for X and Y axis
X = st.selectbox("X axis", ['Close', 'Adj Close', 'Open', 'High', 'Low', 'Volume'])
Y = st.selectbox("Y axis", ['Volume', 'High', 'Low', 'Open', 'Close', 'Adj Close'])

# Create Altair chart
scatter_chart = alt.Chart(google).mark_circle(size=60).encode(
    x=f'{X}:Q',
    y=f'{Y}:Q',
    color=f'{X}:Q',
    tooltip=['Date', X, Y]
).properties(title=f"{X} vs {Y}", width=750, height=400).interactive()

# Display chart
st.altair_chart(scatter_chart)