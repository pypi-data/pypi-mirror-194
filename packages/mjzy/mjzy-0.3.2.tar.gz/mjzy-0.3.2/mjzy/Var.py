import pandas as pd
import numpy as np
from scipy.stats import norm, t
import scipy.stats as st
from statsmodels.tsa.arima.model import ARIMA
from . import portfolio
from . import covarience_matrix
from . import simulation


# Using a fitted AR(1) model
def ar1_var_es(returns, size=10000, alpha=0.05):
    # Fit AR(1) model to returns
    ar1_model = ARIMA(returns, order=(1, 0, 0)).fit()
    
    # Extract model parameters and residuals
    ar1_coeff = ar1_model.params[0]
    residuals = ar1_model.resid
    sigma = np.std(residuals)
    
    # Compute simulated returns using AR(1) model
    last_return = returns.iloc[-1]
    simulated_returns = ar1_coeff * last_return + sigma * np.random.normal(size=size)
    
    # Compute VaR and ES from simulated returns
    var_ar1 = -np.percentile(simulated_returns, alpha * 100)
    es_ar1 = -np.mean(simulated_returns[simulated_returns <= -var_ar1])
    
    return var_ar1, es_ar1, simulated_returns


# calculate var and es by using historical
def calculate_var_hist(returns, alpha=0.05):
    
    # Compute VaR using historic simulation
    var_hist = -np.percentile(returns, alpha * 100)
    
    # Compute ES using historic simulation and VaR
    es_hist = -np.mean(returns[returns < -var_hist])
    
    # Return VaR, ES, and original returns
    return var_hist, es_hist, returns



# calculate normal var and es
def noramal_VaR_ES(data, size=10000, alpha=0.05):

    # Calculate mean and standard deviation of historical returns
    mu = data.mean().values
    sigma = np.std(data).values

    # Generate simulated returns using the normal distribution with mean and standard deviation
    simu_return = np.random.normal(mu, sigma, size)

    # Sort the simulated returns in ascending order
    simu_return.sort()

    # Calculate the index of the value at risk at the confidence level alpha
    n = int(alpha * len(simu_return))

    # Calculate the indices of the upper and lower values at risk
    iup = int(np.ceil(n))
    idn = int(np.floor(n))

    # Calculate the Value at Risk (VaR) as the average of the upper and lower values
    VaR = -(simu_return[iup] + simu_return[idn])/2

    # Calculate the Expected Shortfall (ES) as the average of all returns below the lower value at risk
    ES = -np.mean(simu_return[0:idn])

    # Return VaR, ES, and the sorted simulated returns
    return VaR, ES, simu_return



# Using a normal distribution with an Exponentially Weighted variance ( )λ=0.94
def normal_weighted(meta ,size=10000,lambda_=0.94, alpha=0.05):
    mean_data=meta.mean()
    sigma = np.sqrt(covarience_matrix.exp_weighted_cov(meta,lambda_=lambda_))
    sigma=sigma[0][0]
    simu_norm = np.random.normal(mean_data,sigma,size)
    var_ew = -np.percentile(simu_norm,alpha*100)
    es_ew = -np.mean(simu_norm[0:var_ew])

    return  var_ew,es_ew,simu_norm

# MLE fitted T distribution
def t_VaR_ES(data, alpha = 0.05,size=10000):

    t_df, t_m, t_s = st.t.fit(data)
    t = st.t.rvs(df = t_df, loc = t_m, scale = t_s, size=size)
    tsim = pd.DataFrame({"tsim": t})
    VaR_T = -st.t.ppf(alpha, df = t_df, loc = t_m, scale = t_s)
    temp = tsim[tsim <= -VaR_T].dropna()
    ES_T = -temp.mean().values
    return VaR_T, ES_T[0] ,t


# Delta Normal VaR
def Delta_Normal_VaR(portfolio_type,prices,lambda_=0.94,portfolio_='All'):
    if portfolio_ == 'All':
        current_price, assets_prices, hold = portfolio.Norm_price(portfolio_type,prices)
    else:
        current_price, assets_prices, hold = portfolio.cal_porfolio_price(portfolio_type,prices,portfolio_=portfolio_)
    ret = portfolio.return_calculate(assets_prices).drop('Date', axis=1)
    cov = covarience_matrix.exp_weighted_cov(ret,lambda_)
    sigm = np.sqrt(np.transpose(hold) @ cov @ hold)
    var = -current_price * norm.ppf(0.05) * sigm


    return current_price[0], var[0][0]



# Normal Monte Carlo vaR

def cal_monte_var(portfolio_type,prices, n=10000,lambda_=0.94,alpha=0.05,portfolio_='All'):
    
    current_price, assets_prices, hold = portfolio.cal_porfolio_price(portfolio_type,prices,portfolio_=portfolio_)


    re_n = portfolio.return_calculate(assets_prices).drop('Date', axis=1)

    re_no = re_n - re_n.mean()

    cov = covarience_matrix.exp_weighted_cov(re_no,lambda_)
  
    np.random.seed(0)
    return_simu = np.add(simulation.multivariate_normal_simulation(cov,n),re_n.mean().values)
    assets_prices = assets_prices.drop('Date',axis=1)
    sp=np.dot(return_simu*assets_prices.tail(1).values.reshape(assets_prices.shape[1],),hold)
    var = -np.percentile(sp, alpha*100)
    es = -np.mean(sp[sp<=-var])

    return current_price[0], var,es,sp

# historical var
def cal_historical(portfolio_type, prices,n=10000,alpha=0.05,portfolio_='All'):
    
    current_price, assets_prices, hold = portfolio.cal_porfolio_price(portfolio_type,prices,portfolio_=portfolio_)
    ret = portfolio.return_calculate(assets_prices).drop('Date', axis=1)
    
    assets_prices = assets_prices.drop('Date',axis=1)
    simu = ret.sample(n,replace=True)
    his_pri = np.dot(simu * assets_prices.tail(1).values.reshape(assets_prices.shape[1]), hold)
    

    var_historical = -np.percentile(his_pri, alpha*100)
    es_historical = -np.mean(his_pri[his_pri <=-var_historical])

    return current_price[0], var_historical, es_historical,his_pri