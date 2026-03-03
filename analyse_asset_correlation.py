import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyse_asset_correlation(ticker_a: str, ticker_b: str, period: str = "1y"):
    """
    Fetches historical market data for two assets, calculates their continuous 
    logarithmic returns, and measures their statistical entanglement (correlation).
    
    Parameters:
    ticker_a (str): The first stock ticker (e.g., 'XOM')
    ticker_b (str): The second stock ticker (e.g., 'CVX')
    period (str): The time period to analyze (default is 1 year)
    
    Returns:
    None: Prints the correlation matrix and displays a regression scatter plot.
    """
    tickers = [ticker_a , ticker_b]
    print(f"---Initiating Entanglement Analysis: {ticker_a} vs {ticker_b} ---")
    
    # Telemetry Acuisition & Cleaning
    try: 
        data = yf.download(tickers, period=period, auto_adjust = True, progress = False)['Close']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return 
    if data.empty or len(data.columns) < 2:
        print(f"Error: Incomplete data retrieved. Check ticker symbols.")
        return
    # Continuous Transformation (Velocity)
    # The .dropna() here is a safety net against LinAlgErrors 
    velocity = np.log(data/data.shift(1)).dropna()

    #measure the interation (correlation)
    correlation_matrix = velocity.corr()
    # Extract the specific correlation coefficient 
    rho = correlation_matrix.loc[ticker_a, ticker_b]
    print(f"Data Points Analyzed: {len(velocity)} trading days")
    print(f"Correlation Coefficient (rho): {rho:.4f}\n")

    #signal visulation 
    plt.figure(figsize=(8,8))

    #isolate X and Y axis
    x_returns = velocity[ticker_a]
    y_returns =velocity[ticker_b]

    #scatter plot
    plt.scatter(x_returns, y_returns, alpha = 0.5, color = 'teal' , label = 'Daily Return') 

    # Calculate and plot the physics (Regression Line)
    m, b = np.polyfit(x_returns, y_returns, 1)
    plt.plot(x_returns, m * x_returns + b, color='red', linewidth=2, label=f'Regression (rho={rho:.2f})')
    # Formatting
    plt.title(f"Asset Entanglement: {ticker_a} vs {ticker_b}")
    plt.xlabel(f"{ticker_a} Log Returns")
    plt.ylabel(f"{ticker_b} Log Returns")
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.show()

# --- Execution ---
# Now you can test any pairs instantly!
analyse_asset_correlation("XOM", "CVX", period="1y")
