import csv
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

N_list = [10 * 2**i for i in range(1,7)]
N_list.append(800)
N_list.append(960)
N_list.append(1000)
cover_per = []
num_zeros = []
log_num_zeros = []

plt.xlabel('N')
plt.ylabel('cover precent')
for N in N_list:
    single_cover = 0
    if N == 10:
        first = 1
    else:
        first = 6
    last = 11
    for num in range(first, last):
        csv_file_name = '/cs/labs/nati/tamarals/toroidal_updates/check_random_greedy/N_' + str(N) + '_' + str(num) + '.csv'

        with open(csv_file_name, newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in lines:
                val = row[0].split(',')[1]
                single_cover += float(val)

    cover_per.append(single_cover / (last - first))
	log_num_zeros.append(math.log(round(N**2 * (1 - cover_per / 100.))))
	num_zeros.append(round(N ** 2 * (1 - cover_per / 100.)))

#axs[0].plot(N_list, log_num_zeros, color='green', linestyle='dashed', linewidth = 3,
#         marker='o', markerfacecolor='blue', markersize=12, label='real_data')

N_list = np.array(N_list)
cover_per = np.array(cover_per)
num_zeros = np.array(num_zeros)

log_num_zeros = np.array(log_num_zeros)
popt, pcov = curve_fit(func_log, N_list, cover_per)

x = np.array(range(5, 180))
title = "log_num_of_zeros(n) =  " + str(round(popt[0], 2)) + ' * log(n) + ' + str(round(popt[1], 2))
plt.title(title)
title = "num_of_empty(n) =  (e ^ " + str(round(popt[1], 2)) + ') * (n ^ ' + str(round(popt[0], 2)) + ')'
plt.plot(N_list, num_zeros, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12, label='real_data')
plt.plot(x, func_log_to_exp(x, *popt), 'r-', label=title)
plt.legend()
plt.title('approximation to number of empty cells after random greedy algorithm')
plt.xlabel('N')
plt.ylabel('num of zeros')

#save image
plt.savefig('num of zeros logaritmic scale.png')

# function to show the plot
plt.show()

