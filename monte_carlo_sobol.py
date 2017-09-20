# Initialize discount factor
Z = np.zeros(len(expiry))
avg_Z_sobol = np.zeros(len(expiry))

# Initialize LIBOR rate
L = np.zeros(len(expiry))
avg_L_sobol = np.zeros(len(expiry))

# Initialize caplet
caplet = np.zeros((len(K), len(expiry))) 
avg_caplet_sobol = np.zeros((len(K), len(expiry)))
caplet_hist_sobol = np.empty((len(K),len(expiry),num_iter))

# Initialize floorlet
flrlet = np.zeros((len(K), len(expiry))) 
avg_flrlet_sobol = np.zeros((len(K), len(expiry)))
flrlet_hist_sobol = np.empty((len(K),len(expiry),num_iter))

# Initialize Implied Volatility
avg_IV_cap_sobol = np.empty((len(K),len(expiry)))
avg_IV_flr_sobol = np.empty((len(K),len(expiry)))

# Run monte carlo simulation
for i in range(num_iter):
    
    # Generate a forward curve for 10 years
    (fwd_rates, seed) = forecast.run_sobol(maturity, years, dt, start_values, drift, est_vol1, est_vol2, est_vol3, seed)
    
    # Calculate discount rate, LIBOR, caplet and floorlet values for different expiry years
    for j, yr in enumerate(expiry):
        Z[j] = np.exp(-np.sum(fwd_rates.loc['0.0':yr,'0.08']) * dt)
        L[j] = np.exp(np.sum(fwd_rates.loc[yr,'0.08':'1.0'])/3)-1
        caplet[:,j] = np.array([max(L[j]-k, 0) * Z[j] * tau for k in K])
        flrlet[:,j] = np.array([max(k-L[j], 0) * Z[j] * tau for k in K])
    
    # Compute average discount rate and LIBOR to use in implied volatility computation
    avg_Z_sobol = (i*avg_Z_sobol + Z) / (i+1)    
    avg_L_sobol = (i*avg_L_sobol + L) / (i+1)
    
    # Compute average caplet and floorlet
    avg_caplet_sobol = (i*avg_caplet_sobol + caplet) / (i+1)
    avg_flrlet_sobol = (i*avg_flrlet_sobol + flrlet) / (i+1)           
    
    # Output history to show convergence
    caplet_hist_sobol[:,:,i] = avg_caplet_sobol    
    flrlet_hist_sobol[:,:,i] = avg_flrlet_sobol

# Implied volatility for caplet
for (n, m), cap in np.ndenumerate(avg_caplet_sobol):
    avg_IV_cap_sobol[n,m] = black_scholes.caplet_bisection(tau, avg_Z_sobol[m], avg_L_sobol[m], K[n], 0.01, 2.0, cap, 1e-10)
    if avg_IV_cap_sobol[n,m] > 1.99:
        avg_IV_cap_sobol[n,m] = None

# Implied volatility for floorlet
for (n, m), flr in np.ndenumerate(avg_flrlet_sobol):
    avg_IV_flr_sobol[n,m] = black_scholes.flrlet_bisection(tau, avg_Z_sobol[m], avg_L_sobol[m], K[n], 0.01, 2.0, flr, 1e-10)
    if avg_IV_flr_sobol[n,m] > 1.99:
        avg_IV_flr_sobol[n,m] = None

# Persist output for future use
pickle.dump(avg_L_sobol, open('data/avg_L_sobol.pkl', 'wb'))
pickle.dump(avg_Z_sobol, open('data/avg_Z_sobol.pkl', 'wb'))
pickle.dump(caplet_hist_sobol, open('data/caplet_hist_sobol.pkl', 'wb'))
pickle.dump(flrlet_hist_sobol, open('data/flrlet_hist_sobol.pkl', 'wb'))
pickle.dump(avg_caplet_sobol, open('data/avg_caplet_sobol.pkl', 'wb'))
pickle.dump(avg_flrlet_sobol, open('data/avg_flrlet_sobol.pkl', 'wb'))
pickle.dump(avg_IV_cap_sobol, open('data/avg_IV_cap_sobol.pkl', 'wb'))
pickle.dump(avg_IV_flr_sobol, open('data/avg_IV_flr_sobol.pkl', 'wb'))