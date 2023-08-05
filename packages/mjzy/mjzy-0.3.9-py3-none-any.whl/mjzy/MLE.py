import numpy as np
from scipy.stats import t
from scipy.optimize import minimize

def negative_log_likelihood_t(params, returns):

    degrees_of_freedom, mean, standard_deviation = params
    return -1 * np.sum(t.logpdf(returns, df=degrees_of_freedom, loc=mean, scale=standard_deviation))

def fit_t_distribution(returns):
    # Define constraints for the optimization problem: degrees of freedom must be greater than 1, standard deviation must be positive
    constraints = [{"type": "ineq", "fun": lambda x: x[0] - 1}, {"type": "ineq", "fun": lambda x: x[2]}]
    # Use scipy.optimize.minimize to minimize the negative log-likelihood, starting with initial guesses of mean, standard deviation, and degrees of freedom
    optimized = minimize(negative_log_likelihood_t, x0=[10, np.mean(returns), np.std(returns)], args=returns, constraints=constraints)
    # Extract the optimized degrees of freedom, mean, and standard deviation
    degrees_of_freedom, mean, standard_deviation = optimized.x
    return degrees_of_freedom, mean, standard_deviation
