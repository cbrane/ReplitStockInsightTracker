import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from textblob import TextBlob

# Set page configuration
st.set_page_config(page_title="Stock Data Visualization", layout="wide")

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=st.secrets["NEWSAPI_KEY"])

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

# Function to calculate moving averages
def calculate_moving_averages(data, short_window=20, long_window=50):
    data['SMA20'] = data['Close'].rolling(window=short_window).mean()
    data['SMA50'] = data['Close'].rolling(window=long_window).mean()
    return data

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# Function to create price chart for multiple stocks with indicators
def create_price_chart(data_dict):
    fig = go.Figure()
    for symbol, data in data_dict.items():
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{symbol} Close Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], mode='lines', name=f'{symbol} SMA20', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], mode='lines', name=f'{symbol} SMA50', line=dict(dash='dot')))
    
    fig.update_layout(title='Stock Price History Comparison with Moving Averages', xaxis_title='Date', yaxis_title='Price')
    return fig

# Function to create RSI chart
def create_rsi_chart(data_dict):
    fig = go.Figure()
    for symbol, data in data_dict.items():
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name=f'{symbol} RSI'))
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    
    fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI')
    return fig

# Function to fetch news articles
def fetch_news(symbol, days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    articles = newsapi.get_everything(
        q=symbol,
        from_param=start_date.strftime('%Y-%m-%d'),
        to=end_date.strftime('%Y-%m-%d'),
        language='en',
        sort_by='relevancy',
        page_size=10
    )
    
    return articles['articles']

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.05:
        return 'Positive'
    elif sentiment < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

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
                hist_data = calculate_moving_averages(hist_data)
                hist_data = calculate_rsi(hist_data)
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

            # Display comparative price chart with moving averages
            st.subheader("Price History Comparison with Moving Averages")
            price_chart = create_price_chart(data_dict)
            st.plotly_chart(price_chart, use_container_width=True)

            # Display RSI chart
            st.subheader("Relative Strength Index (RSI)")
            rsi_chart = create_rsi_chart(data_dict)
            st.plotly_chart(rsi_chart, use_container_width=True)

            # Display news sentiment analysis
            st.subheader("News Sentiment Analysis")
            for symbol in symbols:
                with st.expander(f"{symbol} News Sentiment"):
                    news_articles = fetch_news(symbol)
                    if news_articles:
                        for article in news_articles:
                            title = article['title']
                            description = article['description']
                            url = article['url']
                            sentiment = analyze_sentiment(title + " " + description)
                            
                            st.markdown(f"**{title}**")
                            st.write(description)
                            st.write(f"Sentiment: {sentiment}")
                            st.write(f"[Read more]({url})")
                            st.write("---")
                    else:
                        st.write("No recent news articles found.")

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
                        'Volume': data['Volume'],
                        'SMA20': data['SMA20'],
                        'SMA50': data['SMA50'],
                        'RSI': data['RSI']
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
