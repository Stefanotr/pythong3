class InventoryModel:
    
    def __init__(self):
        self.items = []
        self.selectedIndex = 0
        self.maxSlots = 30


    def addItem(self, itemObject):
        if len(self.items) < self.maxSlots:
            self.items.append(itemObject)
            if self.selectedIndex < 0:
                self.selectedIndex = 0
            print(f"Added: {itemObject.getName()}")
            return True
        else:
            print("Inventory full!")
            return False

    def removeItem(self, itemName):
        for i, item in enumerate(self.items):
            if item.getName() == itemName:
                self.items.pop(i)
                uniqueBottles = self.getUniqueBottles()
                if self.selectedIndex >= len(uniqueBottles) and self.selectedIndex > 0:
                    self.selectedIndex -= 1
                return item
        return None

    def consumeSelected(self):
        uniqueBottles = self.getUniqueBottles()
        if not uniqueBottles or self.selectedIndex < 0 or self.selectedIndex >= len(uniqueBottles):
            return None
        
        selectedUnique = uniqueBottles[self.selectedIndex]
        bottleName = selectedUnique['name']
        
        for i, item in enumerate(self.items):
            if item.getName() == bottleName:
                bottle = self.items.pop(i)
                uniqueBottles = self.getUniqueBottles()
                if self.selectedIndex >= len(uniqueBottles) and self.selectedIndex > 0:
                    self.selectedIndex -= 1
                return bottle
        return None


    def getAllItems(self):
        return self.items

    def getSelectedItem(self):
        uniqueBottles = self.getUniqueBottles()
        if uniqueBottles and 0 <= self.selectedIndex < len(uniqueBottles):
            return uniqueBottles[self.selectedIndex]['obj']
        return None

    def getSelectedIndex(self):
        return self.selectedIndex


    def countByType(self):
        counts = {}
        for item in self.items:
            name = item.getName()
            counts[name] = counts.get(name, 0) + 1
        return counts

    def getUniqueBottles(self):
        counts = self.countByType()
        result = []
        seen = set()
        for item in self.items:
            name = item.getName()
            if name not in seen:
                result.append({'name': name, 'count': counts[name], 'obj': item})
                seen.add(name)
        return result


    def selectNext(self):
        uniqueBottles = self.getUniqueBottles()
        if len(uniqueBottles) > 0:
            self.selectedIndex = (self.selectedIndex + 1) % len(uniqueBottles)

    def selectPrevious(self):
        uniqueBottles = self.getUniqueBottles()
        if len(uniqueBottles) > 0:
            self.selectedIndex = (self.selectedIndex - 1) % len(uniqueBottles)


    def count_item(self, item_name):

        return sum(1 for item in self.items if item.getName() == item_name)