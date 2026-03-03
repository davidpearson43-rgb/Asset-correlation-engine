# Asset Correlation & Statistical Entanglement 

This is the second project in my transition from corporate finance forecasting to quantitative Python development. 

While my first project measured the internal volatility of a single asset, this script analyses the interaction between *two* assets. By calculating their correlation coefficient, we can mathematically prove if two stocks (like Exxon and Chevron) move in lockstep due to shared macroeconomic factors. This type of analysis is the foundational mathematics behind Pairs Trading and Statistical Arbitrage.

## The Math & Logic

To measure the entanglement accurately, the script first converts raw prices into stationary, continuous logarithmic returns. Then, it applies two statistical concepts:

**1. Pearson Correlation Coefficient ($\rho$):**
Measures the linear correlation between the two assets' returns, resulting in a value between -1.0 and 1.0.
$$\rho_{X,Y} = \frac{\text{cov}(X,Y)}{\sigma_X \sigma_Y}$$

**2. Linear Regression:**
The script calculates the line of best fit ($y = mx + b$) and plots it over a scatter chart of the daily returns. Outliers far from this regression line represent days where the historical pricing relationship temporarily broke.

## Engineering Features
Coming from an Excel environment where missing data (`#N/A`) can break entire models, I built this script with basic production safeguards:
* **Exception Handling:** Uses a `try... except` block to catch API download failures without crashing the program.
* **Data Scrubbing:** Automatically drops `NaN` values resulting from the return shift calculation to prevent `LinAlgError` failures during the regression math.

## Tools Used
* **Python** * **yfinance** (Multi-asset telemetry)
* **pandas & numpy** (Vectorised math and matrix operations)
* **matplotlib** (Scatter plots and regression lines)

## Usage

The core logic is wrapped in `analyse_asset_correlation()`. Just pass two ticker symbols to generate the correlation matrix and the regression plot.

```python
from correlation_engine import analyse_asset_correlation

# Example: Measure the entanglement of two major energy sector stocks
analyse_asset_correlation("XOM", "CVX", period="1y")
