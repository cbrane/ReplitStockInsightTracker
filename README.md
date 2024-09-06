# Stock Data Visualization App

## Introduction
This Stock Data Visualization App is a powerful tool built with Streamlit that allows users to analyze and visualize stock market data. It provides real-time stock information, interactive charts, technical indicators, news sentiment analysis, and price alerts for multiple stocks simultaneously.

## Features
- Multiple stock comparison
- Real-time stock data fetching using Yahoo Finance API
- Interactive price charts with moving averages (SMA20 and SMA50)
- Relative Strength Index (RSI) chart
- News sentiment analysis for each stock
- Price alert functionality
- Financial data tables with CSV download option

## Prerequisites
- Python 3.7 or higher

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock-data-visualization-app.git
   cd stock-data-visualization-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your NewsAPI key:
   - Sign up for a free API key at [https://newsapi.org/](https://newsapi.org/)
   - Create a file named `.streamlit/secrets.toml` in the project directory
   - Add your API key to the file:
     ```
     NEWSAPI_KEY = "your_api_key_here"
     ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and go to `http://localhost:5000` (or the URL provided in the terminal).

3. Enter stock symbols (comma-separated) in the input field (e.g., AAPL,GOOGL,MSFT).

4. Explore the various features:
   - View real-time stock information
   - Analyze price charts with moving averages
   - Check the RSI indicator
   - Read and analyze recent news sentiment
   - Set price alerts for specific stocks
   - Download financial data as CSV files

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [NewsAPI](https://newsapi.org/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)

## Troubleshooting
If you encounter any issues while running the app, please check the following:
1. Ensure all dependencies are correctly installed.
2. Verify that your NewsAPI key is correctly set in the `.streamlit/secrets.toml` file.
3. Make sure you're using a compatible Python version (3.7 or higher).

For any other problems, please open an issue on the GitHub repository.
