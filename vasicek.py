from __future__ import division
import numpy as np

def ols_calibration(x):
    y = x.drop(0)
    y.reset_index(drop=True, inplace=True)
    x = x.drop(len(x)-1)
    
    n = len(x)
    
    Sx = x.sum()
    Sy = y.sum()
    Sxx = (x**2).sum()
    Syy = (y**2).sum()
    Sxy = (x*y).sum()
    
    a = (n*Sxy - Sx*Sy) / (n*Sxx - Sx**2)
    b = (Sy - a*Sx) / n
    sd = np.sqrt((n*Syy - Sy**2 - a*(n*Sxy - Sx*Sy)) / (n*(n-2)))
    
    return (x, y, a, b, sd)    
    
def calc_params(a, b, sd, time_step):
    _lambda_ = -np.log(a) / time_step
    mu = b / (1-a)
    sigma = sd * np.sqrt((-2*np.log(a))/time_step/(1-a**2))
    
    return (_lambda_, mu, sigma)

def calc_price(r, T, _lambda_, mu, sigma):
    t = 0
    B = (1 - np.exp(-_lambda_*(T-t))) / _lambda_
    A = np.exp((B - T + t)*(_lambda_**2*mu - sigma**2/2)/(_lambda_**2) - (sigma**2)*(B**2)/(4*_lambda_))

    return A* np.exp(-B*r)