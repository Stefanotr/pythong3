class InventoryModel:
    def __init__(self):
        # On stocke les objets dans une liste
        self.items = []
        # On peut aussi ajouter une limite de place si nécessaire
        self.max_slots = 10

    def add_item(self, item_obj):
        """Ajoute un objet (classe Beer, Whisky ou Champagne) à l'inventaire."""
        if len(self.items) < self.max_slots:
            self.items.append(item_obj)
            print(f"Ajouté : {item_obj.name} à l'inventaire.")
            return True
        else:
            print("Inventaire plein !")
            return False

    def remove_item(self, item_name):
        """Retire le premier objet correspondant au nom donné."""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None

    def get_all_items(self):
        """Retourne la liste complète pour que la Vue puisse l'afficher."""
        return self.items

    def count_item(self, item_name):
        """Compte combien de fois on a un objet spécifique."""
        return sum(1 for item in self.items if item.name == item_name)