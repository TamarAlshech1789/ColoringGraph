import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import math

def func_e(x,a,b,c):
    return a * np.exp(-b*x) + c

def func_linear(x, a, b):
    return a * x + b

def func_quadratic(x, a, b, c):
    return a * np.power(x, 2) + b * x + c

def func_power_3(x, a, b, c, d):
    return a * np.power(x, 3) + b * np.power(x, 2) + c * x + d

def func_sqrt(x, a, b):
    return np.sqrt(a * x) + b

def func_exponent(x, a, b):
    return a * np.power(x, b)

def func_log(x, a, b):
    return a * np.log(x) + b

def func_log_to_exp(x, a, b):
    return np.power(x,a) * np.power(np.e, b)

#N_list = [10 * 2**i for i in range(1,14)]
N_list = [10 * 2**i for i in range(1,7)]
N_list.append(800)
N_list.append(960)
N_list.append(1000)
cover_per = []
num_zeros = []
log_num_zeros = []


fig, axs = plt.subplots(2, 1)
#ax.set_yscale('log')

for N in N_list:
    txt_file_name = str(N) + '.txt'
    with open(txt_file_name) as txt_file:
        single_cover_per = float(txt_file.readline().rstrip('\n'))
        cover_per.append(single_cover_per)
        log_num_zeros.append(math.log(round(N**2 * (1 - single_cover_per / 100))))
        num_zeros.append(round(N ** 2 * (1 - single_cover_per / 100)))

axs[0].plot(N_list, log_num_zeros, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12, label='real_data')

N_list = np.array(N_list)
num_zeros = np.array(num_zeros)
log_num_zeros = np.array(log_num_zeros)
popt, pcov = curve_fit(func_log, N_list, log_num_zeros)
#popt, pcov = curve_fit(func_exponent, N_list, num_zeros)

x = np.array(range(10,1000))

title = "logaritmic scale approx: log_num_of_zeros(n) =  " + str(round(popt[0], 2)) + ' * log(n) + ' + str(round(popt[1], 2))
#title = 'exponent approximation: num_of_zeros(n) =' + str(round(popt[0], 2)) + ' * (n ^ ' + str(round(popt[1], 2)) + ')'

axs[0].set_title(title)
axs[0].plot(x, func_log(x, *popt), 'r-', label='fit_func')
#plt.plot(x, func_exponent(x, *popt), 'r-', label='fit_func')


#secong image
title = "num_of_zeros(n) =  (e ^ " + str(round(popt[1], 2)) + ') * (n ^ ' + str(round(popt[0], 2)) + ')'
axs[1].set_title(title)
axs[1].plot(N_list, num_zeros, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12, label='real_data')
axs[1].plot(x, func_log_to_exp(x, *popt), 'r-', label='fit_func')


axs.flat[0].set(xlabel = '.', ylabel = 'log num of zeros')
axs.flat[1].set(xlabel = 'N', ylabel = 'num of zeros')

#save image
plt.savefig('num of zeros logaritmic scale.png')
#plt.savefig('num of zeros exponent.png')

# function to show the plot
plt.show()

