# GUI.py
import pygame
import time
pygame.font.init()


class Grid:
    board = [# This is the Sudoku Puzzle shown in a array.
        [5, 4, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0],
        [4, 0, 0, 6, 0, 0],
        [0, 0, 1, 0, 0, 4],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 3, 2],
    ]
#setting values
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
#setting permenant value
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False



