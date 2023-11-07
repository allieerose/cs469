import tkinter as tk
from stopwatch import Timer
from cells import Cell
import random
#from PIL import Image, ImageTk

class Game ():
    def __init__(self, root, timer, rows, columns) -> None:
        self._timer = timer
        self._frame = tk.Frame(root, padx=20, pady=20)
        self._frame.pack()
        self._icons = {}
        self._init_icons()
        self._cells = []
        self._bombs = []
        self._clicked_cells = 0
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Cell(self._frame, self, i, j))
            self._cells.append(row)

    def _init_icons(self):
        """
        Initializes all icons for later display on cells.
        """
        self._icons['blank'] = tk.PhotoImage(file='icons/blank.png').subsample(3)
        self._icons['mine'] = tk.PhotoImage(file='icons/mine.png').subsample(3)
        self._icons['flag'] = tk.PhotoImage(file='icons/flag.png').subsample(3)
        self._icons[1] = tk.PhotoImage(file='icons/1.png').subsample(3)
        self._icons[2] = tk.PhotoImage(file='icons/2.png').subsample(3)
        self._icons[3] = tk.PhotoImage(file='icons/3.png').subsample(3)
        self._icons[4] = tk.PhotoImage(file='icons/4.png').subsample(3)
        self._icons[5] = tk.PhotoImage(file='icons/5.png').subsample(3)
        self._icons[6] = tk.PhotoImage(file='icons/6.png').subsample(3)
        self._icons[7] = tk.PhotoImage(file='icons/7.png').subsample(3)
        self._icons[8] = tk.PhotoImage(file='icons/8.png').subsample(3)
        self._icons[9] = tk.PhotoImage(file='icons/9.png').subsample(3)
    
    def get_icon(self, name):
        """
        Takes a string and returns the PhotoImage icon.
        """
        return self._icons[name]

    def _start_game(self, row, column):
        """
        Triggers the start of the game by starting the game's timer and placing bombs on the board.
        """
        # start timer
        self._timer.start()
        # place 10 bombs
        for i in range(10):
            bomb_location = (random.randint(0, 8), random.randint(0,8))
            while bomb_location in self._bombs or bomb_location == (row, column):
                bomb_location = (random.randint(0, 8), random.randint(0,8))
            self._bombs.append(bomb_location)
            self._cells[bomb_location[0]][bomb_location[1]].set_bomb()

            # TESTING !!!
            print(bomb_location) 
    
    def cell_clicked(self, row, column):
        """
        Should be called when a non-bomb cell is clicked. Updates the count of selected cells and triggers
        game start (if first cell clicked) or win state (if all non-bomb cells clicked).
        """
        self._clicked_cells += 1
        if self._clicked_cells == 1:
            self._start_game(row, column)
        elif self._clicked_cells == 71: # all non-bomb cells clicked
            self.win()
        
        # TESTING
        if self._clicked_cells % 10 == 0:
            print(self._clicked_cells)
    
    def adjacent_bomb_count(self, row, column):
        """
        Returns the number of adjacent bombs to the given row, col.
        """
        count = 0
        for i in range(row-1, row+2):
            for j in range(column-1, column+2):
                if (i,j) in self._bombs:
                    count += 1
        if count > 0:
            return self._icons[count]
        else: # 0 adjacent bombs
            return self._icons['blank']

    def win(self):
        """
        Performs the win-state functions of the game, including stopping the timer, making all cells inactive,
        and showing win-state info in a pop-up.
        """
        self._timer.stop()
        # perform win-state actions

    def lose(self):
        """
        Performs the lose-state functions of the game, including stopping the timer, making all cells inactive,
        showing all remaining bombs on the board, and showing lose-state info in a pop-up.
        """
        self._timer.stop()
        # perform lose-state actions