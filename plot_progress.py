import matplotlib.pyplot as plt
import csv
import os.path


N = 100
max = 0

plot_metropolis = True
algorithms_list = [
    'Original_Metropolis_Markov_Chain',
    'list_CellAndSymbol_SwitchZero_Absorbers',
    'list_CellAndSymbol_SwitchZero',
    'list_CellAndSymbol_AddZero',
    'list_CellAndSymbol_Absorbers',
    'list_available_CellAndSymbol'
]
algorithm = algorithms_list[5]
if plot_metropolis == True:
    general_csv_file_name = algorithm + '/prog_N_' + str(N) + '_lambda_'
else:
    general_csv_file_name = 'Outputs/randomGreedy_N_' + str(N) + '_lambda_'

lambdas = [1.1]
for i in range(0,5):
    lambdas.append(5 * (10 ** i))
    lambdas.append(10 * (10 ** i))

max_val = 0
max_lambda = 0
max_time = 0
min_val = {}
for l in lambdas:
    x, y = [], []
    min_val[l] = 0
    print('lambda is -', l)
    if l == 1.1:
        csv_file_name = general_csv_file_name + str(1.1) + '.csv'
    else:
        csv_file_name = general_csv_file_name + str(l) + '.0.csv'
    if os.path.isfile(csv_file_name) == True:
        with open(csv_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in csvreader:
                if len(row) > 0:
                    r = row[0].split(',')

                    if float(r[1]) > max_val:
                        max_val = float(r[1])
                        max_lambda = l
                        max_time = float(r[0])

                    if float(r[1]) > min_val[l]:
                        min_val[l] = float(r[1])

                    x.append(float(r[0]) / 60)
                    # y.append("{:.1f}".format(float(r[1])))
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

# save image
imageName = algorithm + '_' + str(N) + '.png'
if plot_metropolis == True:
    plt.savefig(imageName)
else:
    plt.savefig('randomGreedy_' + str(N) + '.png')
