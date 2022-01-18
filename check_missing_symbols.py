import csv
import sys

N = sys.argv[1]
e = sys.argv[2]
column_missing = [[] for n in range(int(N))]

def find_missing_symbols(line, num_line):
    symbols = [s for s in range(1, int(N) + 1 )]
    for i, symbol in enumerate(line):
        """if symbol == '--':
            column_missing[i].append(int(symbol))"""
        if not symbol == '--':
            symbols.remove(int(symbol))

    return symbols

def print_symbols(symbols):
    if len(symbols) == 0:
        return '-'

    str_print = str(symbols[0])
    symbols.remove(symbols[0])
    for s in symbols:
        str_print = str_print + ', ' + str(s)
    return str_print


file_name = general_csv_file_name = 'records/N_' + str(N) + '_10e' + e + '.txt'
#file_name = general_csv_file_name = 'records/N_' + str(N) + '_10e' + e + ' - Copy.txt'

file1 = open(file_name, 'r')
Lines = file1.readlines()
num_line = 1

num_missing_symbols = 0
# Strips the newline character
for line in Lines:
    missing_symbols = find_missing_symbols(line.strip().split(' '), num_line)
    num_missing_symbols += len(missing_symbols)
    print('missing symbols in line ', num_line, ': ', print_symbols(missing_symbols))
    num_line += 1

print('===============================================================')
print('number of missing queens - ', num_missing_symbols)

"""num_column = 1
for column in column_missing:
    print('missing symbols in column ', num_column, ': ', print_symbols(column))
    num_column += 1"""