import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

N_list = [10 * 2**i for i in range(1,7)]
N_list.append(800)
N_list.append(960)
N_list.append(1000)
cover_per = []

for N in N_list:
    txt_file_name = str(N) + '.txt'
    with open(txt_file_name) as txt_file:
        cover_per.append(float(txt_file.readline().rstrip('\n')))

# Define Error
x_error, y_error = [], []
for i in range(len(N_list)):
    x_error.append(2)
    y_error.append(2)

# Plot Bar chart
plt.bar(N_list,cover_per)

# Plot error bar

plt.errorbar(x=N_list, y=cover_per, xerr = x_error, yerr = y_error,
             fmt='o', ecolor = 'red',color='yellow')

# Display graph


plt.show()