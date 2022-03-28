import matplotlib.pyplot as plt
import csv
from enum import Enum
class Scenario(Enum):
    N_50 = 1
    optiomal_priority= 2
    priority_160 = 3
    compare_priority = 4

scenario = Scenario.compare_priority

N = 100
max = 0

general_csv_file_name = 'Outputs_numSymbols/N_' + str(N) + '_lambda_'
lambdas = []
lambdas.append(1.1)
for i in range(1,15):
    lambdas.append(2 ** i)

max_val = 0
list_max_vals = []
max_lambda = 0
max_time = 0
min_val = {}
for l in lambdas:
    x, y = [], []
    min_val[l] = 0

    if l == 1.1:
        csv_file_name = general_csv_file_name + str(1.1) + '.csv'
    else:
        csv_file_name = general_csv_file_name + str(l) + '.0.csv'

    with open(csv_file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            r = row[0].split(',')

            """if e_i == e - 1:
                max = float(r[1])

            if  e_i == e and  float(r[1]) > max :
                break"""

            if float(r[1]) > max_val:
                max_val = float(r[1])
                max_lambda = l
                max_time = float(r[0])

            if float(r[1]) > min_val[l]:
                min_val[l] = float(r[1])

            x.append(float(r[0]) / 60)
            # y.append("{:.1f}".format(float(r[1])))
            y.append(float(r[1]))


    list_max_vals.append(float(r[1]))
    legend = 'lambda_' + str(l)
    plt.plot(x, y, label=legend)

print('max per. ', max_val, ' for lambda ', max_lambda, ' at time ', max_time)
min_lambda = 0
min_val_lambda = 100
for l in lambdas:
    if min_val[l] < min_val_lambda:
        min_val_lambda = min_val[l]
        min_lambda = l
print('worst lambda ', min_lambda, ' with pre. ', min_val_lambda)

# Function add a legend
plt.legend()
plt.xlabel('Time (min)')
plt.ylabel('cover precent')

# save image
plt.savefig('priority_metropolis_numSymbols_' + str(N) + '.png')
print(list_max_vals)