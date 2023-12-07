import tkinter as tk
from stopwatch import Timer
from cells import Cell
import random
#from PIL import Image, ImageTk

class Game ():
    def __init__(self, master, root, rows, columns, num_bombs) -> None:
        # maintain reference to App 
        self._master = master
        # reference to main window
        self._root = root
        # set up timer
        self._timer = Timer(self._root)
        time_label = self._timer.get_label()
        time_label['font'] = ('Yu Gothic Medium', '16')
        time_label.pack()
        # set up grid of cells
        self._frame = tk.Frame(self._root, padx=20, pady=20)
        self._frame.pack()
        self._icons = {}
        self._init_icons()
        self._cells = []
        self._bomb_count = num_bombs # number of bombs to place on the board
        self._rows = rows
        self._columns = columns
        self._bombs = []
        self._clicked_cells = 0
        for i in range(self._rows):
            row = []
            for j in range(self._columns):
                row.append(Cell(self._frame, self, i, j))
            self._cells.append(row)

    def _init_icons(self):
        """
        Initializes all icons for later display on cells.
        """
        self._icons['blank'] = tk.PhotoImage(file='icons/blank.png').subsample(3)
        self._icons['mine'] = tk.PhotoImage(file='icons/mine.png').subsample(3)
        self._icons['flag'] = tk.PhotoImage(file='icons/flag.png').subsample(3)
        self._icons['xflag'] = tk.PhotoImage(file='icons/xflag.png').subsample(3)
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
        # place [bomb_count] number of bombs randomly on board
        for i in range(self._bomb_count):
            bomb_location = (random.randint(0, self._rows - 1), random.randint(0, self._columns - 1))
            while bomb_location in self._bombs or bomb_location == (row, column):
                bomb_location = (random.randint(0, self._rows - 1), random.randint(0,self._columns - 1))
            self._bombs.append(bomb_location)
            self._cells[bomb_location[0]][bomb_location[1]].set_bomb()
            # update the adjacent bomb count for all adjacent cells
            self.add_adjacent_bombs(bomb_location[0], bomb_location[1]) 

            # TESTING
            #print(bomb_location) 
    
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
        elif self._clicked_cells == (self._rows * self._columns) - self._bomb_count: # all non-bomb cells clicked
            # TESTING
            print(f'Final cell: ', row, ' ', column)
            
            self._cells[row][column].reveal_adj_mines()
            self.win()
        
        # TESTING
        #if self._clicked_cells % 10 == 0:
        #    print(self._clicked_cells)
    
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
        for i in range(max(0, row-1), min(self._rows, row+2)):
            for j in range(max(0, column-1), min(self._columns, column+2)):
                if (i,j) != (row, column):
                    adj_cells.append((i,j))
        
        return adj_cells

    def win(self):
        """
        Performs the win-state functions of the game, including stopping the timer, making all cells inactive,
        and showing win-state info in a pop-up.
        """
        self._timer.stop()
        # set all cells to inactive
        self.deactivate_board()
        # call pop-up
        final_time = self._timer.get_final_time()
        if final_time[0] == "00":
            win_message = "You won in "+ final_time[1]+ " seconds. \n Play again?"
        elif final_time[0] == "01":
            win_message = "You won in " + final_time[0]+ " minute and "+ final_time[1]+ " seconds. \n Play again?"
        else:
            win_message = "You won in " + final_time[0]+ " minutes and "+ final_time[1]+ " seconds. \n Play again?"
        self.popup(True, win_message)

    def lose(self):
        """
        Performs the lose-state functions of the game, including stopping the timer, making all cells inactive,
        showing all remaining bombs on the board, and showing lose-state info in a pop-up.
        """
        self._timer.stop()
        # perform lose-state actions

        # compile game info
        correct_flags = 0
        incorrect_flags = 0
        unflagged_bombs = 0
        for i in range(self._rows):
            for j in range(self._columns):
                if (i,j) in self._bombs:
                    if self._cells[i][j].get_if_flagged():
                        # cell is a bomb and was flagged
                        correct_flags += 1
                    else:
                        # cell is a bomb and was NOT flagged
                        unflagged_bombs += 1
                        # reveal bomb
                        self._cells[i][j].reveal_bad_cell()

                elif self._cells[i][j].get_if_flagged():
                    # cell is not a bomb and is flagged
                    incorrect_flags += 1
                    # mark flag as incorrect
                    self._cells[i][j].reveal_bad_cell()
        
        # set all cells to inactive
        self.deactivate_board()

        # call pop-up
        message = ("OOPS, you clicked on a mine!\n"
        f"You correctly flagged {correct_flags} bomb(s), incorrectly flagged {incorrect_flags} cells(s), and"
        f" missed {unflagged_bombs} bomb(s) on the board.\n Play again?")
        self.popup(False, message)
    
    def deactivate_board(self):
        """
        Deactivates all cells on the board so they are no longer function when left/right clicked.
        """
        for row in self._cells:
            for cell in row:
                cell.set_inactive()

    def popup(self, win, message):
        """
        Creates a pop-up upon a win or lose state, displaying the given message and providing options to quit the 
        game or start a new game.

        :boolean win: indicates whether the game was won or lost (impacts pop-up title)
        """
        toplevel = tk.Toplevel()
        if win:
            toplevel.title('You won!')
        else:
            toplevel.title('Too bad.')
        frame = tk.Frame(toplevel, padx=20, pady=20)
        frame.pack()
        output = tk.Label(frame, text=message)
        output.pack()
        replay_button = tk.Button(frame, text='Replay', command=lambda: self.new_game(toplevel))
        replay_button.pack()
        menu_button = tk.Button(frame, text='Return to Menu', command=lambda: self.return_to_menu(toplevel))
        menu_button.pack()
        quit_button = tk.Button(frame, text='Quit', command=lambda: self.end_game(toplevel, True))
        quit_button.pack()

    def new_game(self, popup):
        """
        Ends the pop-up window and the current game before starting a new game.
        """
        self.end_game(popup, False)
        self._master.make_new_game(self._rows, self._columns, self._bomb_count)
    
    def return_to_menu(self, popup):
        """
        Ends the pop-up window and returns to the start menu screen.
        """
        self.end_game(popup, False)
        self._master.open_start_menu()

    def end_game(self, popup, close_root_window):
        """
        Ends the pop-up window (with win or lose message). If close_root_window is true, also closes
        the main game window. Otherwise, removes game content from root window but doesn't close it.
        """
        popup.destroy()
        if close_root_window:
            self._root.destroy()
        else:
            self._timer.get_label().destroy()
            self._frame.destroy()