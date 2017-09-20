def m(tau):
    if tau==0:
        return 0
    else:
        dTau = 0.01
        N = int(tau / dTau)
        dTau = tau / N

        #using trapezium rule to compute M1
        M1 = 0.5 * vol1(0)
        for i in range(1,N):
            M1 = M1 + vol1(i * dTau) #not adjusted by *0.5 because of repeating terms x1...xn-1 - see trapezoidal rule
        M1 = M1 + 0.5 * vol1(tau)
        M1 = M1 * dTau
        M1 = vol1(tau) * M1 #Vol_1 represents v_i(t,T) and M1 represents the result of numerical integration

        #using trapezium rule to compute M2
        M2 = 0.5 * vol2(0)
        for i in range(1,N):
            M2 = M2 + vol2(i * dTau)
        M2 = M2 + 0.5 * vol2(tau)
        M2 = M2 * dTau
        M2 = vol2(tau) * M2

        #using trapezium rule to compute M3
        M3 = 0.5 * vol3(0)
        for i in range(1,N):
            M3 = M3 + vol3(i * dTau)
        M3 = M3 + 0.5 * vol3(tau)
        M3 = M3 * dTau
        M3 = vol2(tau) * M3

        return M1 + M2 + M3 #sum for multi-factor

# Calculate Drift
drift = [m(i) for i in maturity]

# Plost Drift to show monotonicity
plt.clf()
plt.plot(maturity, drift)
plt.title('Drift by Maturity')
plt.xlabel('Maturity (years)')
plt.ylabel('Rate')
plt.savefig('figures/drift_function.png', bbox_inches='tight')
