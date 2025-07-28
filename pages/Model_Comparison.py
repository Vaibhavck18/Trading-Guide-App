# pages/Model_Comparison.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import yfinance as yf
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Model Comparison", page_icon="🔍", layout="wide")
st.title("📊 Forecasting Model Comparison")

# Input
col1, col2 = st.columns([1, 1])
with col1:
    ticker = st.text_input("Enter Stock Ticker", "AAPL")
with col2:
    years = st.slider("Select number of years for training", 1, 5, 2)

# Load data
end = datetime.date.today()
start = datetime.date(end.year - years, end.month, end.day)
data = yf.download(ticker, start=start, end=end)

if data.empty:
    st.error("Failed to load stock data. Please enter a valid ticker.")
    st.stop()

data = data[['Close']].dropna()
data.reset_index(inplace=True)
data.columns = ['Date', 'Close']
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Visual
st.subheader(f"{ticker} Closing Price")
st.line_chart(data['Close'])

# Split
train_size = int(len(data) * 0.8)
train, test = data[:train_size], data[train_size:]

# Common forecast horizon
forecast_horizon = min(30, len(test))

# --------- ARIMA ----------
try:
    model_arima = ARIMA(train['Close'], order=(5, 1, 0))
    result_arima = model_arima.fit()
    forecast_arima = result_arima.forecast(steps=forecast_horizon)
    rmse_arima = np.sqrt(mean_squared_error(test['Close'][:forecast_horizon], forecast_arima))
except:
    forecast_arima = pd.Series([np.nan]*forecast_horizon, index=test.index[:forecast_horizon])
    rmse_arima = np.nan

# --------- SARIMA ----------
try:
    model_sarima = SARIMAX(train['Close'], order=(1, 1, 1), seasonal_order=(1, 1, 0, 12))
    result_sarima = model_sarima.fit(disp=False)
    forecast_sarima = result_sarima.forecast(forecast_horizon)
    rmse_sarima = np.sqrt(mean_squared_error(test['Close'][:forecast_horizon], forecast_sarima))
except:
    forecast_sarima = pd.Series([np.nan]*forecast_horizon, index=test.index[:forecast_horizon])
    rmse_sarima = np.nan

# --------- Prophet ----------
prophet_df = data.reset_index()[['Date', 'Close']]
prophet_df.columns = ['ds', 'y']
model_prophet = Prophet()
model_prophet.fit(prophet_df)
future = model_prophet.make_future_dataframe(periods=forecast_horizon)
forecast_prophet = model_prophet.predict(future)
forecast_p = forecast_prophet[['ds', 'yhat']].set_index('ds').iloc[-forecast_horizon:]
rmse_prophet = np.sqrt(mean_squared_error(test['Close'][:forecast_horizon], forecast_p['yhat']))

# --------- LSTM ----------
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[['Close']])
X, y = [], []
for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i, 0])
    y.append(scaled_data[i, 0])
X, y = np.array(X), np.array(y)

if len(X) > 0:
    X = X.reshape((X.shape[0], X.shape[1], 1))
    model_lstm = Sequential()
    model_lstm.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model_lstm.add(LSTM(units=50))
    model_lstm.add(Dense(1))
    model_lstm.compile(loss='mean_squared_error', optimizer='adam')
    model_lstm.fit(X, y, epochs=5, batch_size=32, verbose=0)

    test_inputs = scaled_data[-(forecast_horizon + 60):]
    X_test = []
    for i in range(60, len(test_inputs)):
        X_test.append(test_inputs[i-60:i, 0])
    X_test = np.array(X_test).reshape(-1, 60, 1)
    lstm_pred = model_lstm.predict(X_test)
    lstm_pred = scaler.inverse_transform(lstm_pred)
    rmse_lstm = np.sqrt(mean_squared_error(test['Close'][:forecast_horizon], lstm_pred[:forecast_horizon]))
else:
    lstm_pred = np.full((forecast_horizon,), np.nan)
    rmse_lstm = np.nan

# --------- Plotting ---------
fig = go.Figure()
fig.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=test['Close'][:forecast_horizon], name='Actual', line=dict(color='black')))
fig.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=forecast_arima, name='ARIMA'))
fig.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=forecast_sarima, name='SARIMA'))
fig.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=forecast_p['yhat'], name='Prophet'))
fig.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=lstm_pred.flatten(), name='LSTM'))
fig.update_layout(title=f'Model Forecast Comparison - {ticker}', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig, use_container_width=True)

# --------- RMSE Table ---------
rmse_df = pd.DataFrame({
    'Model': ['ARIMA', 'SARIMA', 'Prophet', 'LSTM'],
    'RMSE': [round(rmse_arima, 2), round(rmse_sarima, 2), round(rmse_prophet, 2), round(rmse_lstm, 2)]
})
st.subheader("📉 RMSE Comparison Table")
st.dataframe(rmse_df)
