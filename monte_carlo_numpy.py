# Initialize discount factor
Z = np.zeros(len(expiry))
avg_Z_numpy = np.zeros(len(expiry))

# Initialize LIBOR rate
L = np.zeros(len(expiry))
avg_L_numpy = np.zeros(len(expiry))

# Initialize caplet
caplet = np.zeros((len(K), len(expiry))) 
avg_caplet_numpy = np.zeros((len(K), len(expiry)))
caplet_hist_numpy = np.empty((len(K),len(expiry),num_iter))

# Initialize floorlet
flrlet = np.zeros((len(K), len(expiry))) 
avg_flrlet_numpy = np.zeros((len(K), len(expiry)))
flrlet_hist_numpy = np.empty((len(K),len(expiry),num_iter))

# Initialize Implied Volatility
avg_IV_cap_numpy = np.empty((len(K),len(expiry)))
avg_IV_flr_numpy = np.empty((len(K),len(expiry)))

# Run monte carlo simulation
for i in range(num_iter):
    
    # Generate a forward curve for 10 years
    fwd_rates = forecast.run_numpy(maturity, years, dt, start_values, drift, est_vol1, est_vol2, est_vol3)
    
    # Calculate discount rate, LIBOR, caplet and floorlet values for different expiry years
    for j, yr in enumerate(expiry):
        Z[j] = np.exp(-np.sum(fwd_rates.loc['0.0':yr,'0.08']) * dt)
        L[j] = np.exp(np.sum(fwd_rates.loc[yr,'0.08':'1.0'])/3)-1
        caplet[:,j] = np.array([max(L[j]-k, 0) * Z[j] * tau for k in K])
        flrlet[:,j] = np.array([max(k-L[j], 0) * Z[j] * tau for k in K])
    
    # Compute average discount rate and LIBOR to use in implied volatility computation
    avg_Z_numpy = (i*avg_Z_numpy + Z) / (i+1)    
    avg_L_numpy = (i*avg_L_numpy + L) / (i+1)
    
    # Compute average caplet and floorlet
    avg_caplet_numpy = (i*avg_caplet_numpy + caplet) / (i+1)
    avg_flrlet_numpy = (i*avg_flrlet_numpy + flrlet) / (i+1)           
    
    # Output history to show convergence
    caplet_hist_numpy[:,:,i] = avg_caplet_numpy    
    flrlet_hist_numpy[:,:,i] = avg_flrlet_numpy

# Implied volatility for caplet
for (n, m), cap in np.ndenumerate(avg_caplet_numpy):
    avg_IV_cap_numpy[n,m] = black_scholes.caplet_bisection(tau, avg_Z_numpy[m], avg_L_numpy[m], K[n], 0.01, 2.0, cap, 1e-10)
    if avg_IV_cap_numpy[n,m] > 1.99:
        avg_IV_cap_numpy[n,m] = None

# Implied volatility for floorlet
for (n, m), flr in np.ndenumerate(avg_flrlet_numpy):
    avg_IV_flr_numpy[n,m] = black_scholes.flrlet_bisection(tau, avg_Z_numpy[m], avg_L_numpy[m], K[n], 0.01, 2.0, flr, 1e-10)
    if avg_IV_flr_numpy[n,m] > 1.99:
        avg_IV_flr_numpy[n,m] = None

# Persist output for future use
pickle.dump(avg_L_numpy, open('data/avg_L_numpy.pkl', 'wb'))
pickle.dump(avg_Z_numpy, open('data/avg_Z_numpy.pkl', 'wb'))
pickle.dump(caplet_hist_numpy, open('data/caplet_hist_numpy.pkl', 'wb'))
pickle.dump(flrlet_hist_numpy, open('data/flrlet_hist_numpy.pkl', 'wb'))
pickle.dump(avg_caplet_numpy, open('data/avg_caplet_numpy.pkl', 'wb'))
pickle.dump(avg_flrlet_numpy, open('data/avg_flrlet_numpy.pkl', 'wb'))
pickle.dump(avg_IV_cap_numpy, open('data/avg_IV_cap_numpy.pkl', 'wb'))
pickle.dump(avg_IV_flr_numpy, open('data/avg_IV_flr_numpy.pkl', 'wb'))