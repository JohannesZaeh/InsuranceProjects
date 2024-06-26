import scipy.io
import matplotlib.pyplot as plt
import math
import numpy as np

#SET WORKING DIRECTORY, the directory which contains the .mat file
working_dir = "INSERT WORKING DIRECTORY"


# Load the qxt from a .mat file
mat_file = scipy.io.loadmat(f'{working_dir}/Export 2.mat')
#Extract data from .loadmat dictionary
qxt = mat_file["export2"]
#Trim data to only contain years 1980-2006
qxt=qxt[130:]

#Trim data to only contain ages 50 to 90
qxt=[ages[50:91] for ages in qxt]


'''
(a)
'''



#To be consistent with the lecture, i transpose the data so the rows are ages and the columns are years.
qxt = np.transpose(qxt)

#Create Numpy Matrix to make it more convenient to work with.
qxt = np.array(qxt)

#Create the matrix pxt; pxt = 1-qxt
pxt = 1-qxt

#Calculate μx(t). Because we transposed the qxt, this is actually a 41x27 matrix.
m = -1*np.log(pxt)

#A = log(m)
A = np.log(m)

#ax = mean(Ax)
ax = np.mean(A, axis = 1)

#Calculate the matrix A-ax, it's not so straightforward because it is along the rows
A_minus_ax = A - ax[:, np.newaxis]

#Singular Value Decomposition.
U,D,Vt = np.linalg.svd(A_minus_ax, full_matrices=False)

#Transpose Vt to get V
V = np.transpose(Vt)
#Calculate c such that the betas sum up to one
c = 1/np.sum(D[0]*U[:,0])

#Calculate kappa
kappa = (1/c)*V[:,0]

#Calculate beta
beta = c*D[0]*U[:,0]

print("Test if the vecors sum up correctly:")
print(f"Sum Kappa: {np.sum(kappa)}")
print(f"Sum Beta: {np.sum(beta)}")

#Plot the vectors
ages = np.linspace(50,90,41)
years = np.linspace(1980,2006,27)

plt.plot(ages,ax)
plt.title("Alpha")
plt.xlabel('Age')
plt.ylabel('Alpha')
plt.show()

plt.plot(years,kappa)
plt.title("Kappa")
plt.xlabel('Year')
plt.ylabel('Kappa')
plt.show()

plt.plot(ages,beta)
plt.title("Beta")
plt.xlabel('Age')
plt.ylabel('Beta')
plt.show()

'''
(c)
'''
#estimate sigmasquaredepsilon
sum = 0
for m in range(41):
    for n in range(27):
        sum += (A[m,n]-ax[m]-beta[m]*kappa[n])**2
sigmasquaredepsilon = sum/(41*27)


print(f"Sigmasquaredepsilon: {sigmasquaredepsilon}")

'''
(d)
'''
#First calculate the model μ. To do that i broadcast the vectors to 41x27 matrices first.
ax = np.tile(ax, (27, 1)).T
beta = np.tile(beta, (27, 1)).T
kappa = np.tile(kappa, (41, 1))

#Now calculate log(μ)
log_m_model = ax+beta*kappa

#Now calculate the Percentage of Variance explained by the model
sum_model = 0
sum_data = 0
for m in range(41):
    for n in range(27):
        sum_model += (log_m_model[m,n]-ax[m,n])**2
        sum_data += (A[m,n]-ax[m,n])**2

goodness_of_fit = sum_model/sum_data

print(f"Goodness of fit: {goodness_of_fit}")

'''
(e)
'''
#estimator C
C = (kappa[0,26]-kappa[0,0])/26
print(f"Estimator C: {C}")

#estimator sigmasquaredkappa
sum = 0
for n in range(1,27):
    sum += ((kappa[0,n]-kappa[0,n-1])-C)**2
sigmasquaredkappa = sum/26
print(f"Estimator sigmasquaredkappa: {sigmasquaredkappa}")

'''
(f)
'''
#For 2050, k=44. Compute with the formula:
prediction_interval = [math.exp(log_m_model[30,26]+44*beta[30,26]*C-1.96*beta[30,26]*(sigmasquaredkappa**0.5)*44**0.5),math.exp(log_m_model[30,26]+44*beta[30,26]*C+1.96*beta[30,26]*(sigmasquaredkappa**0.5)*44**0.5)]
print(f"Prediction Interval for μ for age 80 in 2050: {prediction_interval}")


#Prediction interval for survival probabilities
p_prediction_interval = [math.exp(-prediction_interval[1]),math.exp(-prediction_interval[0])]
print(f"Prediction Interval for p for age 80 in 2050: {p_prediction_interval}")


