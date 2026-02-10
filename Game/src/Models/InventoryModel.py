class InventoryModel:


    def __init__(self):

        self.items = []
        self.selected_index = 0  
        self.max_slots = 30


    def add_item(self, item_obj):
       
        if len(self.items) < self.max_slots:
            self.items.append(item_obj)
            
            if self.selected_index < 0:
                self.selected_index = 0
            print(f"Added: {item_obj.getName()} to inventory.")
            return True
        else:
            print("Inventory full!")
            return False



    def remove_item(self, item_name):
        
        for i, item in enumerate(self.items):
            if item.getName() == item_name:
                self.items.pop(i)
                
                unique_bottles = self.get_unique_bottles()
                if self.selected_index >= len(unique_bottles) and self.selected_index > 0:
                    self.selected_index -= 1
                return item
        return None


    def consume_selected(self):
        
        unique_bottles = self.get_unique_bottles()
        if not unique_bottles or self.selected_index < 0 or self.selected_index >= len(unique_bottles):
            return None
        
        selected_unique = unique_bottles[self.selected_index]
        bottle_name = selected_unique['name']
        
       
        for i, item in enumerate(self.items):
            if item.getName() == bottle_name:
                bottle = self.items.pop(i)
               
                unique_bottles = self.get_unique_bottles()
                if self.selected_index >= len(unique_bottles) and self.selected_index > 0:
                    self.selected_index -= 1
                return bottle
        return None


    def get_all_items(self):
        
        return self.items
    

    def get_selected_item(self):
        
        unique_bottles = self.get_unique_bottles()
        if unique_bottles and 0 <= self.selected_index < len(unique_bottles):
            return unique_bottles[self.selected_index]['obj']
        return None


    def get_selected_index(self):
        
        return self.selected_index



    def count_by_type(self):
       
        counts = {}
        for item in self.items:
            name = item.getName()
            counts[name] = counts.get(name, 0) + 1
        return counts

    def get_unique_bottles(self):
       
        counts = self.count_by_type()
        result = []
        seen = set()
        for item in self.items:
            name = item.getName()
            if name not in seen:
                result.append({'name': name, 'count': counts[name], 'obj': item})
                seen.add(name)
        return result

    def select_next(self):
      
        unique_bottles = self.get_unique_bottles()
        if len(unique_bottles) > 0:
            self.selected_index = (self.selected_index + 1) % len(unique_bottles)


    def select_previous(self):
       
        unique_bottles = self.get_unique_bottles()
        if len(unique_bottles) > 0:
            self.selected_index = (self.selected_index - 1) % len(unique_bottles)

    def count_item(self, item_name):
        
        return sum(1 for item in self.items if item.getName() == item_name)