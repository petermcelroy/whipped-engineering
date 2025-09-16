import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_1000(ticker, start_date, end_date, drop_threshold):
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
                    'gross_profit': gross_profit * leverage_factor, # Store the leveraged gross profit
                    'depreciation_cost': depreciation_cost * leverage_factor, # Store the leveraged depreciation cost
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
            
    strategy_data['Signal'] = signals
    strategy_data['Position'] = strategy_data['Signal'].replace(to_replace=0.0).ffill()

    # 4. Calculate strategy and buy-and-hold values
    initial_investment = 1000.0
    strategy_value = [initial_investment]
    strategy_value_gross = [initial_investment]
    buy_and_hold_value = [initial_investment]
    
    current_strategy_value = initial_investment
    current_strategy_value_gross = initial_investment
    
    trade_exit_dates = {trade['exit_date']: {'profit': trade['profit'], 'gross_profit': trade['gross_profit']} for trade in trade_results}
    
    for i in range(1, len(strategy_data)):
        date = strategy_data.index[i]
        daily_return = strategy_data.iloc[i]['Close'] / strategy_data.iloc[i-1]['Close'] - 1
        
        # Calculate Buy and Hold value
        buy_and_hold_value.append(buy_and_hold_value[-1] * (1 + daily_return))
        
        # Calculate Strategy value based on profits
        if date in trade_exit_dates:
            profit = trade_exit_dates[date]['profit']
            current_strategy_value += profit
            
            gross_profit = trade_exit_dates[date]['gross_profit']
            current_strategy_value_gross += gross_profit
            
        strategy_value.append(current_strategy_value)
        strategy_value_gross.append(current_strategy_value_gross)

    strategy_data['Strategy_Value'] = strategy_value
    strategy_data['Strategy_Value_Gross'] = strategy_value_gross
    strategy_data['Buy_and_Hold_Value'] = buy_and_hold_value

    # 5. Plot results
    plt.figure(figsize=(12, 8))
    plt.plot(strategy_data['Strategy_Value'], label='Strategy Value (w/ Depreciation)', color='blue')
    plt.plot(strategy_data['Strategy_Value_Gross'], label='Strategy Value (Gross)', color='blue', linestyle='--')
    plt.plot(strategy_data['Buy_and_Hold_Value'], label='Buy and Hold Value', color='gray', linestyle='--')
    
    # Add markers for the buy and sell signals
    buy_signals = strategy_data.loc[strategy_data['Signal'] == 1.0]
    plt.scatter(buy_signals.index, buy_signals['Buy_and_Hold_Value'], marker='^', color='green', s=100, label='Buy Signal')
    
    sell_signals = strategy_data.loc[strategy_data['Signal'] == -1.0]
    plt.scatter(sell_signals.index, sell_signals['Buy_and_Hold_Value'], marker='v', color='red', s=100, label='Sell Signal')
    
    # Add notes to the main graph
    ax = plt.gca()
    plt.text(0.02, 0.98,
             f'Buy Condition: A new trade is entered after a {int(drop_threshold*100)}% drop\n from the original high.',
             ha='left', va='top', fontsize=10, transform=ax.transAxes,
             bbox=dict(facecolor='green', alpha=0.1))
    plt.text(0.02, 0.90,
             f'Sell Condition: All open trades are exited when the price\n returns to the original high.',
             ha='left', va='top', fontsize=10, transform=ax.transAxes,
             bbox=dict(facecolor='red', alpha=0.1))
    plt.text(0.02, 0.82,
             f'Additional Cost: A daily {daily_depreciation_rate*100:.2f}% depreciation is applied\n to the held investments.',
             ha='left', va='top', fontsize=10, transform=ax.transAxes,
             bbox=dict(facecolor='yellow', alpha=0.1))

    plt.title(f'Single Entry Strategy Backtest for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    
    # 6. Plot trade performance
    if trade_results:
        trade_profits = pd.DataFrame(trade_results)
        
        plt.figure(figsize=(12, 8))
        plt.bar(range(len(trade_profits)), trade_profits['profit'], color='green')
        plt.title(f'Profit per Trade ($) with {leverage_factor}x Leverage')
        plt.xlabel('Trade Number')
        plt.ylabel('Profit ($)')
        plt.grid(axis='y', linestyle='--')

    # 7. Plot recovery time histogram
    recovery_times_days = [(t['exit_date'] - t['entry_date']).days for t in trade_results]
    if recovery_times_days:
        plt.figure(figsize=(10, 6))
        plt.hist(recovery_times_days, bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Recovery Times')
        plt.xlabel('Recovery Time (Trading Days)')
        plt.ylabel('Frequency')
        plt.grid(True)
    
    # 8. Create a table for the trade summary
    if trade_results:
        trade_df = pd.DataFrame(trade_results)
        
        # Calculate the running total
        trade_df['running_total'] = trade_df['profit'].cumsum()
        
        # Create a new figure and axis for the table
        fig, ax = plt.subplots(figsize=(16, len(trade_df) * 0.3 + 1))
        ax.axis('off')  # Hide the axes
        
        # Prepare data for the table
        table_data = trade_df[['entry_date', 'exit_date', 'ath_at_entry', 'entry_price', 'exit_price', 'percent_from_ath', 'percent_profit', 'depreciation_cost', 'profit', 'running_total']].copy()
        table_data.columns = ['Entry Date', 'Exit Date', 'Previous ATH', 'Price at Buy', 'Price at Sell', '% from ATH', '% Profit', 'Depreciation ($)', 'Profit ($)', 'Running Total ($)']
        
        # Format the values for display
        for col in ['Previous ATH', 'Price at Buy', 'Price at Sell', 'Depreciation ($)', 'Profit ($)', 'Running Total ($)']:
            table_data[col] = table_data[col].apply(lambda x: f'${x:.2f}')
        table_data['% from ATH'] = table_data['% from ATH'].apply(lambda x: f'{x:.2%}')
        table_data['% Profit'] = table_data['% Profit'].apply(lambda x: f'{x:.2%}')
        table_data['Entry Date'] = pd.to_datetime(trade_df['entry_date']).dt.strftime('%Y-%m-%d')
        table_data['Exit Date'] = pd.to_datetime(trade_df['exit_date']).dt.strftime('%Y-%m-%d')

        table = ax.table(cellText=table_data.values,
                         colLabels=table_data.columns,
                         loc='center',
                         cellLoc='center',
                         colColours=['#f5f5f5'] * len(table_data.columns))
        
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
        
        ax.set_title('Trade-by-Trade Breakdown', fontweight='bold', fontsize=16)
        
    plt.show()

    # 9. Print trade summary to the console (optional but useful)
    if trade_results:
        print("\n--- Trade Summary ---")
        print(f"Total trades completed: {len(trade_results)}")
        print(f"Average profit per trade: ${np.mean([t['profit'] for t in trade_results]):.2f}")
    else:
        print("\nNo trades were detected with these parameters.")

    return strategy_data

if __name__ == '__main__':
    # Run the backtest with the new single entry strategy parameters
    backtest_results = backtest_1000(
        ticker='SPY',
        start_date='2010-01-01',
        end_date='2020-01-01',
        drop_threshold=0.05,        # A single buy for a 5% drop
    )

    if backtest_results is not None:
        print("\nBacktest Results:")
        print(backtest_results.tail())
