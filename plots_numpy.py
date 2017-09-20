# History for caplet with 0.015 strike and 6Y expiry
# First 500 Simulations
plt.clf()
plt.plot(caplet_hist_numpy[5,10,0:500])
plt.title('Price Convergence of a caplet with 0.015 strike and 6 year expiry \n First 500 simulations')
plt.ylabel('Average Caplet Price')
plt.xlabel('Simulation Number')
plt.ylim(0.007,0.009)
plt.savefig('figures/caplet_price_convergence_numpy_500.png', bbox_inches='tight')

# First 2000 Simulations
plt.clf()
plt.plot(caplet_hist_numpy[5,10,0:2000])
plt.title('Price Convergence of a caplet with 0.015 strike and 6 year expiry \n First 2000 simulations')
plt.ylabel('Average Caplet Price')
plt.xlabel('Simulation Number')
plt.ylim(0.007,0.009)
plt.savefig('figures/caplet_price_convergence_numpy_2000.png', bbox_inches='tight')

# All Simulations
plt.clf()
plt.plot(caplet_hist_numpy[5,10,:])
plt.title('Price Convergence of a caplet with 0.015 strike and 6 year expiry \n All simulations')
plt.ylabel('Average Caplet Price')
plt.xlabel('Simulation Number')
plt.ylim(0.007,0.009)
plt.savefig('figures/caplet_price_convergence_numpy_all.png', bbox_inches='tight')

# 1Y caplet values for 2Y, 5Y, and 10Y maturities by strike 
plt.clf()
plt.plot(K, avg_caplet_numpy[:,[2,8,18]])
plt.title('1Y caplet values for 2Y, 5Y, and 10Y expiries by strike')
plt.ylabel('Caplet Price')
plt.xlabel('Strike')
plt.legend(['2Y','5Y','10Y'], loc='upper right')
plt.savefig('figures/caplet_payoff_numpy.png', bbox_inches='tight')

# 1Y floorlet values for 2Y, 5Y, and 10Y maturities by strike 
plt.clf()
plt.plot(K, avg_flrlet_numpy[:,[2,8,18]])
plt.title('1Y floorlet values for 2Y, 5Y, and 10Y expiries by strike')
plt.ylabel('Floorlet Price')
plt.xlabel('Strike')
plt.legend(['2Y','5Y','10Y'], loc='upper left')
plt.savefig('figures/floorlet_payoff_numpy.png', bbox_inches='tight')

# Volatility surface for caplet with 1Y maturity
# at varying epirations and strikes
fig = plt.figure()
ax = Axes3D(fig)
Y, X = np.meshgrid(expiry.astype(float), K)
ax.plot_wireframe(X, Y, avg_IV_cap_numpy, rstride=1, cstride=1)
ax.set_title('Volatility Surface for Caplet with 1Y Maturity')
ax.set_xlabel('Strike (percent)')
ax.set_ylabel('Expiry (years)')
ax.set_zlabel('Implied Volatility')
ax.azim = 45
plt.savefig('figures/caplet_implied_volatility_numpy.png', bbox_inches='tight')

# Volatility surface for floorlet with 1Y maturity
# at varying epirations and strikes
fig = plt.figure()
ax = Axes3D(fig)
Y, X = np.meshgrid(expiry.astype(float), K)
ax.plot_wireframe(X, Y, avg_IV_flr_numpy, rstride=1, cstride=1)
ax.set_title('Volatility Surface for Floorlet with 1Y Maturity')
ax.set_xlabel('Strike (percent)')
ax.set_ylabel('expiry (years)')
ax.set_zlabel('Implied Volatility')
ax.azim = 135
plt.savefig('figures/floorlet_implied_volatility_numpy.png', bbox_inches='tight')