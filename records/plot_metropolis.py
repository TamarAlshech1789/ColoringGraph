import matplotlib.pyplot as plt
import sys
import csv

N = int(sys.argv[1])
e = int(sys.argv[2])
max = 0

general_csv_file_name = 'N_' + str(N) + '_10e'
for e_i in range(2, e + 1):
    first = True
    x, y = [], []

    csv_file_name = general_csv_file_name + str(e_i) + '.csv'
    with open(csv_file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            if first == True:
                first = False
            else:
                r = row[0].split(',')

                if e_i == e - 1:
                    max = float(r[1])

                if  e_i == e and  float(r[1]) > max :
                    break
                x.append(float(r[0]) / 60)
                #y.append("{:.1f}".format(float(r[1])))
                y.append(float(r[1]))

    legend = 'lambda_10e' + str(e_i)
    plt.plot(x, y, label=legend)


# Function add a legend
plt.legend()
plt.xlabel('Time (min)')
plt.ylabel('cover precent')

#save image
plt.savefig('N_' + str(N) + '.png')

# function to show the plot
plt.show()
