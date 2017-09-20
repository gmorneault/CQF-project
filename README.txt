The program can be understood and broken down into the following components:

- main.py - This is the main executable and all other scripts are executed through this program.

Executable Files
----------------
- pca.py - Principal component analysis
- fit_volatility.py - Volatility funtion fitting with polynomials
- drift_calculation.py - Drift Function creation using numerical integration
- test_random_numbers.py - A series of tests performed on the Sobol random number generator
- single_run_execution.py - A single simulation executed for both Numpy and Sobol monte carlo implementations
- monte_carlo_numpy.py - Numpy monte carlo execution
- monte_carlo_sobol.py - Sobol monte carlo execution
- plots_numpy.py - Plots for Numpy monte carlo execution
- plots_sobol.py - Plot for Sobol monte carlo execution
- calibrate_vasicek.py - Calibration file for Vasicek model

Functions
---------
- vasicek.py - For calibration, parameter calculation, and pricing of zero-coupon bonds using the Vasicek model
- forecast.py - Forward curve generation using both Numpy and Sobol monte carlo
- black_scholes.py - For calculating the implied volatility of caplet and floorlets using the bisection method

Note: Monte Carlo execution does not need to be re-run for 10,000 simulations.  If you want to re-create the subsequent plots and calculations, simply skip Part 1 (line 119 in main.py) and proceed to Part 2 (line 148 in main.py)