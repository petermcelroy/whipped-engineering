import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_comps(ticker, start_date, end_date, drop_threshold):
    """
    Performs a backtest of a 'single entry' strategy based on a price drop from a high.
    A single buy signal is triggered after a percentage drop.
    Profit is taken when the price returns to the original high.

    :param ticker: The stock ticker symbol (e.g., 'SPY').
    :param start_date: The start date for the backtest.
    :param end_date: The end date for the backtest.
    :param drop_threshold: The percentage drop required to trigger the buy (e.g., 0.05 for 5%).
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
    
    # Use lists to store signals and trade results
    signals = pd.Series(index=strategy_data.index, dtype=float).fillna(0.0)
    trade_results = []
    
    # State variables to manage the backtest
    original_high = -1.0
    
    # A dictionary to hold the details of the single open trade
    current_trade = None

    # Amount to invest per trade
    investment_per_trade = 1000.0
    
    # Set the leverage factor
    leverage_factor = 3.0

    # Set the daily depreciation rate (0.01%)
    daily_depreciation_rate = 0.0001
    
    # Iterate through the data to find all potential trades
    for i in range(1, len(strategy_data)):
        current_close = strategy_data.iloc[i]['Close']
        
        # Check for a new all-time high to reset our high-water mark
        if current_close > original_high:
            original_high = current_close
            
            # Check for a complete recovery on the open trade and take profit
            if current_trade:
                shares = investment_per_trade / current_trade['entry_price']
                
                # Calculate gross profit
                gross_profit = shares * (current_close - current_trade['entry_price'])
                
                # Calculate depreciation
                days_held = (strategy_data.index[i] - current_trade['entry_date']).days
                depreciation_cost = investment_per_trade * daily_depreciation_rate * days_held
                
                # Calculate final profit
                final_profit = (gross_profit - depreciation_cost) * leverage_factor
                
                trade_results.append({
                    'entry_date': current_trade['entry_date'],
                    'exit_date': strategy_data.index[i],
                    'entry_price': current_trade['entry_price'],
                    'exit_price': current_close,
                    'profit': final_profit,
                    'gross_profit': gross_profit * leverage_factor,
                    'depreciation_cost': depreciation_cost * leverage_factor,
                    'percent_from_ath': (current_trade['entry_price'] - current_trade['ath_at_entry']) / current_trade['ath_at_entry'],
                    'percent_profit': (current_close - current_trade['entry_price']) / current_trade['entry_price'],
                    'ath_at_entry': current_trade['ath_at_entry']
                })
                
                # Mark a sell signal
                signals.loc[strategy_data.index[i]] = -1.0
                
                # Reset the open trade
                current_trade = None

        # Check for a new buy signal (price crosses the drop threshold)
        buy_price_threshold = original_high * (1 - drop_threshold)
        if current_close <= buy_price_threshold and not current_trade:
            entry_price = current_close
            current_trade = {
                'entry_date': strategy_data.index[i],
                'entry_price': entry_price,
                'ath_at_entry': original_high
            }
            signals.loc[strategy_data.index[i]] = 1.0
            
    # 4. Calculate strategy value
    initial_investment = 1000.0
    strategy_value = [initial_investment]
    
    current_strategy_value = initial_investment
    
    trade_exit_dates = {trade['exit_date']: {'profit': trade['profit']} for trade in trade_results}
    
    for i in range(1, len(strategy_data)):
        date = strategy_data.index[i]
        
        # Calculate Strategy value based on profits
        if date in trade_exit_dates:
            profit = trade_exit_dates[date]['profit']
            current_strategy_value += profit
            
        strategy_value.append(current_strategy_value)

    strategy_data['Strategy_Value'] = strategy_value
    
    return strategy_data

if __name__ == '__main__':
    # Define the parameters for the comparative backtest
    ticker = 'SPY'
    start_date = '2010-01-01'
    end_date = '2020-01-01'
    drop_thresholds = [0.01, 0.03, 0.06, 0.09]
    
    plt.figure(figsize=(12, 8))
    
    # Store final results for the summary table
    final_results = []
    
    # Run the backtest for each drop threshold and plot the results
    for drop in drop_thresholds:
        results = backtest_comps(ticker, start_date, end_date, drop)
        if results is not None:
            plt.plot(results['Strategy_Value'], label=f'Strategy ({int(drop*100)}% Drop)')
            final_results.append({
                'Strategy': f'{int(drop*100)}% Drop',
                'Final Value': results['Strategy_Value'].iloc[-1]
            })

    # Run and plot the buy and hold baseline
    buy_and_hold_data = yf.download(ticker, start=start_date, end=end_date)
    buy_and_hold_value = (1 + buy_and_hold_data['Close'].pct_change().fillna(0)).cumprod() * 1000
    plt.plot(buy_and_hold_value, label='Buy and Hold Value', color='gray', linestyle='--')
    final_results.append({
        'Strategy': 'Buy and Hold',
        'Final Value': buy_and_hold_value.iloc[-1]
    })

    plt.title(f'Comparative Backtest for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Create and display the summary table using matplotlib
    summary_df = pd.DataFrame(final_results)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    
    # Format the 'Final Value' column for display
    summary_df['Final Value'] = summary_df['Final Value'].apply(lambda x: f'${float(x):.2f}')
    
    table_data = summary_df.values
    col_labels = summary_df.columns
    
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    
    ax.set_title('Final Portfolio Value Comparison', fontsize=16, fontweight='bold')
    
    plt.show()
