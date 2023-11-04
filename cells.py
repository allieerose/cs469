import tkinter as tk

class Cell ():
    def __init__(self, root, game, row, column) -> None:
        # construct button object
        self._button = tk.Button(root, image=game.get_icon('blank'))
        self._button.bind('<ButtonRelease-1>', self.left_click) # can change activation to <Button-1> if on click rather than click+release
        self._button.bind('<Button-3>', self.right_click)
        self._button.grid(row=row, column=column)
        self._game = game # reference parent game
        self._row = row
        self._column = column
        self._is_mine = False # by default
        self._flagged = False
    

    def left_click(self, event):
        """
        Event handler for left-click of a button.
        """
        if self._button['state'] != tk.DISABLED:
            event.widget['state'] = tk.DISABLED
            self._button.after(0, self.deactivate)
            if self._is_mine:
                self._button["image"] = self._game.get_icon('mine')
                self._game.lose()
            else: 
                self._game.cell_clicked(self._row, self._column)
                self._button["image"] = self._game.adjacent_bomb_count(self._row, self._column)

    def deactivate(self):
        self._button['bg'] = 'gray64'
        self._button['relief'] = tk.SUNKEN

    def right_click(self, event):
        """
        Event handler for right-click of a button.
        """
        if self._flagged: # unflag cell
            event.widget["state"] = tk.ACTIVE
            self._button["image"] = self._game.get_icon('blank')
            self._flagged = False
        elif event.widget["state"] != tk.DISABLED:
            event.widget["state"] = tk.DISABLED
            self._button["image"] = self._game.get_icon('flag')
            self._flagged = True
    
    def set_bomb(self):
        """
        Sets the cell to be a bomb
        """
        self._is_mine = True
            
