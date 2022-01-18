import matplotlib.pyplot as plt
import sys
import csv

N = int(sys.argv[1])
max = 0

general_csv_file_name = 'N_' + str(N) + '/N_' + str(N) + '_lambda_'
lambdas = []
"""
lambdas.append(1.1)
for i in range(1, 21):
    lambdas.append(i * 5)
for i in range(2, 11):
    lambdas.append(i * 100)
    
for i in range(3, 21):
    lambdas.append(i * 500)
    """
lambdas.append(2000)
lambdas.append(2500)
lambdas.append(3000)
lambdas.append(3500)
lambdas.append(4000)
for i in range(3, 21):
    lambdas.append(i * 5000)

max_val = 0
max_lambda = 0
max_time = 0
min_val = {}
for l in lambdas:
    first = True
    x, y = [], []
    min_val[l] = 0

    if l == 1.1:
        csv_file_name = general_csv_file_name + str(1.1) + '.csv'
    else:
        csv_file_name = general_csv_file_name + str(l) + '.0.csv'

    with open(csv_file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            if first == True:
                first = False
            else:
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
                #y.append("{:.1f}".format(float(r[1])))
                y.append(float(r[1]))

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

#save image
plt.savefig('N_' + str(N) + '.png')

# function to show the plot
plt.show()

