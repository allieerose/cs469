import tkinter as tk

class Cell ():
    def __init__(self, root, game, row, column) -> None:
        # construct button object
        self._button = tk.Button(root, height=2, width=4, state='active')
        self._button.bind('<ButtonRelease-1>', self.left_click) # can change activation to <Button-1> if on click rather than click+release
        self._button.bind('<Button-3>', self.right_click)
        self._button.grid(row=row, column=column)
        self._game = game # reference parent game
        self._row = row
        self._column = column
        self._is_bomb = False # by default
    
    def left_click(self, event):
        """
        Event handler for left-click of a button.
        """
        if self._is_bomb:
            self._game.lose()
        elif event.widget["text"] == "": # ** may need to change later
            self._game.cell_clicked()
            event.widget["text"] = "A"
            event.widget["state"] = "disabled"
    
    def right_click(self, event):
        """
        Event handler for right-click of a button.
        """
        if event.widget["text"] == "B":
            event.widget["text"] = ""
            event.widget["state"] = "active"
        elif event.widget["text"] == "":
            event.widget["text"] = "B"
            event.widget["state"] = "disabled"
            
