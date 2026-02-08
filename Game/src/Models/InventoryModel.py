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
                unique_bottles = self.getUniqueBottles()
                if self.selectedIndex >= len(unique_bottles) and self.selectedIndex > 0:
                    self.selectedIndex -= 1
                return item
        return None

    def consumeSelected(self):
        unique_bottles = self.getUniqueBottles()
        if not unique_bottles or self.selectedIndex < 0 or self.selectedIndex >= len(unique_bottles):
            return None
        
        selected_unique = unique_bottles[self.selectedIndex]
        bottle_name = selected_unique['name']
        
        for i, item in enumerate(self.items):
            if item.getName() == bottle_name:
                bottle = self.items.pop(i)
                unique_bottles = self.getUniqueBottles()
                if self.selectedIndex >= len(unique_bottles) and self.selectedIndex > 0:
                    self.selectedIndex -= 1
                return bottle
        return None


    def getAllItems(self):
        return self.items

    def getSelectedItem(self):
        unique_bottles = self.getUniqueBottles()
        if unique_bottles and 0 <= self.selectedIndex < len(unique_bottles):
            return unique_bottles[self.selectedIndex]['obj']
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
        unique_bottles = self.getUniqueBottles()
        if len(unique_bottles) > 0:
            self.selectedIndex = (self.selectedIndex + 1) % len(unique_bottles)

    def selectPrevious(self):
        unique_bottles = self.getUniqueBottles()
        if len(unique_bottles) > 0:
            self.selectedIndex = (self.selectedIndex - 1) % len(unique_bottles)


    def count_item(self, item_name):

        return sum(1 for item in self.items if item.getName() == item_name)