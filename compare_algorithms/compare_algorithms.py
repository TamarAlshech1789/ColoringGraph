import matplotlib.pyplot as plt
import csv

N  = 50

def read_csv(file_name):
    x = []
    y = []
    with open(file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            r = row[0].split(',')
            if float(r[0]) / 60 < 200:
                x.append(float(r[0]) / 60)
                # y.append("{:.1f}".format(float(r[1])))
                y.append(float(r[1]))

        return x,y
if N == 50:
    legends = ['Original', 'AddZero', 'couples', 'Priority', 'ChangingZero', 'Priority_numSymbols', 'Absorbers', 'Mix']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
else:
    legends = ['Original', 'couples', 'Priority', 'ChangingZero', 'Priority_numSymbols']
    colors = ['b', 'r', 'c', 'm', 'y']

for i, legend in enumerate(legends):
    file_name = legend + '_N_' + str(N) + '.csv'
    x,y = read_csv(file_name)
    plt.plot(x, y, label=legend)

plt.legend()
plt.xlabel('Time (min)')
plt.ylabel('cover precent')
title = 'compare algorithms for N = ' + str(N)
plt.title(title)
# save image
figName = 'compare_algorithms_N_' + str(N) + '.png'
plt.savefig(figName)