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
            #return the position of the cube
    def click(self, pos):
       
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 6
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self): #check empty boxes in the board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        # Defining Function to solve the sudoku puzzle/board.
        find = find_empty(self.model)# This will find the empty spaces where the zeros are.
        if not find:
            # If the statement for finding the empty spaces is not correct then it will return a boolean with True.
            return True
        else:
            # The Else statement would remove the digit and try another based on the find statement in all row and columns
            row, col = find

        for i in range(1, 9):
            if valid(self.model, i, (row, col)): # If all looks promising then it will make an attempt to solve.
               
                self.model[row][col] = i # Making an attempt to solve.

                if self.solve():# If the solution is a success it will return a boolean with True Statement.
                    return True

                self.model[row][col] = 0# If it fails, it will try again and in doing so trigger the backtracking.

        return False
   

    def solve_gui(self):# Defining Function to solve the sudoku puzzle/board.
        self.update_model()
        find = find_empty(self.model)# This will find the empty spaces where the zeros are.
        if not find:# If the statement for finding the empty spaces is not correct then it will return a boolean with True.
            return True
        else:# The Else statement would remove the digit and try another based on the find statement in all row and columns
            row, col = find

        for i in range(1, 9):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():# If the solution is a success it will return a boolean with True Statement.
                    return True

                self.model[row][col] = 0# If it fails, it will try again and in doing so trigger the backtracking.
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

#6 rows and 6 coloumns
class Cube:
    rows = 6
    cols = 6

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 6
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 6
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val





