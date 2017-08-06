import sys
import subprocess
import time

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from Solver import Board

qtCreatorFile = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.solve_button.clicked.connect(self.solve)
        self.reset_button.clicked.connect(self.reset)
        self.boxes = self.get_boxes()
        QtWidgets.QWidget.setFixedSize(self, 380, 412)

    def get_boxes(self):
        boxes = []
        for counter in range(1, 82):
            boxes.append(getattr(self, 'box_{}'.format(counter)))
        return boxes

    def create_input(self):
        board = [[0 for x in range(9)] for y in range(9)]
        values = iter(self.boxes)
        for x in range(9):
            for y in range(9):
                value = next(values).text()
                if value:
                    board[x][y] = int(value)
        return board

    def create_output(self, board):
        for x in range(9):
            for y in range(9):
                self.boxes[(x*9)+y].setText(str(board[x][y]))

    def solve(self):
        """
        Using command to run Solver with PyPy to speed up the algorithm.
        If you want to use pure Python just do:
        solution = Board(self.create_input()).solve()
        """
        self.boxes = self.get_boxes()
        start_time = time.clock()
        result = subprocess.run(
            ['pypy', 'Solver.py', str(self.create_input())],
            stdout=subprocess.PIPE
        )
        elapsed = time.clock() - start_time
        solution = result.stdout.decode('utf-8')
        if not solution.startswith('['):
            msg = QtWidgets.QMessageBox.warning(self, 'Warning', solution)
        else:
            self.create_output(eval(solution))
            self.time_display.setText('Time: {0:.5f} seconds'.format(elapsed))

    def reset(self):
        for obj in self.boxes:
            obj.setText('')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
