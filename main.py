import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="Stock Data Visualization", layout="wide")

# Function to fetch stock data
def fetch_stock_data(symbol, period="1y"):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

# Function to create price chart
def create_price_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title='Stock Price History', xaxis_title='Date', yaxis_title='Price')
    return fig

# Main app
def main():
    st.title("Stock Data Visualization App")

    # User input for stock symbol
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL for Apple Inc.)", "AAPL").upper()

    if symbol:
        # Fetch stock data
        hist_data, stock_info = fetch_stock_data(symbol)

        if hist_data is not None and stock_info is not None:
            # Display basic stock information
            st.subheader(f"{stock_info.get('longName', symbol)} ({symbol})")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${stock_info.get('currentPrice', 'N/A'):.2f}")
            col2.metric("Market Cap", f"${stock_info.get('marketCap', 0) / 1e9:.2f}B")
            col3.metric("P/E Ratio", f"{stock_info.get('trailingPE', 'N/A'):.2f}")

            # Display price chart
            st.subheader("Price History")
            price_chart = create_price_chart(hist_data)
            st.plotly_chart(price_chart, use_container_width=True)

            # Display financial data table
            st.subheader("Financial Data")
            fin_data = pd.DataFrame({
                'Date': hist_data.index,
                'Open': hist_data['Open'],
                'High': hist_data['High'],
                'Low': hist_data['Low'],
                'Close': hist_data['Close'],
                'Volume': hist_data['Volume']
            })
            st.dataframe(fin_data)

            # CSV download button
            csv = fin_data.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{symbol}_stock_data.csv",
                mime="text/csv",
            )
        else:
            st.warning("Unable to fetch stock data. Please check the symbol and try again.")

if __name__ == "__main__":
    main()
