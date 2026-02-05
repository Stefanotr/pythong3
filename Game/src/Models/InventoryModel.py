class InventoryModel:
    def __init__(self):
        # List of bottle objects
        self.items = []
        # Track selected bottle index
        self.selected_index = -1
        # Max slots
        self.max_slots = 30

    def add_item(self, item_obj):
        """Add a bottle object to inventory"""
        if len(self.items) < self.max_slots:
            self.items.append(item_obj)
            # Auto-select first item
            if self.selected_index == -1:
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
                if self.selected_index >= len(self.items) and self.selected_index > 0:
                    self.selected_index -= 1
                return item
        return None

    def consume_selected(self):
        """Remove and return the selected bottle"""
        if 0 <= self.selected_index < len(self.items):
            bottle = self.items.pop(self.selected_index)
            # Adjust selection
            if self.selected_index >= len(self.items) and self.selected_index > 0:
                self.selected_index -= 1
            return bottle
        return None

    def get_all_items(self):
        """Return complete list"""
        return self.items

    def get_selected_item(self):
        """Get currently selected bottle"""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
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
        """Move selection to next bottle (navigation)"""
        if len(self.items) > 0:
            self.selected_index = (self.selected_index + 1) % len(self.items)

    def select_previous(self):
        """Move selection to previous bottle (navigation)"""
        if len(self.items) > 0:
            self.selected_index = (self.selected_index - 1) % len(self.items)

    def count_item(self, item_name):
        """Count how many of a specific bottle type"""
        return sum(1 for item in self.items if item.getName() == item_name)