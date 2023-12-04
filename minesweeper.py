import tkinter as tk
from game import Game
from startMenu import StartMenu

class MinesweeperApp():
    def __init__(self):
        # initializes with a game
        self._root = tk.Tk()
        self._root.title("Minesweeper")
        self._start_menu = StartMenu(self, self._root)

        # run application
        self._root.mainloop()
    
    def open_start_menu(self):
        """
        Adds the start menu contents to the root window.
        """
        self._start_menu.open_menu()

    def make_new_game(self, rows, columns, bomb_count):
        """
        Starts a new game of minesweeper in the root window.
        """
        Game(self, self._root, rows, columns, bomb_count)

MinesweeperApp()