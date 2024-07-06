import scipy.io
import scipy.stats as stats
import math
import numpy as np

from utils import load_data
from utils import trim_qxt


def lee_carter_model(data, timespan, confidence_level, *args):
    '''
    intput: path to mortality data (.txt file, seperated by tabs, first column contains years),time horizon, confidence level,
            if required you can trim data here to e.p. only look at certain years/ages from the input. In that case,
            input as *args: start_date,end_date,start_age,end_age,start_age_data
    output: prediction intervals for each year of the timespan
    '''

    print("Starting Lee-Carter-Model")

    qxt_dict = load_data(data)

    if len(args) == 0:
        qxt = trim_qxt(qxt_dict)
    elif len(args) == 5:
        qxt = trim_qxt(qxt_dict, args[0], args[1], args[2], args[3], args[4])
    else:
        print("invalid number of arguments.")
        return 1

    print("Fitting model...")

    [A, alpha, beta, kappa] = estimate_parameters(qxt)

    [log_m_model, goodness_of_fit] = calculate_model(A, alpha, beta, kappa)

    print(f"Goodness of fit: {goodness_of_fit}")

    prediction_intervals = project_mortality(log_m_model, beta, kappa, timespan, confidence_level)

    return prediction_intervals


def estimate_parameters(qxt):
    '''
    Input: death probabilities as 2-dimensional list (here the format of the input is essential, rows are years and columns are ages)
    Output: The matrix A, which is important for later calculations.
            The Parameters as lists, alpha (one alpha for each age), beta (one beta for each age), kappa (one kappa for each observation year)
    '''
    qxt = np.array(qxt)
    qxt = np.transpose(qxt)
    # Create the matrix pxt; pxt = 1-qxt
    pxt = 1 - qxt
    # Calculate μx(t)
    m = -1 * np.log(pxt)
    # A = log(m)
    A = np.log(m)
    # ax = mean(Ax)
    alpha = np.mean(A, axis=1)
    # Calculate the matrix A-alpha, it's not so straightforward because it is along the rows. A is a matrix with x rows and alpha is a list of length x.
    A_minus_alpha = A - alpha[:, np.newaxis]
    # Singular Value Decomposition.
    U, D, Vt = np.linalg.svd(A_minus_alpha, full_matrices=False)
    # Transpose Vt to get V
    V = np.transpose(Vt)
    # Calculate c such that the betas sum up to one
    c = 1 / np.sum(D[0] * U[:, 0])
    # Calculate kappa
    kappa = (1 / c) * V[:, 0]
    # Calculate beta
    beta = c * D[0] * U[:, 0]

    print(f"Sum Kappa: {np.sum(kappa)}")
    print(f"Sum Beta: {np.sum(beta)}")

    return [A, alpha, beta, kappa]


def sigmasquaredepsilon(A, alpha, beta, kappa):
    '''
    estimate sigmasquaredepsilon
    '''

    years = len(kappa)
    ages = len(alpha)

    sum = 0
    for m in range(ages):
        for n in range(years):
            sum += (A[m, n] - alpha[m] - beta[m] * kappa[n]) ** 2

    sigmasquaredepsilon = sum / (ages * years)

    return sigmasquaredepsilon


def calculate_model(A, alpha, beta, kappa):
    '''
    calculate the log_m_model and
    evaluate goodness of fit of the model to the historic data.
    output: [log_m_model,goodness of fit]
    '''
    years = len(kappa)
    ages = len(alpha)
    # First calculate the model μ. To do that i broadcast the vectors to 41x27 matrices first.
    alpha = np.tile(alpha, (years, 1)).T
    beta = np.tile(beta, (years, 1)).T
    kappa = np.tile(kappa, (ages, 1))

    # Now calculate log(μ)
    log_m_model = alpha + beta * kappa

    # Now calculate the Percentage of Variance explained by the model
    sum_model = 0
    sum_data = 0
    for m in range(len(alpha)):
        for n in range(len(kappa)):
            sum_model += (log_m_model[m, n] - alpha[m, n]) ** 2
            sum_data += (A[m, n] - alpha[m, n]) ** 2

    goodness_of_fit = sum_model / sum_data

    return [log_m_model, goodness_of_fit]


'''
(e)
'''


def project_mortality(log_m_model, beta, kappa, timespan, confidence_level):
    '''
    input:
    output: a list of prediction intervals for each year of the timespan
    '''

    '''
    first compute some important values
    '''
    ages = len(beta)
    years = len(kappa)

    # estimator C
    C = (kappa[-1] - kappa[0]) / (years - 1)

    # estimator sigmasquaredkappa
    sum = 0
    for n in range(1, years):
        sum += ((kappa[n] - kappa[n - 1]) - C) ** 2
    sigmasquaredkappa = sum / (years - 1)

    '''
    now compute the prediction intervals
    '''
    prediction_intervals = []

    # Quantile of standard normal distribution
    z = stats.norm.ppf(confidence_level + (1 - confidence_level) / 2)

    for t in range(1, timespan):

        prediction_intervals.append([])

        for a in range(ages):
            beta_now = beta[a]

            deterministic_term = log_m_model[a, (years - 1)] + t * beta_now * C

            probability_term = z * beta_now * (sigmasquaredkappa ** 0.5) * t ** 0.5

            prediction_interval = [math.exp(deterministic_term - probability_term),
                                   math.exp(deterministic_term + probability_term)]

            # Transform force of mortality to survival probabilities
            p_prediction_interval = [math.exp(-prediction_interval[1]), math.exp(-prediction_interval[0])]

            prediction_intervals[t - 1].append(p_prediction_interval)

    return prediction_intervals
