import tkinter as tk

class StartMenu():
    def __init__(self, master, root) -> None:
        self._master = master
        self._root = root
        self._frame = tk.Frame(self._root, padx=20, pady=20)
        self._frame.pack()
        # Difficulty options
        difficulty_label = tk.Label(self._frame, text="Select a difficulty")
        difficulty_label.pack()
        self._difficulty = tk.StringVar(value='easy')
        easy_mode = tk.Radiobutton(self._frame, text="Easy", variable=self._difficulty, value='easy')
        easy_mode.pack(anchor=tk.W)
        medium_mode = tk.Radiobutton(self._frame, text="Medium", variable=self._difficulty, value='medium')
        medium_mode.pack(anchor=tk.W)
        hard_mode = tk.Radiobutton(self._frame, text="Hard", variable=self._difficulty, value='hard')
        hard_mode.pack(anchor=tk.W)

        # start game button
        self._new_game = tk.Button(self._frame, text='Start Game', command=self._start_game)
        self._new_game.pack()
        # button for instructions pop-up
        self._instructions_button = tk.Button(self._frame, text='Instructions', command=self._open_instructions)
        self._instructions_button.pack()
    
    def _start_game(self):
        """
        Removes the start menu items from the root window, then requests a game to be started in the window.
        """
        self._frame.pack_forget() # remove start menu items from window
        if self._difficulty.get() == 'easy':
            self._master.make_new_game(9,9,10)
        elif self._difficulty.get() == 'medium':
            self._master.make_new_game(16,16,40)
        else: # hard mode
            self._master.make_new_game(16,30,99)
    
    def open_menu(self):
        """
        Adds the menu elements to the root window. Note that nothing is removed from the root window
        before this; it is assumed the root window is empty. 
        """
        self._frame.pack()

    def _open_instructions(self):
        """
        Creates a pop-up with instructions for playing the game.
        """
        instructions_window = tk.Toplevel()
        instructions_window.title("Instructions")
        frame = tk.Frame(instructions_window, padx=20, pady=20)
        frame.pack()
        with open('instructions.txt', 'r') as text:
            instructions = tk.Label(frame, text=text.read())
        instructions.pack()
        quit_button = tk.Button(frame, text='Close Instructions', command=instructions_window.destroy)
        quit_button.pack()