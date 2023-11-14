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
        Takes one of the following strings: 'mine', 'flag', 'blank'
        or an integer 0-8 and returns the PhotoImage icon.
        Note that 0 is equivalent to 'blank'.
        """
        if name == 0:
            name = 'blank'
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
            # update the adjacent bomb count for all adjacent cells
            self.add_adjacent_bombs(bomb_location[0], bomb_location[1]) 

            # TESTING !!!
            print(bomb_location) 
    
    def add_adjacent_bombs(self, row, column):
        """
        Adds 1 to the adjacent bomb count for all cells adjacent to the cell at the given row, column.
        """
        adj_cells = self.get_adjacent_cell_indices(row,column)
        for (i,j) in adj_cells:
            self._cells[i][j].add_adjacent_bomb()

    def cell_clicked(self, row, column):
        """
        Should be called when a non-bomb cell is clicked. Updates the count of selected cells and triggers
        game start (if first cell clicked) or win state (if all non-bomb cells clicked).
        """
        self._clicked_cells += 1
        if self._clicked_cells == 1:
            self._start_game(row, column)
        elif self._clicked_cells == 71: # all non-bomb cells clicked
            print(f'Final cell: ', row, ' ', column)
            self.win()
        
        # TESTING
        if self._clicked_cells % 10 == 0:
            print(self._clicked_cells)
    
    def adjacent_bomb_count(self, row, column):
        """
        NO LONGER NEEDED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Returns the number of adjacent bombs to the given row, col.
        """
        count = 0
        adj_cells = self.get_adjacent_cell_indices(row, column)
        for cell in adj_cells:
            if (cell[0],cell[1]) in self._bombs:
                count += 1
                
        if count > 0:
            return self._icons[count]
        else: # 0 adjacent bombs
            return self._icons['blank']
    
    def zero_cell_reveals(self, row, column):
        """
        Reveals all cells adjacent to the cell at the given row, column. If any of the revealed
        cells have 0 adjacent mines, those also have all adjacent cells revealed. 
        Note that the given row, column should correspond to a cell with 0 adjacent bombs.
        """
        zero_cells = [(row, column)]
        while len(zero_cells) > 0:
            zero_cell = zero_cells.pop() # remove a zero cell from the list
            adj_cells = self.get_adjacent_cell_indices(zero_cell[0], zero_cell[1])
            for (i,j) in adj_cells:
                if self._cells[i][j].get_adj_mine_count() == 0:
                    zero_cells.append((i,j))
                if self._cells[i][j].get_adj_mine_count() >= 0:
                    self._cells[i][j].reveal_adj_mines()
                    self.cell_clicked(i,j)
        
    def get_adjacent_cell_indices(self, row, column):
        """
        Returns a list of tuples in form (row, column) containing the indices of all
        adjacent cells on the board to the cell at the given row, column.
        """
        adj_cells = []
        for i in range(max(0, row-1), min(9, row+2)):
            for j in range(max(0, column-1), min(9, column+2)):
                if (i,j) != (row, column):
                    adj_cells.append((i,j))
        
        return adj_cells

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