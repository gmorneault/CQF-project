from __future__ import division
from math import *
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import pickle

import forecast
import vasicek
import black_scholes

# import spot rates
rates = pd.read_csv('data/data - 2012 to 2013.csv')
maturity = np.array(rates.columns).astype(float)

# plot evolution of forward rate term structure for today, 1Y, 5Y, and 10Y
plt.clf()
plt.plot(maturity, rates.ix[[0,25,50,100],:].T)
plt.title('Historic Movements of Forward Rate Term Structure \n Jan 2012 to Dec 2013')
plt.xlabel('Maturity (years)')
plt.ylabel('Rate')
plt.legend(['Today','25 weeks','50 weeks','100 weeks'], loc='lower right')
plt.savefig('figures/historic_forward_rate_term_structure.png', bbox_inches='tight')

# plot 10-year projection of spot, 5Y, and 25Y forward rates
plt.clf()
plt.plot(rates.loc[:,['0.08', '5', '10', '25']])
plt.title('Historic Forward Rate Weekly Movements \n Jan 2012 to Dec 2013')
plt.xlabel('Time (weeks)')
plt.ylabel('Rate')
plt.xlim(xmax=101)
plt.legend(['1M','5Y','10Y','25Y'], loc='best')
plt.savefig('figures/historic_forward_rate_movements.png', bbox_inches='tight')

# Calculate forward rate correlations for the 1M, 5Y, 10Y, and 25Y rates
rates_corr_table = rates.loc[:,['0.08', '5', '10', '25']].corr()
rates_corr_table.to_csv('figures/historic_rates_correlation.csv')

'''
Run PCA analysis
''' 
execfile('pca.py')


'''
Volatility Functions
'''
# Generate volitility functions
act_vol = np.sqrt(pca_val[0:3]) * pca_vect[:,0:3]
act_vol1 = act_vol[:,0]
act_vol2 = act_vol[:,1]
act_vol3 = act_vol[:,2]

# Plot volatility functions
plt.clf()
plt.plot(maturity, act_vol)
plt.title('Volatility Functions')
plt.xlabel('Maturity (years)')
plt.ylabel('Volatility')
plt.legend(['Vol_1','Vol_2','Vol_3'], loc='lower right')
plt.savefig('figures/volitility_functions.png', bbox_inches='tight')

# fit volitility functions
execfile('fit_volatility.py')


'''
Drift Calculation
'''
execfile('drift_calculation.py')


'''
Test Random Number Generators
'''
execfile('test_random_numbers.py')

'''
Starting Values
'''
# Set starting values for simulation
start_values = np.array(pd.read_csv('data/starting_values.csv')) / 100

plt.clf()
plt.plot(maturity, start_values.T)
plt.title('State of Forward Rate Curve at Start of Simulation')
plt.xlabel('Maturity (years)')
plt.ylabel('Rate')
plt.legend(['Today','1Y','5Y','10Y'], loc='lower right')
plt.savefig('figures/forward_rate_term_structure_start.png', bbox_inches='tight')

'''
Single Run Execution
'''
# Set time step and number of years for simulation
dt = 0.01
years = 10

# Generate single instance of forward curve and plot snapshots of forward
# curve at certain times as well as the evolution of certain forward rates
# over the entire time frame
execfile('single_run_execution.py')


'''
Monte Carlo Simulation
'''
''' Part 0 - Set Monte Carlo Parameters '''
# This code should be executed regardless of whether executing
# Part 1 or Part 2 below
num_iter = 10000
tau = 1
expiry = np.arange(1.0, 10.5, 0.5).astype(str)
K = np.arange(0.01, 0.05, 0.001)

''' Part 1 - Initial MC Run '''
# Note that MC does not need to be run every time
# To pull in results from previous MC run see Part 2 below

total_start_time = time.time()

# Execute numpy implementation
numpy_start_time = time.time()
execfile('monte_carlo_numpy.py')
numpy_end_time = time.time()

# Execute numpy implementation
sobol_start_time = time.time()
seed = 1
execfile('monte_carlo_sobol.py')
sobol_end_time = time.time()

total_end_time = time.time()

# Compute processsing time for both MC methods
numpy_time = numpy_end_time - numpy_start_time
sobol_time = sobol_end_time - sobol_start_time
total_time = total_end_time - total_start_time

# Print process time results
print 'Numpy Process Time: %.3f seconds' % numpy_time
print 'Sobol Process Time: %.3f seconds' % sobol_time
print 'Total Process Time: %.3f seconds' % total_time

''' Part 2 - Pull in saved results from a previous MC Run '''
# Used only for recovering saved datasets after 10,000 simulation run
# so that MC does not need to be run every time

# Load Numpy Execution
avg_L_numpy = pickle.load(open('data/avg_L_numpy.pkl', 'rb'))
avg_Z_numpy = pickle.load(open('data/avg_Z_numpy.pkl', 'rb'))
caplet_hist_numpy = pickle.load(open('data/caplet_hist_numpy.pkl', 'rb'))
flrlet_hist_numpy = pickle.load(open('data/flrlet_hist_numpy.pkl', 'rb'))
avg_caplet_numpy = pickle.load(open('data/avg_caplet_numpy.pkl', 'rb'))
avg_flrlet_numpy = pickle.load(open('data/avg_flrlet_numpy.pkl', 'rb'))
avg_IV_cap_numpy = pickle.load(open('data/avg_IV_cap_numpy.pkl', 'rb'))
avg_IV_flr_numpy = pickle.load(open('data/avg_IV_flr_numpy.pkl', 'rb'))

# Load Sobol Execution
avg_L_sobol = pickle.load(open('data/avg_L_sobol.pkl', 'rb'))
avg_Z_sobol = pickle.load(open('data/avg_Z_sobol.pkl', 'rb'))
caplet_hist_sobol = pickle.load(open('data/caplet_hist_sobol.pkl', 'rb'))
flrlet_hist_sobol = pickle.load(open('data/flrlet_hist_sobol.pkl', 'rb'))
avg_caplet_sobol = pickle.load(open('data/avg_caplet_sobol.pkl', 'rb'))
avg_flrlet_sobol = pickle.load(open('data/avg_flrlet_sobol.pkl', 'rb'))
avg_IV_cap_sobol = pickle.load(open('data/avg_IV_cap_sobol.pkl', 'rb'))
avg_IV_flr_sobol = pickle.load(open('data/avg_IV_flr_sobol.pkl', 'rb'))


'''
Plots for Numpy and Sobol executions
''' 
execfile('plots_numpy.py')
execfile('plots_sobol.py')


'''
Calibrate Vasicek model and calculate price for different maturities
'''
execfile('calibrate_vasicek.py')

'''
Plot comparsons for bond prices
'''
# Plot Numpy and Sobol versus Vasicek
plt.clf()    
plt.plot(expiry, Z_vasicek)
plt.plot(expiry, avg_Z_numpy, '--')
plt.plot(expiry, avg_Z_sobol, ':')
plt.title('Comparison of Bond Prices')
plt.xlabel('Maturity (Years)')
plt.ylabel('Price')
plt.legend(['Vasicek','Numpy','Sobol'], loc='best')
plt.savefig('figures/bond_prices_with_vasicek.png', bbox_inches='tight')

# Plot difference between Numpy and Sobol
plt.clf()
plt.plot(expiry, avg_Z_numpy - avg_Z_sobol)
plt.title('Bond Price Difference \n Numpy minus Sobol ')
plt.xlabel('Maturity (Years)')
plt.ylabel('Price Difference')
plt.savefig('figures/bond_prices_difference.png', bbox_inches='tight')