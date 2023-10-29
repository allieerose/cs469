import time
import tkinter as tk

class Timer ():
    def __init__(self, root) -> None:
        self._start_time = None
        self._end_time = None
        self._label = tk.Label(root, text='00:00')

    def get_label(self):
        """
        Returns a string of form MM:SS representing time passed since starting the timer.
        """
        return self._label

    def start(self):
        """
        Starts the timer.
        """
        self._start_time = time.time()
        self._update_time()

    def is_active(self):
        """
        Returns a Boolean value indicating if the timer is currently running
        (i.e., has been started and has not been stopped).
        """
        return self._start_time is not None and self._end_time is None
    
    def _update_time(self):
        """
        A private method to update the time label each second.
        """
        if self.is_active():
            time_diff = time.time() - self._start_time
            seconds = self._format_time(time_diff % 60)
            minutes = self._format_time(time_diff // 60)
            self._label['text']= minutes + ':' + seconds
            self._label.after(1000, self._update_time) # recalls this function each second to update
    
    def _format_time(self, time):
        """
        A private method to format and return the given time as a string. Includes a leading 0 if given time is < 10 units.
        """
        time_str = ''
        if time < 10:
            time_str += '0'
        time_str += str(int(time))
        return time_str
    
    def stop(self):
        """
        Stops the timer.
        """
        self._end_time = time.time()