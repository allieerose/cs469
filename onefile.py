import tkinter as tk
import random
import time
import sys
import os

class Timer ():
    def __init__(self, root) -> None:
        self._start_time = None
        self._end_time = None
        self._label = tk.Label(root, text='00:00')

    def get_label(self):
        """
        Returns a string of form MM:SS representing time passed since starting the timer.
        """
        return self._label

    def start(self):
        """
        Starts the timer.
        """
        self._start_time = time.time()
        self._update_time()

    def is_active(self):
        """
        Returns a Boolean value indicating if the timer is currently running
        (i.e., has been started and has not been stopped).
        """
        return self._start_time is not None and self._end_time is None
    
    def _update_time(self):
        """
        A private method to update the time label each second.
        """
        if self.is_active():
            time_diff = time.time() - self._start_time
            seconds = self._format_time(time_diff % 60)
            minutes = self._format_time(time_diff // 60)
            self._label['text']= minutes + ':' + seconds
            self._label.after(1000, self._update_time) # recalls this function each second to update
    
    def _format_time(self, time):
        """
        A private method to format and return the given time as a string. Includes a leading 0 if given time is < 10 units.
        """
        time_str = ''
        if time < 10:
            time_str += '0'
        time_str += str(int(time))
        return time_str
    
    def stop(self):
        """
        Stops the timer.
        """
        self._end_time = time.time()
    
    def get_final_time(self):
        """
        Returns a tuple of form (minutes, seconds) representing the final time. Note that
        the stopwatch must have been started and stopped to retrieve a final time. Otherwise,
        None is returned. 
        """
        if self._end_time is not None:
            seconds = self._format_time((self._end_time - self._start_time) % 60)
            minutes = self._format_time((self._end_time - self._start_time) // 60)
            return (minutes, seconds)

class Cell ():
    def __init__(self, root, game, row, column) -> None:
        # construct button object
        self._button = tk.Button(root, image=game.get_icon('blank'), command=self.left_click)
        self._button.bind('<Button-3>', self.right_click)
        self._button.grid(row=row, column=column)
        self._game = game # reference parent game
        self._row = row
        self._column = column
        # by default:
        self._is_mine = False 
        self._flagged = False
        self._adjacent_mines = 0
    
    def add_adjacent_bomb(self):
        """
        Adds 1 to the count of adjacent mines. 
        """
        self._adjacent_mines += 1

    def left_click(self):
        """
        Event handler for left-click of a button.
        """
        if not self._flagged and self._button is not None: # if the button is not flagged and has not been previously left-clicked
            self._button.configure(
                command=lambda: None,
                relief=tk.SUNKEN,
                background='gray64'
            )
            if self._is_mine:
                self._button["image"] = self._game.get_icon('mine')
                self._game.lose()
            else:
                self._game.cell_clicked(self._row, self._column)
                if self._adjacent_mines == 0: 
                    self._button = None
                    self._game.zero_cell_reveals(self._row, self._column)
                else:
                    if self._button is not None: # this check is to avoid an error when the final cell is clicked
                        self._button["image"] = self._game.get_icon(self._adjacent_mines)
                        self._button = None # remove button reference to indicate button should no longer function
                

    def right_click(self, event):
        """
        Event handler for right-click of a button.
        """
        if self._flagged and self._button is not None: 
            # unflag cell
            self._button["image"] = self._game.get_icon('blank')
            self._flagged = False
        elif self._button is not None: # if the button has not been left-clicked
            self._button["image"] = self._game.get_icon('flag')
            self._flagged = True
    
    def set_bomb(self):
        """
        Sets the cell to be a bomb.
        """
        self._is_mine = True
            
    def reveal_adj_mines(self):
        """
        Performs the button appearance change to reveal the number of adjacent bombs without the cell having
        been left-clicked. This is a helper method for revealing cells adjacent to a revealed 0-value cell. 
        """
        if self._is_mine: # for testing purposes
            print("ERROR! NON-0 CELL PICKED IN METHOD")

        if self._button is not None:
            self._button.configure(
                command=lambda: None,
                relief=tk.SUNKEN,
                background='gray64',
                image=self._game.get_icon(self._adjacent_mines)
            )
            self._button = None # cell should be inactive after being revealed
    
    def get_adj_mine_count(self):
        """
        Returns the number of recorded adjacent mines.
        """
        if self._button is None or self._is_mine:
            # the mine count for this cell is irrelevant (either it is inactive or is a mine)
            return -1 
        return self._adjacent_mines
    
    def get_if_flagged(self):
        """
        Returns True if the cell is flagged; returns False otherwise. 
        """
        return self._flagged
    
    def set_inactive(self):
        """
        Sets the cell to inactive so it has no functionality if clicked. Note: no appearance change occurs.
        """
        self._button = None

class Game ():
    def __init__(self, master, rows, columns) -> None:
        # maintain reference to App 
        self._master = master
        # set up window
        self._root = tk.Tk()
        self._root.title("Minesweeper")
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
        self._bombs = []
        self._clicked_cells = 0
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Cell(self._frame, self, i, j))
            self._cells.append(row)
        # run application
        self._root.mainloop()

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

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
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
            # TESTING
            print(f'Final cell: ', row, ' ', column)
            
            self._cells[row][column].reveal_adj_mines()
            self.win()
        
        # TESTING
        if self._clicked_cells % 10 == 0:
            print(self._clicked_cells)
    
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

        # set all cells to inactive
        self.deactivate_board()
        # call pop-up
        correct_flags = 0
        incorrect_flags = 0
        unflagged_bombs = 0
        for i in range(9):
            for j in range(9):
                if (i,j) in self._bombs:
                    if self._cells[i][j].get_if_flagged():
                        # cell is a bomb and was flagged
                        correct_flags += 1
                    else:
                        # cell is a bomb and was NOT flagged
                        unflagged_bombs += 1
                elif self._cells[i][j].get_if_flagged():
                    # cell is not a bomb and is flagged
                    incorrect_flags += 1
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
        quit_button = tk.Button(frame, text='Quit', command=lambda: self.end_game(toplevel))
        quit_button.pack() # TODO: add function to quit

    def new_game(self, popup):
        """
        Ends the pop-up window and the current game before starting a new game
        """
        self.end_game(popup)
        self._master.make_new_game()

    def end_game(self, popup):
        """
        Ends the pop-up window (with win or lose message) and the main game
        """
        popup.destroy()
        self._root.destroy()

class MinesweeperApp():
    def __init__(self):
        # initializes with a game
        game = Game(self, 9, 9)
    
    def make_new_game(self):
        """
        Starts a new game of minesweeper.
        """
        game = Game(self, 9,9)

MinesweeperApp()