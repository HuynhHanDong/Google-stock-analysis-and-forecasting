# Google Stock Analysis and Forecasting
This project combines time series forecasting with Explainable AI (XAI) techniques to predict and interpret Google stock prices. We implement both traditional models (ARIMA, SARIMA) and deep learning models (LSTM, Transformer), enhanced with tools like SHAP, LIME, Attention, ICFTS, and DAVOTS to make model predictions more transparent and interpretable. The project includes an interactive Streamlit dashboard for visualizing forecasts and exploring model explainability through dynamic charts and XAI visual tools.

## Dataset
Google Stock Data (2020-2025): https://www.kaggle.com/datasets/mzohaibzeeshan/google-stock-price-data-2020-2025-googl

This dataset includes the daily historical stock prices for Google (GOOGL) spanning from 2020 to 2025. It features essential financial metrics such as opening and closing prices, daily highs and lows, adjusted close prices, and trading volumes.

## Exploratory Data Analysis (EDA)
- Check for missing data and outliers.
- Visualize data (Closing price, Opening price, High, Low, Trading volume).
- Calculate moving averages and volatility.
- Analyze seasonality (Seasonal Decomposition).
- Examine the relationship between closing price and trading volume.

## Time Series Forecasting with Traditional Models
- Implement ARIMA and SARIMA for stock price forecasting.
- Evaluate the models using RMSE and MAE.

## Time Series Forecasting with Deep Learning
- Train LSTM and Time Series Transformer to forecast stock prices.
- Evaluate models performance.

## Model Comparison
- Compare ARIMA vs SARIMA vs LSTM vs Transformer (error metrics).
- Assess the trade-off between accuracy and interpretability.

## Explainable AI (XAI)
1. Feature Importance Analysis   
Use SHAP to evaluate the most influential factors affecting stock prices.

2. Local Interpretability   
Use LIME to explain predictions from the LSTM/Transformer models. Identify why the model made a specific prediction.

3. ICFTS and DAVOTS Methods   
Apply ICFTS for generating counterfactual explanations. Use DAVOTS to visualize the weight distribution in forecasting results.

4. Financial Analysis   
Provide conclusions on the key factors in the financial market.

## Dashboard Explainability (Streamlit)
The application focuses on simplicity, ease of use, and provides the following key features:

- Interative financial analysis charts of Google stock (2020–2025)

- Forecast model selection: Users can choose between ARIMA, LSTM, or Transformer to forecast Google stock prices (GOOGL).

- Adjustable forecast time frame: Allows users to select the number of days to forecast.

- Forecast result visualization: Line chart displaying actual vs. predicted prices, making it easy to track discrepancies over time.

- XAI analysis charts
