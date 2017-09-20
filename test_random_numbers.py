

numpy_mean_avg = 0
numpy_std_avg = 0
numpy_time_avg = 0
sobol_mean_avg = 0
sobol_std_avg = 0
sobol_time_avg = 0
seed = int(np.random.uniform(1,1e5))

for i in range(100):
    
    numpy_start_time = time.time()    
    numpy_sample = forecast.rand_numpy(1000)
    numpy_end_time = time.time()
    
    sobol_start_time = time.time()
    (sobol_sample, seed) = forecast.rand_sobol(1000, seed)
    sobol_end_time = time.time()

    numpy_mean = np.mean(numpy_sample)
    numpy_std = np.std(numpy_sample)
    numpy_time = numpy_end_time - numpy_start_time
    sobol_mean = np.mean(sobol_sample)
    sobol_std = np.std(sobol_sample)
    sobol_time = sobol_end_time - sobol_start_time    
    
    numpy_mean_avg = (i*numpy_mean_avg + numpy_mean) / (i+1)
    numpy_std_avg = (i*numpy_std_avg + numpy_std) / (i+1)
    numpy_time_avg = (i*numpy_time_avg + numpy_time) / (i+1)
    sobol_mean_avg = (i*sobol_mean_avg + sobol_mean) / (i+1)
    sobol_std_avg = (i*sobol_std_avg + sobol_std) / (i+1)
    sobol_time_avg = (i*sobol_time_avg + sobol_time) / (i+1)

print 'Average Results from 100 iterations of 1,000 size samples'
print 'Numpy --- Mean: %.5f | Std Dev: %.5f | Time: %.3f' % (numpy_mean_avg, numpy_std_avg, numpy_time_avg)
print 'Sobol --- Mean: %.5f | Std Dev: %.5f | Time: %.3f' % (sobol_mean_avg, sobol_std_avg, sobol_time_avg)

# Plot average Numpy mean and std against 1,000 sample 
plt.clf()
plt.hist(numpy_sample, bins=25, normed=True)
(xmin, xmax) = plt.xlim()
x = np.linspace(xmin, xmax, 100)
numpy_pdf = norm.pdf(x, numpy_mean_avg, numpy_std_avg)
plt.plot(x, numpy_pdf, '--r', linewidth=2)
title = 'Numpy Implementation \n Fit results: mean = %.5f,  std = %.5f' % (numpy_mean_avg, numpy_std_avg)
plt.title(title)
plt.savefig('figures/norm_dist_fit_numpy.png', bbox_inches='tight')

# Plot average Numpy mean and std against 1,000 sample 
plt.clf()
plt.hist(sobol_sample, bins=25, normed=True)
(xmin, xmax) = plt.xlim()
x = np.linspace(xmin, xmax, 100)
sobol_pdf = norm.pdf(x, sobol_mean_avg, sobol_std_avg)
plt.plot(x, sobol_pdf, '--r', linewidth=2)
title = 'Sobol Implementation \n Fit results: mean = %.5f,  std = %.5f' % (sobol_mean_avg, sobol_std_avg)
plt.title(title)
plt.savefig('figures/norm_dist_fit_sobol.png', bbox_inches='tight')