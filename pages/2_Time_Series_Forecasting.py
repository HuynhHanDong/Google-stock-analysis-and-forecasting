import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import joblib
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Time Series Forecasting Dashboard")
st.header("Google Stock Price Forecasting (2020-2025)")

# Load dataset
google = pd.read_csv('C:/Users/HanDong/Documents/Study/Semester 4/DAPm391/assignment/Google_Stock_2020_2025.csv')
google['MonthYear'] = pd.to_datetime(google['Date']).dt.strftime('%Y-%m')

# Path to trained models
models = {
    "ARIMA": "./saved_models/arima.pkl",
    "SARIMA": "./saved_models/sarima.pkl",
    "LSTM": "./saved_models/lstm.pkl",
    "Transformer": "./saved_models/transformer.pkl"
}

# User selection for model and test size
selected_model = st.selectbox("Select forecasting model", list(models.keys()))
test_size = st.slider("Select test size (percentage of data)", 10, 50, 30, 10)

# Filter data based on selection
test_sample_size = int(len(google) * (test_size / 100))
train_size = len(google) - test_sample_size
st.write(f"Number of test samples: {test_sample_size}")

# User selection window size
if selected_model in ["LSTM", "Transformer"]:
    window_size = st.slider("Select window size", 10, 100, 60, 10)

button = st.button("Forecast")

# Load selected model and generate forecast
def load_model(model_path):
    with open(model_path, "rb") as file:
        return joblib.load(file)

# Function to create sequences (fot LSTM and Transformer)
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i, 0])  # Take window_size previous values
        y.append(data[i, 0])  # Predict the next value
    return np.array(X), np.array(y)   

def generate_counterfactual(instance, target):
    modified_instance = instance.copy()
    modified_instance['Close'] = target  # Adjust Close price to desired counterfactual value
    return modified_instance

if button:
    st.header('Result')
    model = load_model(models[selected_model])

    if (selected_model == "ARIMA") or (selected_model == "SARIMA"):
        # Split test data
        test = google[test_sample_size:]['Close']
        test_date = google[-test_sample_size:]['Date']

        # Forecast
        predictions = model.forecast(steps=test_sample_size)
        google["Forecast"] = [None] * (len(google) - test_sample_size) + list(predictions)  # Add "Forecast" column to dataset

        # Visualize result
        actual_chart = alt.Chart(google).mark_line(color='blue').encode(
            x='Date:T',
            y=alt.Y('Close', title='Train Price'),
            tooltip=['Date', 'Close']
        )

        test_chart = alt.Chart(pd.DataFrame({'Date': test_date, 'Test': test})).mark_line(color='green').encode(
            x='Date:T',
            y=alt.Y('Test', title='Test Price'),
            tooltip=['Date', 'Test']
        ).properties(title=f"{selected_model} model forecast for Google stock price", width=800, height=400).interactive()

        forecast_chart = alt.Chart(pd.DataFrame({'Date': test_date, 'Forecast': predictions})).mark_line(color='orange', strokeDash=[5,5]).encode(
            x='Date:T',
            y=alt.Y('Forecast', title='Forecasted Price'),
            tooltip=['Date', 'Forecast']
        ).properties(title=f"{selected_model} model forecast for Google stock price", width=800, height=400).interactive()

    else:
        scaler = MinMaxScaler()
        data = scaler.fit_transform(google[['Close']].values)
        X, y = create_sequences(data, window_size)

        # Split test data
        X_test = X[test_sample_size:]
        y_test = y[test_sample_size:]

        # Reshape for LSTM input (samples, time steps, features)
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # Forecast
        predictions = model.predict(X_test)

        # Inverse transform predictions to original scale
        y_pred_rescaled = scaler.inverse_transform(predictions)
        y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))
        predicted_dates = google['Date'].iloc[len(google) - test_sample_size:]
        train_actual = google.iloc[:len(google)-test_sample_size]
        test_actual = google.iloc[len(google)-test_sample_size:]

        # Add "Forecast" column to dataset
        google["Forecast"] = [None] * (len(google) - test_sample_size) + list(predictions)

        # Visualize result
        actual_chart = alt.Chart(google).mark_line(color='blue').encode(
            x='Date:T',
            y=alt.Y('Close', title='Train Price'),
            tooltip=['Date', 'Close']
        )
        test_chart = alt.Chart(pd.DataFrame({'Date': predicted_dates, 'Test': test_actual})).mark_line(color='green').encode(
            x='Date:T',
            y=alt.Y('Test', title='Test Price'),
            tooltip=['Date', 'Test']
        )
        forecast_chart = alt.Chart(pd.DataFrame({'Date': predicted_dates, 'Forecast': y_pred_rescaled})).mark_line(color='orange', strokeDash=[5,5]).encode(
            x='Date:T',
            y=alt.Y('Forecast', title='Forecasted Price'),
            tooltip=['Date', 'Forecast']
        ).properties(title=f"{selected_model} model forecast for Google stock price", width=800, height=400).interactive()

    # Show chart
    st.altair_chart(actual_chart + test_chart + forecast_chart, use_container_width=True)

    st.header('SHAP explanation')
    if selected_model == "ARIMA":
        st.image("shap_arima.png")
    elif selected_model == "SARIMA":
        st.image("shap_sarima.png")
    elif selected_model == "LSTM":
        st.image("shap_lstm.png")
    else:
        st.image("shap_tf.png")
    
    st.header('ICFTS explanation')
    cf_example = generate_counterfactual(google.iloc[test_size + 10], target=predictions.iloc[10] * 1.05)
    st.write(cf_example)

    coefficients = pd.DataFrame({
        "Coefficient": ["AR Coeff", "MA Coeff"],
        "Value": [model.arparams[0], model.maparams[0]]
    })

    st.header('DAVOTS explanation')
    DAVOTS_chart = alt.Chart(coefficients).mark_bar().encode(
        x=alt.X("Coefficient", title=f" {model} Coefficients"),
        y=alt.Y("Value", title="Coefficient Value"),
        color=alt.value("blue")
    )
    st.altair_chart(DAVOTS_chart, use_container_width=True)
