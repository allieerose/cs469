import tkinter as tk

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