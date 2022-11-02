import numpy as np
import csv
import random
import copy
import timeit
import os, os.path
from cell import Cell
random_greedy = True

class Board:
    def __init__(self, N, is_cluster=True, _lambda = 0 ):
        self.N = N
        self.marked_cells = 0
        self.max_marked_cells = 0
        self.max_cover_per = 0
        self.board = [[Cell(N, (j,i)) for i in range(N)] for j in range(N)]
        self.RG_empty_cells = list(np.ndindex(np.array(self.board).shape))
        self.empty_cells = copy.deepcopy(self.RG_empty_cells)
        self.all_cells = copy.deepcopy(self.RG_empty_cells)
        self.used_indices = []
        #self.good_cels = copy.deepcopy(self.RG_empty_cells)
        self.good_cells = []
        self.init_good_cells()
        self.good_cells_count = {}
        self.good_cells_count[self.N] = list(np.ndindex(np.array(self.board).shape))

        self.start_time = timeit.default_timer()
        self._lambda = _lambda

        if is_cluster:
            self.output_dir = '/cs/labs/nati/tamarals/toroidal_updates/couples_changezero/'
        else:
            self.output_dir = 'Outputs/'
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        self.csv_file_name = self.output_dir
        self.prog_csv_file_name = self.output_dir
        self.prog_RG_csv_file_name = self.output_dir
        self.txt_file_name = self.output_dir
        self.set_file_names()

    def init_good_cells(self):
        symbols = list([(s + 1) for s in range(self.N)])

        for cell in self.RG_empty_cells:
            for symbol in symbols:
                self.good_cells.append((cell, symbol))

    def set_file_names(self):
        self.csv_file_name += 'N_' + str(self.N) + '_lambda_' +str(self._lambda) + '.csv'
        if os.path.isfile(self.csv_file_name):
            os.remove(self.csv_file_name)

        self.txt_file_name += 'metropolis_board_N_' + str(self.N) + '_lambda_' + str(self._lambda) + '.txt'
        if os.path.isfile(self.txt_file_name):
            os.remove(self.txt_file_name)

        self.prog_csv_file_name += 'prog_N_' + str(self.N) + '_lambda_' +str(self._lambda) + '.csv'
        if os.path.isfile(self.prog_csv_file_name):
            os.remove(self.prog_csv_file_name)

        self.prog_RG_csv_file_name += 'randomGreedy_N_' + str(self.N) + '_lambda_' + str(self._lambda) + '.csv'
        if os.path.isfile(self.prog_RG_csv_file_name):
            os.remove(self.prog_RG_csv_file_name)
			
    def update_good_cell_count(self, cell, prev_num_options, new_num_options):
        if prev_num_options == new_num_options:
            return
        if prev_num_options > 0:
            self.good_cells_count[prev_num_options].remove(cell)
            if len(self.good_cells_count[prev_num_options]) == 0:
                del self.good_cells_count[prev_num_options]

        if new_num_options > 0:
            if not new_num_options in self.good_cells_count:
                self.good_cells_count[new_num_options] = []
            self.good_cells_count[new_num_options].append(cell)


    def remove_optional_symbol(self, symbol, curr_cell, other_cell):
        prev_num_options = len(self[curr_cell].optional_symbols)
        self[curr_cell].remove_optional_symbol(symbol, other_cell)
        if (curr_cell, symbol) in self.good_cells:
            self.good_cells.remove((curr_cell, symbol))

        num_options = len(self[curr_cell].optional_symbols)
        self.update_good_cell_count(curr_cell, prev_num_options, num_options)

    def choose_random_empty_cell(self):
        cell = random.choice(self.RG_empty_cells)
        while (self[cell].symbol != 0):
            cell = random.choice(self.RG_empty_cells)

        return cell

    def choose_random_used_cell(self):
        cell = random.choice(self.used_indices)

        return cell

    def choose_random_cell(self):
        cell = random.choice(self.all_cells)
        return cell

    def choose_good_random_cell_and_symbol(self):
        if len(self.good_cells) == 0:
            return ((-1,-1), 0)

        (cell, symbol) = random.choice(self.good_cells)
        return (cell, symbol)

    def switch_empty_cell(self):
        cell = random.choice(self.empty_cells)
        symbols_list = self[cell].symbols_with_one_threat()
        if len(symbols_list) == 0:
            return False

        symbol = random.choice(symbols_list)
        switch_cell = self[cell].bad_symbols[symbol][0]

        self.fix_board_remove_symbol(switch_cell)
        self.fix_board_add_symbol(cell, symbol, random_greedy=False)
        return True

    def print_solution(self, file=None):
        for i in range(self.N):
            line = ''
            for cell in self.board[i]:
                s = cell.symbol
                if s == 0:
                    line += '-- '
                else:
                    line += "{:02d}".format(int(s))
                    line += " "
            if file == None:
                print(line)
            else:
                line += '\n'
                file.write(line)

    def set_cell(self, cell, symbol):
        self[cell].symbol = symbol
        prev_num_options = len(self[cell].optional_symbols)
        if symbol in self[cell].optional_symbols:
            self[cell].optional_symbols.remove(symbol)

        if (cell, symbol) in self.good_cells:
            self.good_cells.remove((cell, symbol))
        num_options = len(self[cell].optional_symbols)
        self.update_good_cell_count(cell, prev_num_options, num_options)

    def __getitem__(self, cell):
        (row, col) = cell
        return self.board[row][col]

    def fix_board_add_symbol(self, cell, symbol):
        (row, col) = cell
        N = self.N

        if cell in self.empty_cells:
            self.empty_cells.remove(cell)
        if not cell in self.used_indices:
            self.used_indices.append(cell)


        for r in range(N):
            self.remove_optional_symbol(symbol, (r,col), cell)
        for c in range(N):
            self.remove_optional_symbol(symbol, (row,c), cell)

        # Check left diagonal on upeer side
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            self.remove_optional_symbol(symbol, (i,j), cell)

        # Check left diagonal on lower side
        for i, j in zip(range(row, N, 1),
                        range(col, -1, -1)):
            self.remove_optional_symbol(symbol, (i,j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, -1, -1),
                        range(col, N, 1)):
            self.remove_optional_symbol(symbol, (i,j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, N, 1),
                        range(col, N, 1)):
            self.remove_optional_symbol(symbol, (i,j), cell)

        if random_greedy:
            for i in range(1,N):
                #column
                self[((row + i) % N, (col) % N)].remove_toroidal_optional_symbol(symbol, cell)
                #row
                self[((row) % N, (col + i) % N)].remove_toroidal_optional_symbol(symbol, cell)
                #diagonals
                self[((row + i) % N, (col + i) % N)].remove_toroidal_optional_symbol(symbol, cell)
                self[((row + i) % N, (col - i) % N)].remove_toroidal_optional_symbol(symbol, cell)

        self.set_cell(cell, symbol)
        self.marked_cells += 1

        if random_greedy == False:
            self.save_prog(self.prog_csv_file_name)
        else:
            self.save_prog(self.prog_RG_csv_file_name)


        if random_greedy==False and self.max_marked_cells < self.marked_cells:
            cover_per = float(100 * self.marked_cells) / N ** 2
            if (cover_per - self.max_cover_per) >= 0.2:
                with open(self.csv_file_name, 'a') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([timeit.default_timer() - self.start_time, cover_per])

                if float(100 * self.marked_cells) / N ** 2 > 50 and int(cover_per * 100) % 10 - int( self.max_cover_per* 100) % 10 >= 1:

                        self.print_current_board(cover_per)

                self.max_cover_per = cover_per

            self.max_marked_cells = self.marked_cells

    def print_current_board(self, cover_per):
        if os.path.isfile(self.txt_file_name):
            os.remove(self.txt_file_name)

        file = open(self.txt_file_name, 'a')

        file.write('board with ' + str(int(cover_per)) + ' per cover:\n')
        self.print_solution(file)
        file.close()

    def remove_symbol(self, symbol, curr_cell, other_cell):
        prev_num_options = len(self[curr_cell].optional_symbols)
        self[curr_cell].remove_cell_from_bad(symbol, other_cell)

        if symbol in self[curr_cell].optional_symbols and not (curr_cell, symbol) in self.good_cells:
            self.good_cells.append((curr_cell, symbol))
        num_options = len(self[curr_cell].optional_symbols)
        self.update_good_cell_count(curr_cell, prev_num_options, num_options)

    def fix_board_remove_symbol(self, cell):
        (row, col) = cell
        N = self.N
        symbol = self[cell].symbol

        if not cell in self.empty_cells:
            self.empty_cells.append(cell)
        if  cell in self.used_indices:
            self.used_indices.remove(cell)

        for r in range(N):
            self.remove_symbol(symbol, (r,col), cell)
        for c in range(N):
            self.remove_symbol(symbol, (row,c), cell)

        # Check left diagonal on upeer side
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            self.remove_symbol(symbol, (i,j), cell)

        # Check left diagonal on lower side
        for i, j in zip(range(row, N, 1),
                        range(col, -1, -1)):
            self.remove_symbol(symbol, (i,j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, -1, -1),
                        range(col, N, 1)):
            self.remove_symbol(symbol, (i,j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, N, 1),
                        range(col, N, 1)):
            self.remove_symbol(symbol, (i,j), cell)

        self.set_cell(cell, 0)
        self.marked_cells -= 1

        self.save_prog(self.prog_csv_file_name)

    def update_optional_symbol(self, prev_symbol, new_symbol, curr_cell, other_cell):

        prev_num_options = len(self[curr_cell].optional_symbols)
        self[curr_cell].remove_cell_from_bad(prev_symbol, other_cell)
        self[curr_cell].remove_optional_symbol(new_symbol, other_cell)

        if prev_symbol in self[curr_cell].optional_symbols and not (curr_cell, prev_symbol) in self.good_cells:
            self.good_cells.append((curr_cell, prev_symbol))
        if (curr_cell, new_symbol) in self.good_cells:
            self.good_cells.remove((curr_cell, new_symbol))
		
        num_options = len(self[curr_cell].optional_symbols)
        self.update_good_cell_count(curr_cell, prev_num_options, num_options)


    def fix_board_change_symbol(self, cell, symbol):
        (row, col) = cell
        N = self.N
        prev_symbol = self[cell].symbol

        for r in range(N):
            self.update_optional_symbol(prev_symbol, symbol, (r,col), cell)
        for c in range(N):
            self.update_optional_symbol(prev_symbol, symbol, (row,c), cell)

        # Check left diagonal on upeer side
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            self.update_optional_symbol(prev_symbol, symbol, (i, j), cell)

        # Check left diagonal on lower side
        for i, j in zip(range(row, N, 1),
                        range(col, -1, -1)):
            self.update_optional_symbol(prev_symbol, symbol, (i, j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, -1, -1),
                        range(col, N, 1)):
            self.update_optional_symbol(prev_symbol, symbol, (i, j), cell)

        # Check right diagonal on upper side
        for i, j in zip(range(row, N, 1),
                        range(col, N, 1)):
            self.update_optional_symbol(prev_symbol, symbol, (i, j), cell)

        self.set_cell(cell, symbol)

    def get_np_board(self):
        board = np.zeros(self.N ** 2).reshape((self.N, self.N))
        for r in range(self.N):
            for c in range(self.N):
                board[r][c] = self.board[r][c].symbol

        return board

    def save_csv(self, file_name = ''):
        if file_name == '':
            csv_file_name = self.output_dir + 'board_' + str(self.N) + '.csv'
        else:
            csv_file_name = file_name

        np.savetxt(csv_file_name, self.get_np_board(), delimiter=',')

    def find_empty_cells(self):
        np_board = self.get_np_board()
        return sum([list(line).count(0) for line in np_board])

    def save_prog(self, file_name):
        cover_per = float(100 * self.marked_cells) / self.N ** 2
        with open(file_name, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([timeit.default_timer() - self.start_time, cover_per])

    def change_random_greedy_stage(self):
        self.random_greedy = False