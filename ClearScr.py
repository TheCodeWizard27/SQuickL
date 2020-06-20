from os import system, name 

# Hidden class that enables cross platform clear functionality.
class _ClearScr:
    def __init__(self):
        self._clearCmd = "cls" if name == 'nt' else "clear" # Use cls if windows (nt) or clear if unix console

    def __call__(self): system(self._clearCmd)

clear_cl = _ClearScr()