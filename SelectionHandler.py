
class SelectableItem:
    def __init__(self, label, data = None):
        self.label = label
        self.data = data
        self.selected = False

class SelectionHandler:
    _width = 40
    _margin = 2
    _selectedIndex = 0

    def __init__(self, selectableItems):
        self._items = selectableItems
        self._items[0].selected = True

    def draw(self):
        seperator = "+" + "-"*self._width + "+"
        blankLine = "|" + " "*self._width + "|"

        print(seperator)

        for item in self._items:
            #print(blankLine) 

            tmpLabel = self.limit_name("> " + item.label if item.selected else "" + item.label)
            marginString = " " * self._margin
            print("|" + marginString + tmpLabel + " " * self.get_remaining_width(tmpLabel) + marginString + "|")

            #print(blankLine)

        print(seperator)

    def limit_name(self, label): 
        if(len(label) <= self.get_real_width()):
            return label
        else:
            # Remove everything after the max length and 3 more to make space for the ...
            return label[:self.get_real_width()-3] + "..."

    def get_remaining_width(self, label): return self.get_real_width() - len(label)

    def get_real_width(self): return self._width - self._margin*2

    def get_selected_item(self): return self._items[self._selectedIndex]

    def select_next(self): 
        self._select_new(self._selectedIndex+1 if self._selectedIndex < len(self._items)-1 else 0)
    def select_prev(self): 
        self._select_new(self._selectedIndex-1 if self._selectedIndex > 0 else len(self._items)-1)

    def _select_new(self, newValue):
        self._items[self._selectedIndex].selected = False # Deselect current.
        self._selectedIndex = newValue
        self._items[self._selectedIndex].selected = True # Select next.
