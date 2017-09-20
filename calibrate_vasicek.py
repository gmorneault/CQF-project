# Pull in historic short term rates
short_rate = rates['0.08'] / 100
time_step = 52 / 365 # 52 weeks divided by 365 days

# Plot histogram of historical rates
plt.clf()
plt.hist(short_rate, bins=50)
plt.title('Distribution of Short Term Rate')
plt.xlabel('Rate')
plt.ylabel('Count')
plt.savefig('figures/rate_distribution.png', bbox_inches='tight')

# Calibrate Vasicek model using ordinary least squares regression 
(x, y, a, b, sd) = vasicek.ols_calibration(short_rate)

# Define linear function with OLS parameters
def line_fit(x):
        return a*x + b

# Generate estimates
y_est = line_fit(x)

# Display goodness of fit
plt.clf()    
plt.plot(x, y, '.b')
plt.plot(x, y_est, '-k')
plt.title('Least Squared Fit to Consective Observations')
plt.xlabel('r(i-1)')
plt.ylabel('r(i)')
plt.legend(['Actual','Fitted'], loc='lower right')
plt.savefig('figures/rate_least_squared.png', bbox_inches='tight')

# Calculate Vasicek parameters
(_lambda_, mu, sigma) = vasicek.calc_params(a, b, sd, time_step)

# Set starting rate for Vasicek execution
r = start_values[0,0]

# Calculate bond prices for each expiry
Z_vasicek = np.zeros(len(expiry))
for (i,), T in np.ndenumerate(expiry.astype(float)):
    Z_vasicek[i] = vasicek.calc_price(r, T, _lambda_, mu, sigma)