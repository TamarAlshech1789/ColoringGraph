import random


class Cell:
    def __init__(self, N, cell, symbol = 0):
        self.cell = cell
        self.symbol = symbol
        self.optional_symbols = list([(s + 1) for s in range(N)])
        self.bad_symbols = {}
        self.num_optional = len(self.optional_symbols)
        self.toroidal_optional_symbols = list([(s + 1) for s in range(N)])

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

    def remove_toroidal_optional_symbol(self, symbol, other_cell):
        if self.cell == other_cell:
            return

        if symbol in self.toroidal_optional_symbols:
            self.toroidal_optional_symbols.remove(symbol)

    def remove_cell_from_bad(self, symbol, other_cell):
        if self.cell == other_cell:
            return

        if symbol in self.bad_symbols and other_cell in self.bad_symbols[symbol]:
            self.bad_symbols[symbol].remove(other_cell)
            if len(self.bad_symbols[symbol]) == 0:
                del self.bad_symbols[symbol]
        if not symbol in self.bad_symbols and not symbol in self.optional_symbols :
            self.optional_symbols.append(symbol)

    def choose_random_symbol(self):
        if len(self.optional_symbols) == 0:
            return 0
        return random.choice(self.optional_symbols)

    def choose_random_toroidal_symbol(self):
        if len(self.toroidal_optional_symbols) == 0:
            return 0
        return random.choice(self.toroidal_optional_symbols)

