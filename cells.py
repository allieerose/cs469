import tkinter as tk

class Cell ():
    def __init__(self, root, game, row, column) -> None:
        # construct button object
        self._button = tk.Button(root, image=game.get_icon('blank'), command=self.left_click)
        #self._button.bind('<ButtonRelease-1>', self.left_click) # can change activation to <Button-1> if on click rather than click+release
        self._button.bind('<Button-3>', self.right_click)
        self._button.grid(row=row, column=column)
        self._game = game # reference parent game
        self._row = row
        self._column = column
        self._is_mine = False # by default
        self._flagged = False
    

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
                self._button["image"] = self._game.adjacent_bomb_count(self._row, self._column)
                self._button = None # remove button reference to indicate button should no longer function


    def right_click(self, event):
        """
        Event handler for right-click of a button.
        """
        if self._flagged: 
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
            
