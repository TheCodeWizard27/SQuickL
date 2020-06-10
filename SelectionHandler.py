
class SelectableItem:
    def __init__(self, label, data):
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

            tmpLabel = self.limitName("> " + item.label if item.selected else "" + item.label)
            marginString = " " * self._margin
            print("|" + marginString + tmpLabel + " " * self.getRemainingWidth(tmpLabel) + marginString + "|")

            #print(blankLine)

        print(seperator)

    def limitName(self, label): 
        if(len(label) <= self.getRealWidth()):
            return label
        else:
            # Remove everything after the max length and 3 more to make space for the ...
            return label[:self.getRealWidth()-3] + "..."

    def getRemainingWidth(self, label): return self.getRealWidth() - len(label)

    def getRealWidth(self): return self._width - self._margin*2

    def getSelectedItem(self): return self._items[self._selectedIndex]

    def selectNext(self): 
        self._selectNew(self._selectedIndex+1 if self._selectedIndex < len(self._items)-1 else 0)
    def selectPrev(self): 
        self._selectNew(self._selectedIndex-1 if self._selectedIndex > 0 else len(self._items)-1)

    def _selectNew(self, newValue):
        self._items[self._selectedIndex].selected = False # Deselect current.
        self._selectedIndex = newValue
        self._items[self._selectedIndex].selected = True # Select next.
