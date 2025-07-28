import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

st.title("📈 Portfolio Analysis")

# Sidebar - Select tickers and date range
tickers = st.sidebar.multiselect("Select stocks for portfolio", ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META'], default=['AAPL', 'MSFT'])
start = st.sidebar.date_input("Start date", dt.date(2020, 1, 1))
end = st.sidebar.date_input("End date", dt.date.today())

if not tickers:
    st.warning("Please select at least one ticker.")
else:
    # ✅ Download stock data safely for both single and multiple tickers
    raw_data = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=True)

    if isinstance(raw_data.columns, pd.MultiIndex):
        # Multiple tickers
        data = pd.concat([raw_data[ticker]['Close'] for ticker in tickers], axis=1)
        data.columns = tickers
    else:
        # Single ticker
        data = pd.DataFrame(raw_data['Close'])
        data.columns = tickers

    st.subheader("Stock Prices Over Time")
    st.line_chart(data)

    st.subheader("Daily Returns")
    returns = data.pct_change().dropna()
    st.line_chart(returns)

    st.subheader("Correlation Matrix")
    corr = returns.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Cumulative Returns")
    cumulative_returns = (1 + returns).cumprod()
    st.line_chart(cumulative_returns)

    st.success("Portfolio analysis completed successfully!")

