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
            #setting temp value for the cube
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 6
        for i in range(self.rows):
            if i % 2 == 0 and i != 0:
                thick = 5
                pygame.draw.line(self.win, (0,200,0), (0, i * gap), (self.width, i*gap), thick) # for vertical line
            for j in range(self.rows):
                if i % 3 == 0 and i != 0:
                    thick = 5
                    #pygame.draw.line(self.win, (0,255,0), (0, i * gap), (self.width, i*gap), thick) # for vertical line
                    pygame.draw.line(self.win, (150, 0, 200), (i * gap, 0), (i * gap, self.height), thick) # for Horizontal line
            pygame.draw.line(self.win, (0,250,0), (0, i * gap), (self.width, i*gap), 2) # for vertical line


            pygame.draw.line(self.win, (150, 0, 200), (i * gap, 0), (i * gap, self.height),2) # for Horizontal line


        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)



