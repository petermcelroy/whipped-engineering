import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def backtest_strategy(ticker, start_date, end_date, short_window, long_window, initial_investment):
    """
    Performs a backtest of a simple moving average crossover strategy.

    :param ticker: The stock ticker symbol (e.g., 'AAPL').
    :param start_date: The start date for the backtest (e.g., '2020-01-01').
    :param end_date: The end date for the backtest (e.g., '2023-01-01').
    :param short_window: The window size for the short moving average.
    :param long_window: The window size for the long moving average.
    :param initial_investment: The initial amount of money to invest.
    :return: A DataFrame with the backtest results.
    """
    # 1. Download data
    data = yf.download(ticker, start=start_date, end=end_date)

    # 2. Calculate moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

    # Drop rows with NaN values
    data.dropna(inplace=True)

    # 3. Generate trading signals
    data['Signal'] = 0.0
    data['Signal'] = pd.np.where(data['Short_MA'] > data['Long_MA'], 1.0, 0.0)
    data['Position'] = data['Signal'].diff()

    # 4. Calculate strategy returns and cumulative returns
    data['Daily_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Daily_Return'] * data['Position'].shift(1)
    
    # Calculate cumulative returns
    data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()
    data['Buy_and_Hold'] = (1 + data['Daily_Return']).cumprod()

    # 5. Plot results
    plt.figure(figsize=(12, 8))
    plt.plot(data['Cumulative_Return'], label='Strategy Cumulative Return')
    plt.plot(data['Buy_and_Hold'], label='Buy and Hold Cumulative Return')
    plt.title(f'Moving Average Crossover Strategy Backtest for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.show()

    return data

if __name__ == '__main__':
    # Run the backtest with example parameters
    backtest_results = backtest_strategy(
        ticker='SPY',  # Changed from 'AAPL' to 'SPY'
        start_date='2020-01-01',
        end_date='2023-01-01',
        short_window=50,
        long_window=200,
        initial_investment=100000.0
    )

    print("\nBacktest Results:")
    print(backtest_results.tail())
