import streamlit as st

st.set_page_config(page_title="Home Page")

st.write("# Welcome to Streamlit! 👋")
"""
## About Project:
In this project, we will apply time series forecasting techniques to financial data and compare the performance of ARIMA, LSTM, and Transformer models in stock price prediction. We will use SHAP and LIME to explain AI model predictions and assess the significance of financial factors within the models. Additionally, we will provide financial insights based on XAI and develop an Explainability Dashboard to visually present model interpretations. Furthermore, we will integrate ICFTS, DAVOTS, and Visual Explanations to enhance model explainability.

👈 Please check out the demo in sidebar!

### Dataset:  Google Stock Data (2020-2025)   
This dataset includes the daily historical stock prices for Google (GOOGL) spanning from 2020 to 2025. It features essential financial metrics such as opening and closing prices, daily highs and lows, adjusted close prices, and trading volumes.

### Models Used   
ARIMA, SARIMA, LSTM, and Transformer   

### Explainable AI (XAI) Techniques   
SHAP, LIME, ICFTS, DAVOTS

**Note**: Forecasts are not guarantees and explanations indicate model reasoning, not certainties.

## Created by: 
Huynh Han Dong, Tran Hoang Tuan Hung, Nguyen van Anh Duy
"""