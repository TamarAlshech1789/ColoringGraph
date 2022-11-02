import numpy as np
import csv
import random
import copy
import timeit
import os, os.path
from cell import Cell

class Board:
    def __init__(self, N, is_cluster=True, _lambda = 0, count = 0 ):
        self.N = N
        self.random_greedy = True
        self.count = count
        self.marked_cells = 0
        self.max_marked_cells = 0
        self.max_cover_per = 0
        self.board = [[Cell(N, (j,i)) for i in range(N)] for j in range(N)]
        self.RG_empty_cells = list(np.ndindex(np.array(self.board).shape))
        self.all_cells = copy.deepcopy(self.RG_empty_cells)
        self.used_indices = []
        self.good_cels = copy.deepcopy(self.RG_empty_cells)
        self.start_time = timeit.default_timer()
        self._lambda = _lambda

        if is_cluster:
            output_dir = '/cs/labs/nati/tamarals/build_PLS/Original/epsilon_' + str(_lambda) + '/'
        else:
            output_dir = 'Outputs/'
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        if self.count > 0:
            self.output_dir = output_dir + str(self.count) + '/'
        else:
            self.output_dir = output_dir

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)


        self.csv_file_name = self.output_dir
        self.prog_csv_file_name = self.output_dir
        self.prog_RG_csv_file_name = self.output_dir
        self.prog_RG_board = self.output_dir
        self.txt_file_name = self.output_dir
        self.set_file_names()

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

    def remove_optional_symbol(self, symbol, curr_cell, other_cell):
        self[curr_cell].remove_optional_symbol(symbol, other_cell)
        if curr_cell in self.good_cels and len(self[curr_cell].optional_symbols) < 1:
            self.good_cels.remove(curr_cell)

    def choose_random_empty_cell(self):
        cell = random.choice(self.RG_empty_cells)
        while (self[cell].symbol != 0):
            cell = random.choice(self.RG_empty_cells)

        return cell

    def choose_random_cell(self):
        cell = random.choice(self.all_cells)
        return cell

    def choose_good_random_cell(self):
        if len(self.good_cels) == 0:
            return (-1,-1)

        cell = random.choice(self.good_cels)
        #while (self[cell].symbol != 0):
        #    cell = random.choice(self.empty_cells)

        return cell

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
        if symbol in self[cell].optional_symbols:
            self[cell].optional_symbols.remove(symbol)

        if cell in self.good_cels and len(self[cell].optional_symbols) == 0:
            self.good_cels.remove(cell)

    def __getitem__(self, cell):
        (row, col) = cell
        return self.board[row][col]

    def fix_board_add_symbol(self, cell, symbol):
        (row, col) = cell
        N = self.N

        if not cell in self.used_indices:
            self.used_indices.append(cell)

        for i in range(1,N):
            #column
            self[((row + i) % N, (col) % N)].remove_optional_symbol(symbol, cell)
            #row
            self[((row) % N, (col + i) % N)].remove_optional_symbol(symbol, cell)
            #diagonals
            self[((row + i) % N, (col + i) % N)].remove_optional_symbol(symbol, cell)
            self[((row + i) % N, (col - i) % N)].remove_optional_symbol(symbol, cell)

        self.set_cell(cell, symbol)
        self.marked_cells += 1

        if self.random_greedy == False:
            self.save_prog(self.prog_csv_file_name)
        else:
            self.save_prog(self.prog_RG_csv_file_name)


        if self.random_greedy==False and self.max_marked_cells < self.marked_cells:
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
        self[curr_cell].remove_cell_from_bad(symbol, other_cell)
        if not curr_cell in self.good_cels and len(self[curr_cell].optional_symbols) >= 1:
            self.good_cels.append(curr_cell)

    def fix_board_remove_symbol(self, cell):
        (row, col) = cell
        N = self.N
        symbol = self[cell].symbol

        if  cell in self.used_indices:
            self.used_indices.remove(cell)

        for i in range(1, N):
            # column
            self.remove_symbol(symbol, ((row + i) % N, (col) % N), cell)
            # row
            self.remove_symbol(symbol, ((row) % N, (col + i) % N), cell)
            # diagonals
            self.remove_symbol(symbol, ((row + i) % N, (col + i) % N), cell)
            self.remove_symbol(symbol, ((row + i) % N, (col - i) % N), cell)

        self.set_cell(cell, 0)
        self.marked_cells -= 1

        self.save_prog(self.prog_csv_file_name)

    def update_optional_symbol(self, prev_symbol, new_symbol, curr_cell, other_cell):

        self[curr_cell].remove_cell_from_bad(prev_symbol, other_cell)
        self[curr_cell].remove_optional_symbol(new_symbol, other_cell)
        if curr_cell in self.good_cels and len(self[curr_cell].optional_symbols) < 1:
            self.good_cels.remove(curr_cell)


    def fix_board_change_symbol(self, cell, symbol):
        (row, col) = cell
        N = self.N
        prev_symbol = self[cell].symbol

        for i in range(1, N):
            # column
            self.update_optional_symbol(prev_symbol, symbol, ((row + i) % N, (col) % N), cell)
            # row
            self.update_optional_symbol(prev_symbol, symbol, ((row) % N, (col + i) % N), cell)

            # diagonals
            self.update_optional_symbol(prev_symbol, symbol, ((row + i) % N, (col + i) % N), cell)
            self.update_optional_symbol(prev_symbol, symbol, ((row + i) % N, (col - i) % N), cell)

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

    def check_good_cells(self):
        for cell in self.good_cels:
            if len(self[cell].optional_symbols) ==0:
                print('error with cell ', cell)

    def save_prog(self, file_name):
        cover_per = float(100 * self.marked_cells) / self.N ** 2
        with open(file_name, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([timeit.default_timer() - self.start_time, cover_per])

    def change_random_greedy_stage(self):
        self.random_greedy = False