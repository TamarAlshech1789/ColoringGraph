import random


class Cell:
    def __init__(self, N, cell, symbol = 0):
        self.cell = cell
        self.symbol = symbol
        self.optional_symbols = list([(s + 1) for s in range(N)])
        self.bad_symbols = {}
        self.num_optional = len(self.optional_symbols)

    def remove_optional_symbol(self, symbol, other_cell):
        if self.cell == other_cell:
            return

        if symbol in self.optional_symbols:
            self.optional_symbols.remove(symbol)
        if symbol in self.bad_symbols:
            if not other_cell in self.bad_symbols[symbol]:
                self.bad_symbols[symbol].append(other_cell)
        else:
            self.bad_symbols[symbol] = []
            self.bad_symbols[symbol].append(other_cell)

    def remove_cell_from_bad(self, symbol, other_cell):
        if self.cell == other_cell:
            return

        if symbol in self.bad_symbols and other_cell in self.bad_symbols[symbol]:
            self.bad_symbols[symbol].remove(other_cell)
            if len(self.bad_symbols[symbol]) == 0:
                del self.bad_symbols[symbol]
        if not symbol in self.bad_symbols and not symbol in self.optional_symbols :
            self.optional_symbols.append(symbol)

    def check_cell(self):
        for symbol in self.bad_symbols:
            if not symbol == self.symbol and len(self.bad_symbols[symbol]) == 0:
                print('problem')

    def choose_random_symbol(self):
        if len(self.optional_symbols) == 0:
            return 0
        return random.choice(self.optional_symbols)

    def symbols_with_one_threat(self):
        symbol_list = []
        for symbol in self.bad_symbols:
            if  len(self.bad_symbols[symbol]) == 1:
                symbol_list.append(symbol)

        return symbol_list