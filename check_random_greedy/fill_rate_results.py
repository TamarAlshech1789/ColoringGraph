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
N_list = [10 * 2**i for i in range(1,7)]
N_list.append(800)
N_list.append(960)
N_list.append(1000)
cover_per = []

plt.xlabel('N')
plt.ylabel('cover precent')
for N in N_list:
    txt_file_name = str(N) + '.txt'
    with open(txt_file_name) as txt_file:
        cover_per.append(float(txt_file.readline().rstrip('\n')))

plt.plot(N_list, cover_per, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12, label='real_data')

N_list = np.array(N_list)
cover_per = np.array(cover_per)
popt, pcov = curve_fit(func_log, N_list, cover_per)

x = np.array(range(20, 1000))
title = "approximation of func y = " + str(round(popt[0], 2)) + ' * log(x) + ' + str(round(popt[1], 2))
plt.title(title)
plt.plot(x, func_log(x, *popt), 'r-', label='fit_func')

#save image
plt.savefig('cover per as function of N.png')

# function to show the plot
plt.show()