from SelectionHandler import *
from Getch import get_char
from ClearScr import clear_cl

class UIController:
    def __init__(self,selectionHandler, sQuickLHandler):
        self._selectionHandler = selectionHandler
        self._sQuickLHandler = sQuickLHandler

    # Input function that controlls input and output.
    # Return value will be used for next Controller.
    def control_input(self):
        while(True):
            clear_cl()
            self.on_print()
            
            self._selectionHandler.draw()
            key = get_char()

            if(key == b'\r'): return self.on_selection(self._selectionHandler.get_selected_item()) # Selection
            if(key == b'P'): self._selectionHandler.select_next() # Arrow Up
            if(key == b'H'): self._selectionHandler.select_prev() # Arrow Down
            if(key == b'\x03'): raise Exception() # Return ctrl+c functionality.

    def on_print(self): pass # Can be overriden to add something to the print.

    def on_selection(self, item): pass # Needs to be overriden.
    
class MainController(UIController):

    def __init__(self, sQuickHandler):
        super().__init__(SelectionHandler([
            SelectableItem("Execute Query", self._execute_query),
            SelectableItem("Write Query", self._write_query),
            SelectableItem("Manual", self._manual),
            SelectableItem("Quit", self._quit)
        ]), sQuickHandler)

    def _execute_query(self): return QueryListController(self._sQuickLHandler)

    def _write_query(self): return ExecuteQueryController(self._sQuickLHandler)

    def _manual(self): return ManualController(self._sQuickLHandler)

    def _quit(self): return None

    def on_selection(self, item):
        return item.data()

class ManualController(UIController):
    def __init__(self, sQuickHandler):
        super().__init__(SelectionHandler([
            SelectableItem("Back"),
        ]), sQuickHandler)

    def on_print(self):
        self._sQuickLHandler.paramReader.print_usage()

    def on_selection(self, item): return MainController(self._sQuickLHandler)

class QueryListController(UIController):
    def __init__(self, sQuickHandler):
        queries = [
            SelectableItem(key, param) for key, param in sQuickHandler.config.try_get_value("queryList", {}).items()
        ]
        queries += [SelectableItem("Back")]
        super().__init__(SelectionHandler(queries), sQuickHandler)

    def on_selection(self, item):
        if(not item.data): return MainController(self._sQuickLHandler)

        clear_cl()
        self._sQuickLHandler.run_query(item.data)
        return self

class ExecuteQueryController(UIController):
    def __init__(self, sQuickHandler):
        super().__init__(None, sQuickHandler) # Giving None works because the control_input function is overriden.

    def control_input(self):
        clear_cl()

        query = input("Query:")
        self._sQuickLHandler.run_query(query)

        return MainController(self._sQuickLHandler)
