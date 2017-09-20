'''
Fit volatility functions with polynomials of varying degrees
'''
# Fit volitility functions
p_vol1 = np.polyfit(maturity, act_vol1, 0)
p_vol2 = np.polyfit(maturity, act_vol2, 2)
p_vol3 = np.polyfit(maturity, act_vol3, 3)

# Define volitility functions with polynomial parameters
def vol1(tau):
    return np.polyval(p_vol1, tau)

def vol2(tau):
    return np.polyval(p_vol2, tau)

def vol3(tau):
    return np.polyval(p_vol3, tau)

# Calculate fitted values
est_vol1 = vol1(maturity)
est_vol2 = vol2(maturity)
est_vol3 = vol3(maturity)

# Print plots of each volitility function against fitted values
# First volatility function
plt.clf()
plt.plot(maturity, act_vol1, '-')
plt.plot(maturity, est_vol1, '--')
plt.title('Fit for first volatility function')
plt.xlabel('Maturity (years)')
plt.ylabel('Volatility')
plt.legend(['Actual','Fitted'], loc='lower right')
plt.savefig('figures/volatility_fit_1.png', bbox_inches='tight')

# Second volatility function
plt.clf()
plt.plot(maturity, act_vol2, '-')
plt.plot(maturity, est_vol2, '--')
plt.title('Fit for second volatility function')
plt.xlabel('Maturity (years)')
plt.ylabel('Volatility')
plt.legend(['Actual','Fitted'], loc='lower right')
plt.savefig('figures/volatility_fit_2.png', bbox_inches='tight')

# Third volatility function
plt.clf()
plt.plot(maturity, act_vol3, '-')
plt.plot(maturity, est_vol3, '--')
plt.title('Fit for third volatility function')
plt.xlabel('Maturity (years)')
plt.ylabel('Volatility')
plt.legend(['Actual','Fitted'], loc='lower right')
plt.savefig('figures/volatility_fit_3.png', bbox_inches='tight')