class InventoryModel:
    def __init__(self):
        # List of bottle objects
        self.items = []
        # Track selected bottle index (for unique bottle display)
        self.selected_index = 0  # Index in the unique bottles list (not all items)
        # Max slots
        self.max_slots = 30

    def add_item(self, item_obj):
        """Add a bottle object to inventory"""
        if len(self.items) < self.max_slots:
            self.items.append(item_obj)
            # Auto-select first item if nothing selected
            if self.selected_index < 0:
                self.selected_index = 0
            print(f"Added: {item_obj.getName()} to inventory.")
            return True
        else:
            print("Inventory full!")
            return False

    def remove_item(self, item_name):
        """Remove first matching bottle"""
        for i, item in enumerate(self.items):
            if item.getName() == item_name:
                self.items.pop(i)
                # Adjust selected index if needed
                unique_bottles = self.get_unique_bottles()
                if self.selected_index >= len(unique_bottles) and self.selected_index > 0:
                    self.selected_index -= 1
                return item
        return None

    def consume_selected(self):
        """Remove and return the first bottle of selected type"""
        unique_bottles = self.get_unique_bottles()
        if not unique_bottles or self.selected_index < 0 or self.selected_index >= len(unique_bottles):
            return None
        
        selected_unique = unique_bottles[self.selected_index]
        bottle_name = selected_unique['name']
        
        # Find and remove first bottle of this type
        for i, item in enumerate(self.items):
            if item.getName() == bottle_name:
                bottle = self.items.pop(i)
                # Adjust selection if needed
                unique_bottles = self.get_unique_bottles()
                if self.selected_index >= len(unique_bottles) and self.selected_index > 0:
                    self.selected_index -= 1
                return bottle
        return None

    def get_all_items(self):
        """Return complete list"""
        return self.items

    def get_selected_item(self):
        """Get currently selected bottle (first of the selected unique type)"""
        unique_bottles = self.get_unique_bottles()
        if unique_bottles and 0 <= self.selected_index < len(unique_bottles):
            return unique_bottles[self.selected_index]['obj']
        return None

    def get_selected_index(self):
        """Get current selection index"""
        return self.selected_index

    def count_by_type(self):
        """Return dict of bottle counts by type name"""
        counts = {}
        for item in self.items:
            name = item.getName()
            counts[name] = counts.get(name, 0) + 1
        return counts

    def get_unique_bottles(self):
        """Get list of unique bottle types with their counts"""
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
        """Move selection to next unique bottle type"""
        unique_bottles = self.get_unique_bottles()
        if len(unique_bottles) > 0:
            self.selected_index = (self.selected_index + 1) % len(unique_bottles)

    def select_previous(self):
        """Move selection to previous unique bottle type"""
        unique_bottles = self.get_unique_bottles()
        if len(unique_bottles) > 0:
            self.selected_index = (self.selected_index - 1) % len(unique_bottles)

    def count_item(self, item_name):
        """Count how many of a specific bottle type"""
        return sum(1 for item in self.items if item.getName() == item_name)