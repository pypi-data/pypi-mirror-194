
import pandas as pd
import numpy as np

# portfolio A/B/C
def cal_porfolio_price(portfolio,prices,portfolio_="All"):
    if portfolio_=="All":
        a=portfolio.drop('Portfolio',axis=1)
        portfolio_type = a.groupby('Stock', as_index=False).sum('Holding')
    else:
        portfolio_type = portfolio[portfolio["Portfolio"]==portfolio_]
    stock_name = list(portfolio_type["Stock"])
    assets_prices = pd.concat([prices["Date"], prices[stock_name]], axis=1)
    current_price = np.dot(prices[portfolio_type["Stock"]].tail(1), portfolio_type["Holding"])
    holdings = portfolio_type["Holding"]

    return current_price,assets_prices,holdings

# all 
def Norm_price(portfolio,prices,portfolio_='All'):
    if portfolio_=="All":
        a=portfolio.drop('Portfolio',axis=1)
        portfolio_type = a.groupby('Stock', as_index=False).sum('Holding')
    else:
        portfolio_type = portfolio[portfolio["Portfolio"]==portfolio_]
        
    stock_name = list(portfolio_type["Stock"])
    assets_prices = pd.concat([prices["Date"], prices[stock_name]], axis=1)
    current_price = np.dot(prices[portfolio_type["Stock"]].tail(1), portfolio_type["Holding"])

    val = portfolio_type["Holding"].values.reshape(-1,1) * prices[portfolio_type["Stock"]].tail(1).T.values
    hold = val/current_price
   

    return current_price,assets_prices,hold


# specify the method of return calculation
def return_calculate(prices, method = 'Arithmetic'):
    prices_date = prices.Date[1:]
    row = len(prices_date)

    col = prices.columns
    col_new = col.drop('Date')
    le = len(col_new)

    price_new = prices[col_new].to_numpy()

    price_return = np.empty((row,le))

    for i in range(row):
        for j in range(le):
            price_return[i][j] = price_new[i+1][j]/price_new[i][j]


    if method == 'Arithmetic':
        price_return = price_return - 1.0
    elif method == 'Log':
        price_return = np.log(price_return)
    else:
        raise ValueError(f'Wrong method')

    dateColumn = "Date"
    prices_da = pd.DataFrame({dateColumn: prices_date}) 

    for i in range(le):
        prices_da[col_new[i]] = price_return[:,i]
    
    return prices_da