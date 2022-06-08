# Refs: https://github.com/tim-hub/Python-Sudoku.git
# GUI.py
import pygame
import time
pygame.font.init()



class Grid:
    board = [# This is the Sudoku Puzzle shown in a array.
        [5, 4, 0, 0, 2, 6],
        [6, 0, 0, 3, 0, 0],
        [4, 0, 5, 6, 0, 0],
        [0, 0, 1, 0, 5, 4],
        [2, 0, 0, 5, 0, 1],
        [0, 5, 0, 4, 0, 2],
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


            if valid(self.model, val, (row,col)) and (self.model):
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
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1,7):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                if solve():
                    return True
                self.model[row][col] = 0
        return False

   

    def solve_gui(self):# Defining Function to solve the sudoku puzzle/board.
        self.update_model()
        find = find_empty(self.model)# This will find the empty spaces where the zeros are.
        if not find:# If the statement for finding the empty spaces is not correct then it will return a boolean with True.
            return True
        else:# The Else statement would remove the digit and try another based on the find statement in all row and columns
            row, col = find

        for i in range(1, 7):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(20)

                if self.solve_gui():# If the solution is a success it will return a boolean with True Statement.
                    return True

                self.model[row][col] = 0# If it fails, it will try again and in doing so trigger the backtracking.
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(2)

        return False

0#6 rows and 6 coloumns
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


def find_empty(bo):# Defining function to find empty squares by 0.
    for i in range(len(bo)):# Finding the empty blanks in the columns of the board.
        for j in range(len(bo[0])):# Finding the empty spaces in the rows, in other words the 0 in the rows of the board.
            if bo[i][j] == 0:# Check if the position is 0.
                return (i, j)  # row, col

    return None# If there is no squares that equals to 0 then it will trigger the find solution and make it true and say we are done.


def valid(bo, num, pos): # Checking each row if its equal to the number entered.
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i: # If the number is in the position we just inserted, it will ignore it.
            return False
    # Checking each columns if its equal to the number inserted.
    # Check column

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i: # If the number is in the position we entered in the column , it will once again ignore it.
            return False

    # Check box
    box_x = pos[1] // 3 # Checks which position squares or boxes we are in the X value. This will give us value 0,1,2.
    box_y = pos[0] // 2# Checks which position squares or boxes we are in the Y value.
   
    # This will loop all elements in those squares/boxes and make sure that the same numbers wont appear twice.
    for i in range(box_y*2, box_y*2+2): # Here we multiply the square that are from the X value with 3 to get to index 6.
        for j in range(box_x *3 , box_x*3+3): # Same as above, we multiply squares from Y value with 3 to get to index 6.
            if bo[i][j] == num and (i,j) != pos: # Checks if all elements in board are equal to the num added, and making sure it doesnt checks same position we added in and finally if that is true, it will return false because of duplicate numbers.
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(secs): #setting time
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((700,700))
    pygame.display.set_caption("Sudoku")   #screen
    board = Grid(6, 6, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)
#checking inserted keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3

                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            #user has selected right value
                            print("Success")
                        else:#user has entered wrong digit
                            print("Wrong")
                            strikes += 1
                        key = None
           #when the game is over
                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

#callinf functions
main()
pygame.quit()


