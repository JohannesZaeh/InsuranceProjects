import numpy as np
import scipy.stats as stats

'''
Calculate optimal reinsurance coverage for a PROPORTIONAL reinsurance by maximizing profit of insurance company under condition that solvency capital
requirement is fulfilled.
alpha = 1 means no reinsurance. alpha = 0 means solvency cannot be reached in any case.
'''

def calc_alpha(ES, SigmaS, u, theta, xi, solvency_level):
    '''
    input:
    ES = expected Claims Amount,
    SigmaS = standard deviation of claims amount,
    u = initial capital,
    theta = safety loading of cedent in percent,
    xi = safety loading of reinsurer in percent,
    solvency_level = for example 0.995
    output:
    alpha = percentage of insured sum the cedent will keep
    '''

    #Get quantile of standard normal distribution
    z = stats.norm.ppf(solvency_level)

    #Formula for alpha derived with central limit theorem
    alpha = (u - (xi - theta) * ES) / (z * SigmaS - xi * ES)

    #If alpha < 0 set alpha = 0; if alpha > 1 set alpha = 1
    alpha = min(max(alpha, 0), 1)

    return alpha


