


'''
Numpy
'''
# Generate single forecast and time execution
start_time = time.time()
fwd_rates = forecast.run_numpy(maturity, years, dt, start_values, drift, est_vol1, est_vol2, est_vol3)
end_time = time.time()
numpy_time = end_time - start_time

print 'Numpy Process Time: %.3f seconds' % numpy_time

# plot evolution of forward rate term structure for today, 1Y, 5Y, and 10Y
plt.clf()
plt.plot(maturity, fwd_rates.loc[['0.0', '1.0', '5.0', '10.0'],:].T)
plt.title('Evolution of Forward Rate Term Structure - Numpy Implementation')
plt.xlabel('Maturity (years)')
plt.ylabel('Rate')
plt.legend(['Today','1Y','5Y','10Y'], loc='lower right')
plt.savefig('figures/forward_rate_term_structure_numpy.png', bbox_inches='tight')

# plot 10-year projection of spot, 5Y, and 25Y forward rates
plt.clf()
plt.plot(fwd_rates.loc[:,['0.08', '5.0', '25.0']])
plt.title('Projection of Forward Rates - Numpy Implementation')
plt.xlabel('Time (time step = 0.01)')
plt.ylabel('Rate')
plt.legend(['1M','5Y','25Y'], loc='lower right')
plt.savefig('figures/forward_rate_projections_numpy.png', bbox_inches='tight')

'''
Sobol
'''
seed = int(np.random.uniform(0, 1e5))
# Generate single forecast and time execution
start_time = time.time()
(fwd_rates, seed) = forecast.run_sobol(maturity, years, dt, start_values, drift, est_vol1, est_vol2, est_vol3, seed)
end_time = time.time()
sobol_time = end_time - start_time

print 'Sobol Process Time: %.3f seconds' % sobol_time

# plot evolution of forward rate term structure for today, 1Y, 5Y, and 10Y
plt.clf()
plt.plot(maturity, fwd_rates.loc[['0.0', '1.0', '5.0', '10.0'],:].T)
plt.title('Evolution of Forward Rate Term Structure - Sobol Implementation')
plt.xlabel('Maturity (years)')
plt.ylabel('Rate')
plt.legend(['Today','1Y','5Y','10Y'], loc='lower right')
plt.savefig('figures/forward_rate_term_structure_sobol.png', bbox_inches='tight')

# plot 10-year projection of spot, 5Y, and 25Y forward rates
plt.clf()
plt.plot(fwd_rates.loc[:,['0.08', '5.0', '25.0']])
plt.title('Projection of Forward Rates - Sobol Implementation')
plt.xlabel('Time (time step = 0.01)')
plt.ylabel('Rate')
plt.legend(['1M','5Y','25Y'], loc='lower right')
plt.savefig('figures/forward_rate_projections_sobol.png', bbox_inches='tight')