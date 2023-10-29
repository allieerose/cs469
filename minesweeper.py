import tkinter as tk
from stopwatch import Timer
from cells import Cell
from game import Game


root = tk.Tk()
root.title("Minesweeper")

# initialize timer at top of screen
timer = Timer(root)
time_label = timer.get_label()
time_label['font'] = ('Yu Gothic Medium', '16')
time_label.pack()

game = Game(root, timer, 9, 9)

root.mainloop()