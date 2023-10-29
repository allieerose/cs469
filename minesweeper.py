import tkinter as tk
from stopwatch import Timer
from cells import Cell


root = tk.Tk()
root.title("Minesweeper")

# initialize timer at top of screen
timer = Timer(root)
time_label = timer.get_label()
time_label['font'] = ('Yu Gothic Medium', '16')
time_label.pack()

class Game ():
    def __init__(self, root, timer, rows, columns) -> None:
        self._timer = timer
        self._frame = tk.Frame(root, padx=20, pady=20)
        self._frame.pack()
        self._cells = []
        self._bombs = []
        self._clicked_cells = 0
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Cell(self._frame, self, i, j))
            self._cells.append(row)

    def _start_game(self):
        """
        Triggers the start of the game by starting the game's timer and placing bombs on the board.
        """
        # start timer
        self._timer.start()
        # place bombs
    
    def cell_clicked(self):
        """
        Should be called when a non-bomb cell is clicked. Updates the count of selected cells and triggers
        game start (if first cell clicked) or win state (if all non-bomb cells clicked).
        """
        self._clicked_cells += 1
        if self._clicked_cells == 1:
            self._start_game()
        elif self._clicked_cells == 71: # all non-bomb cells clicked
            self.win()
        
        # TESTING
        if self._clicked_cells % 10 == 0:
            print(self._clicked_cells)
    
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

game = Game(root, timer, 9, 9)

root.mainloop()