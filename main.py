from functools import wraps
import re
import time


SCHEME = """
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)

    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)

    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
    (0, 0, 0)   (0, 0, 0)   (0, 0, 0)
"""
SCHEME_ERROR_MESSAGE = 'You distorted the pattern and it is no longer valid.'
SOLUTION_ERROR_MESSAGE = 'There is no solution to this Sudoku.'


def timer(func):
    """
    Calculates time that given function take to execute.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        result = func(*args, **kwargs)
        elapsed = time.clock() - start
        print('Function {} with arguments: {}, {} took {:.6f}s.'.format(
            func.__name__, args, kwargs, elapsed
        ))
        return result
    return wrapper


class SchemeError(Exception):
    """
    Exception raised when scheme of input file isn't the same as given pattern.
    """


class SolutionNotFoundError(Exception):
    """
    Exception raised when there's no solution to given Sudoku.
    """


class Board(object):
    def __init__(self, board):
        self.board = board
        self.constant_positions = []
        self.find_constants()

    @timer
    def solve(self):
        """
        Backtracking algorithm - brute-force in simple words.
        Based on description from:
        https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
        """
        x, y, last_tmp = 0, 0, 1
        search = True
        omit = False
        while x < 9:
            while y < 9:
                if (x, y) in self.constant_positions:
                    y += 1
                    continue
                else:
                    for tmp in range(last_tmp, 10):
                        if (tmp not in self.board[x]
                                and tmp not in [_[y] for _ in self.board]
                                and tmp not in self.section_values(x, y)):
                            self.board[x][y] = tmp
                            last_tmp = 1
                            break
                    else:
                        omit = True
                        if self.board[x][y] is not 0:
                            self.board[x][y] = 0
                        while search:
                            if y == 0:
                                if x == 0:
                                    give_output(self.board)
                                    return
                                x -= 1
                                y = 8
                            else:
                                y -= 1
                            if (x, y) not in self.constant_positions:
                                search = False
                                last_tmp = self.board[x][y] + 1
                        search = True
                if omit:
                    omit = False
                    continue
                y += 1
            y = 0
            x += 1

    def section_values(self, x, y):
        """
        Given a coordinates to value return all values in that section.
        """
        # TODO optimize by adding sector variable
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
                    self.constant_positions.append((x, y))


def take_input():
    with open('input', 'r') as f:
        origin = f.read()
    if re.sub(r'\d', r'0', origin) == SCHEME:
        values = map(int, re.findall(r'\d', origin))
        return [list(a) for a in zip(*([iter(values)]*9))]
    else:
        with open('input', 'w') as f:
            f.write(SCHEME)
        raise SchemeError(SCHEME_ERROR_MESSAGE)


def give_output(board):
    output = list(map(str, board))
    with open('output', 'w') as f:
        for x in output:
            f.write(x + '\n\n')


if __name__ == '__main__':
    board = Board(board=take_input())
    board.solve()
    give_output(board.board)
