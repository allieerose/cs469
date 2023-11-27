import tkinter as tk
from game import Game


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