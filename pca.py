'''
Calcualte covariance matrix of rate differences
'''
# calculate rate differences
rates_diff = np.log(rates)
rates_diff = rates_diff.diff()
rates_diff.drop(0, inplace=True)

# generate covariance matrix and annualize
# 51 equals 52 weeks in a year - 1 week worth of holidays 
rates_cov = rates_diff.cov() * 51 / 10000

'''
Define array sorting and extracting functions
'''
def combine_and_sort(eig_val, eig_vec):
    # Combine eigenvalues with associated eigenvectors
    eig_pairs = [(eig_val[i], eig_vec[:,i]) for i in range(len(eig_val))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort()
    eig_pairs.reverse()
    
    return eig_pairs

def top(eig_pairs, num):
    # Unpack sorted tuple
    (eig_val, eig_vec) = zip(*eig_pairs)
    
    # Take top eigenvalues and eigenvectors 
    top_val = np.array(eig_val[0:num])
    top_vec = np.array(eig_vec[0:num]).T
    
    return top_val, top_vec
 
   
'''
QR Decomposition Implementation
(For testing and comparing numpy implementation only)
'''
# Calculate eigenvalues and eigenvectors from covariance matrix
A = np.array(rates_cov)
X = A
pQ = np.identity(A.shape[0])

# 30 iterations was concluded to be a sufficient number
for i in range(30):
    (Q, R) = np.linalg.qr(X)
    pQ = np.dot(pQ,Q)
    X = np.dot(R,Q)

eig_val_rates_cov = X.diagonal()
eig_vec_rates_cov = pQ

# Make a list of (eigenvalue, eigenvector) tuples
# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs = combine_and_sort(eig_val_rates_cov, eig_vec_rates_cov)

# Calculate cumlative R squared
sorted_eig_vals = np.array([float(i[0]) for i in eig_pairs])
R_squared = sorted_eig_vals.cumsum()/sorted_eig_vals.sum()
np.savetxt('figures/R_squared - QR Decomposition.csv', R_squared, delimiter=",")

# Through exploratory analysis, determined to take top four
# eigenvalues with associated eigenvectors
(pca_val, pca_vect) = top(eig_pairs, 4)

# Plot top three principal components by maturity
plt.clf()
plt.plot(maturity, pca_vect)
plt.title('Principal Components - QR Decomposition')
plt.xlabel('Maturity (years)')
plt.ylabel('Eigenvector')
plt.ylim((-0.5,0.5))
plt.legend(['PC1','PC2','PC3', 'PC4'], loc='lower right')
plt.savefig('figures/principal_components_qr_decomposition.png', bbox_inches='tight')


'''
Numpy Implementation
'''
# Calculate eigenvalues and eigenvectors from covariance matrix
eig_val_rates_cov, eig_vec_rates_cov = np.linalg.eig(rates_cov)

# Make a list of (eigenvalue, eigenvector) tuples
# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs = combine_and_sort(eig_val_rates_cov, eig_vec_rates_cov)

# Calculate cumlative R squared
sorted_eig_vals = np.array([float(i[0]) for i in eig_pairs])
R_squared = sorted_eig_vals.cumsum()/sorted_eig_vals.sum()
np.savetxt('figures/R_squared - Numpy.csv', R_squared, delimiter=",")

# Through exploratory analysis, determined to take top four
# eigenvalues with associated eigenvectors
(pca_val, pca_vec) = top(eig_pairs, 4)

pca_val = pca_val.astype(float)
pca_vec = pca_vec.astype(float)

# Plot top three principal components by maturity
plt.clf()
plt.plot(maturity, pca_vect)
plt.title('Principal Components - Numpy Method')
plt.xlabel('Maturity (years)')
plt.ylabel('Eigenvector')
plt.ylim((-0.5,0.5))
plt.legend(['PC1','PC2','PC3', 'PC4'], loc='lower right')
plt.savefig('figures/principal_components_numpy.png', bbox_inches='tight')


'''
# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(eig_val_rates_cov[i], eig_vec_rates_cov[:,i]) for i in range(len(eig_val_rates_cov))]


# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort()
eig_pairs.reverse()

# Calculate cumlative R squared
sorted_eig_vals = np.array([float(i[0]) for i in eig_pairs])
R_squared = sorted_eig_vals.cumsum()/sorted_eig_vals.sum()
np.savetxt('figures/sorted_eigenvalues_R_squared.csv', R_squared, delimiter=",")

# Through exploratory analysis, determined to take top three eigenvalues with associated eigenvectors
pca_val = np.hstack((eig_pairs[0][0].reshape(1,1) \
                        ,eig_pairs[1][0].reshape(1,1) \
                        ,eig_pairs[2][0].reshape(1,1) \
                        ,eig_pairs[3][0].reshape(1,1)))
pca_val = pca_val.astype(float)

pca_vect = np.hstack((eig_pairs[0][1].reshape(51,1) \
                        ,eig_pairs[1][1].reshape(51,1) \
                        ,eig_pairs[2][1].reshape(51,1) \
                        ,eig_pairs[3][1].reshape(51,1)))
pca_vect = pca_vect.astype(float)

# Plot top three principal components by maturity
plt.clf()
plt.plot(maturity, pca_vect)
plt.title('Principal Components')
plt.xlabel('Maturity (years)')
plt.ylabel('Eigenvector')
plt.legend(['PC1','PC2','PC3', 'PC4'], loc='lower right')
plt.savefig('figures/principal_components.png', bbox_inches='tight')
'''