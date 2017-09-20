from __future__ import division
import pandas as pd
import numpy as np
import sobol_lib as sobol


'''
Implementation for forward rate forecast
'''
def run(maturity, years, dt, start_values, drift, vol1, vol2, vol3, phi1, phi2, phi3):
    
    N = int(years / dt)
    dt = years / N
    
    df = np.empty((N+1,51))
    df[0,:] = np.array(start_values)

    for i in range(0,N):
        for j in range(0,51):
            df[i+1,j] = df[i,j]
            df[i+1,j] += drift[j]*dt
            df[i+1,j] += (vol1[j]*phi1[i] + vol2[j]*phi2[i] + vol3[j]*phi3[i]) * np.sqrt(dt)
            if j==50:
                df[i+1,j] += (df[i,j] - df[i,j-1]) / (maturity[j] - maturity[j-1]) * dt
            else:
                df[i+1,j] += (df[i,j+1] - df[i,j]) / (maturity[j+1] - maturity[j]) * dt

    fwd_rates = pd.DataFrame(df)
    fwd_rates.index = [str(i) for i in fwd_rates.index/100]
    fwd_rates.columns = [str(i) for i in maturity]
    return fwd_rates

'''
Define Numpy uniform random number implementation
'''
# Define random number generation function
def rand_numpy(N):
    x = 0
    for i in range(12):
        x = x + np.random.uniform(size=N)
    return x - 6

# Wrapper for run function
def run_numpy(maturity, years, dt, start_values, drift, vol1, vol2, vol3):

    N = int(years / dt)
    dt = years / N       
    
    phi1 = rand_numpy(N)
    phi2 = rand_numpy(N)
    phi3 = rand_numpy(N)    
    
    return run(maturity, years, dt, start_values, drift, vol1, vol2, vol3, phi1, phi2, phi3)

'''
Define Numpy unifor random number implementation
'''
# Define random number generation function
def rand_sobol(N, seed):
    x = sobol.i4_sobol_generate(12, N, seed)
    x = x.sum(axis=0) - 6    
    seed = seed + N
    return (x, seed)

# Wrapper for run function
def run_sobol(maturity, years, dt, start_values, drift, vol1, vol2, vol3, seed):
    
    N = int(years / dt)
    dt = years / N          

    (phi1, seed) = rand_sobol(N, seed)
    (phi2, seed) = rand_sobol(N, seed)
    (phi3, seed) = rand_sobol(N, seed)
    
    return (run(maturity, years, dt, start_values, drift, vol1, vol2, vol3, phi1, phi2, phi3), seed)

