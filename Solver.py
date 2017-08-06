from __future__ import print_function
import re
import sys


class Board(object):
    def __init__(self, board):
        self.board = board
        self.constant_positions = []

    def solve(self):
        """
        Backtracking algorithm - brute-force in simple words.
        Based on description from:
        https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
        """
        if isinstance(self.find_constants(), str):
            return 'Invalid input, please check given numbers.'
        x, y, last_num = 0, 0, 1
        search = True
        omit = False
        while x < 9:
            while y < 9:
                if (x, y) in self.constant_positions:
                    y += 1
                    continue
                for num in range(last_num, 10):
                    if (num not in self.board[x] and
                            num not in [_[y] for _ in self.board] and
                            num not in self.section_values(x, y)):
                        self.board[x][y] = num
                        last_num = 1
                        break
                else:
                    omit = True
                    self.board[x][y] = 0
                    while search:
                        if y == 0:
                            if x <= 0:
                                return 'Solution could not be found.'
                            x -= 1
                            y = 8
                        else:
                            y -= 1
                        if (x, y) not in self.constant_positions:
                            if self.board[x][y] >= 9:
                                self.board[x][y] = 0
                            else:
                                search = False
                                last_num = self.board[x][y] + 1
                    search = True
                if omit:
                    omit = False
                else:
                    y += 1
            y = 0
            x += 1
        return self.board

    def section_values(self, x, y):
        """
        Given a coordinates to value return all values in that section.
        """
        x //= 3
        y //= 3
        x_values = (x * 3, x * 3 + 1, x * 3 + 2)
        y_values = (y * 3, y * 3 + 1, y * 3 + 2)
        result = []
        for x in x_values:
            for y in y_values:
                result.append(self.board[x][y])
        return result

    def find_constants(self):
        for x in range(9):
            for y in range(9):
                if self.board[x][y] is not 0:
                    tmp = self.board[x][y]
                    self.board[x][y] = 0
                    if (tmp in self.board[x] or
                            tmp in [_[y] for _ in self.board] or
                            tmp in self.section_values(x, y)):
                        return 'InvalidConstants'
                    self.board[x][y] = tmp
                    self.constant_positions.append((x, y))

if __name__ == '__main__':
    print(Board(eval(sys.argv[1])).solve())
