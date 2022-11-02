import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

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

def func_log(x, a, b):
    return a * np.log(x) + b

#N_list = [10 * 2**i for i in range(1,14)]
N_list = [10 * 2**i for i in range(5)]

cover_per = []

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

plt.plot(N_list, cover_per, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12, label='real_data')

N_list = np.array(N_list)
cover_per = np.array(cover_per)
popt, pcov = curve_fit(func_log, N_list, cover_per)

x = np.array(range(5, 180))
title = "approximation of func y = " + str(round(popt[0], 2)) + ' * log(x) + ' + str(round(popt[1], 2))
plt.title(title)
plt.plot(x, func_log(x, *popt), 'r-', label='fit_func')

#save image
plt.savefig('cover per as function of N.png')

# function to show the plot
plt.show()