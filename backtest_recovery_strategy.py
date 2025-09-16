import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_recovery_strategy(ticker, start_date, end_date, drop_threshold, recovery_threshold):
    """
    Performs a backtest of a 'dip-buying' strategy based on price recovery,
    using only the close prices.

    :param ticker: The stock ticker symbol (e.g., 'SPY').
    :param start_date: The start date for the backtest.
    :param end_date: The end date for the backtest.
    :param drop_threshold: The percentage drop required to trigger a watch (e.g., 0.05 for 5%).
    :param recovery_threshold: The percentage of the drop that must be recovered to generate a buy signal.
    :return: A DataFrame with the backtest results.
    """
    # 1. Download data and explicitly select only the 'Close' column
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None
    
    if data.empty:
        print("No data downloaded. Check ticker and date range.")
        return None
    
    # Check for a multi-index and handle it gracefully
    if isinstance(data.columns, pd.MultiIndex):
        close_prices = data['Close'][ticker]
    else:
        close_prices = data['Close']
    
    # Create a new DataFrame for our strategy based only on close prices
    strategy_data = pd.DataFrame(index=close_prices.index)
    strategy_data['Close'] = close_prices
    
    # Calculate high water mark and drawdown
    strategy_data['High_Water_Mark'] = strategy_data['Close'].cummax()
    strategy_data['Drawdown'] = (strategy_data['High_Water_Mark'] - strategy_data['Close']) / strategy_data['High_Water_Mark']
    
    strategy_data['Signal'] = 0.0
    in_position = False
    
    for i in range(1, len(strategy_data)):
        # Check for a new high water mark
        if strategy_data.iloc[i]['Close'] > strategy_data.iloc[i-1]['High_Water_Mark']:
            strategy_data.loc[strategy_data.index[i], 'High_Water_Mark'] = strategy_data.iloc[i]['Close']
            strategy_data.loc[strategy_data.index[i], 'Drawdown'] = 0.0
            
        # Check if we are not in a position
        if not in_position:
            # Check for a drop of more than the threshold
            if strategy_data.iloc[i]['Drawdown'] > drop_threshold:
                # We are now watching for a recovery
                # Check for a recovery of the specified threshold
                recovery_target = strategy_data.iloc[i]['High_Water_Mark'] - (strategy_data.iloc[i]['High_Water_Mark'] * drop_threshold) * recovery_threshold
                if strategy_data.iloc[i]['Close'] >= recovery_target:
                    strategy_data.loc[strategy_data.index[i], 'Signal'] = 1.0  # Buy signal
                    in_position = True
        else: # If we are in a position, look for an exit
            # Simple exit: sell when price falls 1% from current close
            # This is a basic trailing stop-loss
            if strategy_data.iloc[i]['Close'] < strategy_data.iloc[i-1]['Close'] * 0.99:
                strategy_data.loc[strategy_data.index[i], 'Signal'] = -1.0
                in_position = False
    
    # Use ffill() to propagate the last signal forward
    strategy_data['Position'] = strategy_data['Signal'].replace(to_replace=0.0).ffill()
    # Correctly set the position to 0 after a sell signal (-1.0)
    strategy_data['Position'] = np.where(strategy_data['Signal'] == -1.0, 0.0, strategy_data['Position'])

    # 4. Calculate strategy returns and cumulative returns
    strategy_data['Daily_Return'] = strategy_data['Close'].pct_change()
    strategy_data['Strategy_Return'] = strategy_data['Daily_Return'] * strategy_data['Position'].shift(1)
    
    # Calculate cumulative returns
    strategy_data['Cumulative_Return'] = (1 + strategy_data['Strategy_Return']).cumprod()
    strategy_data['Buy_and_Hold'] = (1 + strategy_data['Daily_Return']).cumprod()

    # 5. Plot results
    plt.figure(figsize=(12, 8))
    plt.plot(strategy_data['Cumulative_Return'], label='Strategy Cumulative Return')
    plt.plot(strategy_data['Buy_and_Hold'], label='Buy and Hold Cumulative Return')
    plt.title(f'Close-Only Recovery Strategy Backtest for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.show()

    return strategy_data

if __name__ == '__main__':
    # Run the backtest with the new recovery strategy parameters
    backtest_results = backtest_recovery_strategy(
        ticker='SPY',
        start_date='2010-01-01',
        end_date='2020-01-01',
        drop_threshold=0.05,        # 5% drop
        recovery_threshold=0.5      # 50% recovery of the drop
    )

    if backtest_results is not None:
        print("\nBacktest Results:")
        print(backtest_results.tail())
