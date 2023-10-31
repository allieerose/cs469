import tkinter as tk
from PIL import Image, ImageTk

# icons for cells



class Cell ():
    def __init__(self, root, game, row, column) -> None:
        self._icons = {}
        self.init_icons()

        # construct button object
        self._button = tk.Button(root, state='active', image=self._icons['blank'])
        self._button.bind('<ButtonRelease-1>', self.left_click) # can change activation to <Button-1> if on click rather than click+release
        self._button.bind('<Button-3>', self.right_click)
        self._button.grid(row=row, column=column)
        self._game = game # reference parent game
        self._row = row
        self._column = column
        self._is_bomb = False # by default
        self._flagged = False
    

    def init_icons(self):
        """
        Initializes all icons for later display on cells.
        """
        self._icons['blank'] = tk.PhotoImage(file='icons/blank.png').subsample(4)
        self._icons['mine'] = tk.PhotoImage(file='icons/mine.png').subsample(4)
        self._icons['flag'] = tk.PhotoImage(file='icons/flag.png').subsample(4)
        self._icons[1] = tk.PhotoImage(file='icons/1.png').subsample(4)
        self._icons[2] = tk.PhotoImage(file='icons/2.png').subsample(4)
        self._icons[3] = tk.PhotoImage(file='icons/3.png').subsample(4)
        self._icons[4] = tk.PhotoImage(file='icons/4.png').subsample(4)
        self._icons[5] = tk.PhotoImage(file='icons/5.png').subsample(4)
        self._icons[6] = tk.PhotoImage(file='icons/6.png').subsample(4)
        self._icons[7] = tk.PhotoImage(file='icons/7.png').subsample(4)
        self._icons[8] = tk.PhotoImage(file='icons/8.png').subsample(4)
        self._icons[9] = tk.PhotoImage(file='icons/9.png').subsample(4)

    def left_click(self, event):
        """
        Event handler for left-click of a button.
        """
        if self._flagged:
            return

        event.widget["state"] = "disabled" 
        if self._is_bomb:
            self._button["image"] = self._icons['mine']
            self._game.lose()
        elif event.widget["text"] == "": # ** may need to change later
            self._game.cell_clicked()
            event.widget["text"] = "A"
    
    def right_click(self, event):
        """
        Event handler for right-click of a button.
        """
        
        if self._flagged:
            event.widget["state"] = "active"
            self._button["image"] = self._icons['blank']
        elif event.widget["state"] == "active":
            event.widget["state"] = "disabled"
            self._button["image"] = self._icons['flag']
            self._flagged = True
    
    def set_bomb(self):
        """
        Sets the cell to be a bomb
        """
        self._is_bomb = True
            
