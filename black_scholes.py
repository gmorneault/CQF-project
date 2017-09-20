from __future__ import division
from math import *
from scipy.stats import norm

def caplet(tau, Z, L, K, IV):
        
    d1 = (log(L/K) + 0.5*(IV**2)*tau)/(IV*sqrt(tau))
    d2 = (log(L/K) - 0.5*(IV**2)*tau)/(IV*sqrt(tau))
    
    Bl = L*norm.cdf(d1) - K*norm.cdf(d2)
    return Bl * Z * tau / (1+L*tau)

def caplet_bisection(tau, Z, L, K, a, b, target, tol):
    c = (a+b)/2.0
    while (b-a)/2.0 > tol:
        if caplet(tau, Z, L, K, c) == target:
            return c
        elif (caplet(tau, Z, L, K, a)-target)*(caplet(tau, Z, L, K, c)-target) < 0:
            b = c
        else :
            a = c
        c = (a+b)/2.0
    return c


def flrlet(tau, Z, L, K, IV):
        
    d1 = (log(L/K) + 0.5*(IV**2)*tau)/(IV*sqrt(tau))
    d2 = (log(L/K) - 0.5*(IV**2)*tau)/(IV*sqrt(tau))
    
    Bl = K*norm.cdf(-d2) - L*norm.cdf(-d1)
    return Bl * Z * tau / (1+L*tau)

def flrlet_bisection(tau, Z, L, K, a, b, target, tol):
    c = (a+b)/2.0
    while (b-a)/2.0 > tol:
        if flrlet(tau, Z, L, K, c) == target:
            return c
        elif (flrlet(tau, Z, L, K, a)-target)*(flrlet(tau, Z, L, K, c)-target) < 0:
            b = c
        else :
            a = c
        c = (a+b)/2.0
    return c