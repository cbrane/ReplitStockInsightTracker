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

# Function to create price chart for multiple stocks
def create_price_chart(data_dict):
    fig = go.Figure()
    for symbol, data in data_dict.items():
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{symbol} Close Price'))
    fig.update_layout(title='Stock Price History Comparison', xaxis_title='Date', yaxis_title='Price')
    return fig

# Main app
def main():
    st.title("Stock Data Visualization App")

    # User input for multiple stock symbols
    symbols_input = st.text_input("Enter Stock Symbols (comma-separated, e.g., AAPL,GOOGL,MSFT)", "AAPL,GOOGL,MSFT")
    symbols = [sym.strip().upper() for sym in symbols_input.split(',')]

    if symbols:
        # Fetch stock data for all symbols
        data_dict = {}
        info_dict = {}
        for symbol in symbols:
            hist_data, stock_info = fetch_stock_data(symbol)
            if hist_data is not None and stock_info is not None:
                data_dict[symbol] = hist_data
                info_dict[symbol] = stock_info

        if data_dict:
            # Display basic stock information for all symbols
            st.subheader("Stock Information")
            cols = st.columns(len(symbols))
            for i, (symbol, info) in enumerate(info_dict.items()):
                with cols[i]:
                    st.markdown(f"**{info.get('longName', symbol)} ({symbol})**")
                    st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
                    st.metric("Market Cap", f"${info.get('marketCap', 0) / 1e9:.2f}B")
                    st.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")

            # Display comparative price chart
            st.subheader("Price History Comparison")
            price_chart = create_price_chart(data_dict)
            st.plotly_chart(price_chart, use_container_width=True)

            # Display financial data tables
            st.subheader("Financial Data")
            for symbol, data in data_dict.items():
                with st.expander(f"{symbol} Financial Data"):
                    fin_data = pd.DataFrame({
                        'Date': data.index,
                        'Open': data['Open'],
                        'High': data['High'],
                        'Low': data['Low'],
                        'Close': data['Close'],
                        'Volume': data['Volume']
                    })
                    st.dataframe(fin_data)
                    
                    # CSV download button for each stock
                    csv = fin_data.to_csv(index=False)
                    st.download_button(
                        label=f"Download {symbol} data as CSV",
                        data=csv,
                        file_name=f"{symbol}_stock_data.csv",
                        mime="text/csv",
                    )
        else:
            st.warning("Unable to fetch stock data. Please check the symbols and try again.")

if __name__ == "__main__":
    main()
