"""
ShopModel Module

Manages shop state, available items, player currency, and purchase logic.
"""

from Utils.Logger import Logger


# === SHOP MODEL CLASS ===

class ShopModel:
    """
    Model for managing shop state and items.
    Handles available items, player currency, and purchase transactions.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, player):
        """
        Initialize the shop model.
        
        Args:
            player: PlayerModel instance to track currency and inventory
        """
        try:
            self.player = player
            self.player_currency = 100  # Starting currency (can be adjusted)
            
            # Available shop items
            self.available_items = [
                {
                    "name": "Health Potion",
                    "type": "consumable",
                    "price": 20,
                    "description": "Restores 50 HP",
                    "effect": "heal_50"
                },
                {
                    "name": "Beer",
                    "type": "bottle",
                    "price": 15,
                    "description": "Increases drunkenness (+15), damage (+3), accuracy (-5%)",
                    "effect": "bottle_beer"
                },
                {
                    "name": "Whiskey",
                    "type": "bottle",
                    "price": 30,
                    "description": "Strong drink: drunkenness (+25), damage (+5), accuracy (-10%)",
                    "effect": "bottle_whiskey"
                },
                {
                    "name": "Guitar String",
                    "type": "upgrade",
                    "price": 50,
                    "description": "Permanently increases damage by +2",
                    "effect": "upgrade_damage"
                }
            ]
            
            self.selected_index = 0
            self.purchase_success = False
            self.purchase_message = ""
            
            Logger.debug("ShopModel.__init__", "Shop model initialized", 
                        currency=self.player_currency,
                        items_count=len(self.available_items))
        except Exception as e:
            Logger.error("ShopModel.__init__", e)
            raise
    
    # === GETTERS / SETTERS ===
    
    def getPlayer(self):
        """
        Get the player model instance.
        
        Returns:
            PlayerModel: Player model instance
        """
        try:
            return self.player
        except Exception as e:
            Logger.error("ShopModel.getPlayer", e)
            return None
    
    def setPlayer(self, player):
        """
        Set the player model instance.
        
        Args:
            player: PlayerModel instance
        """
        try:
            self.player = player
            Logger.debug("ShopModel.setPlayer", "Player set", player_name=player.getName() if player else "None")
        except Exception as e:
            Logger.error("ShopModel.setPlayer", e)
    
    def getPlayerCurrency(self):
        """
        Get the player's current currency.
        
        Returns:
            int: Current currency amount
        """
        try:
            return self.player_currency
        except Exception as e:
            Logger.error("ShopModel.getPlayerCurrency", e)
            return 0
    
    def setPlayerCurrency(self, amount):
        """
        Set the player's currency amount.
        
        Args:
            amount: New currency amount
        """
        try:
            self.player_currency = max(0, amount)
            Logger.debug("ShopModel.setPlayerCurrency", "Currency updated", amount=self.player_currency)
        except Exception as e:
            Logger.error("ShopModel.setPlayerCurrency", e)
    
    def getAvailableItems(self):
        """
        Get the list of available shop items.
        
        Returns:
            list: List of item dictionaries
        """
        try:
            return self.available_items.copy()  # Return a copy to prevent external modification
        except Exception as e:
            Logger.error("ShopModel.getAvailableItems", e)
            return []
    
    def setAvailableItems(self, items):
        """
        Set the list of available shop items.
        
        Args:
            items: List of item dictionaries
        """
        try:
            if isinstance(items, list):
                self.available_items = items.copy()  # Store a copy
                Logger.debug("ShopModel.setAvailableItems", "Available items set", count=len(self.available_items))
            else:
                Logger.error("ShopModel.setAvailableItems", ValueError("Items must be a list"))
        except Exception as e:
            Logger.error("ShopModel.setAvailableItems", e)
    
    def getSelectedIndex(self):
        """
        Get the currently selected item index.
        
        Returns:
            int: Selected item index
        """
        try:
            return self.selected_index
        except Exception as e:
            Logger.error("ShopModel.getSelectedIndex", e)
            return 0
    
    def setSelectedIndex(self, index):
        """
        Set the selected item index.
        
        Args:
            index: Item index to select
        """
        try:
            if 0 <= index < len(self.available_items):
                self.selected_index = index
                Logger.debug("ShopModel.setSelectedIndex", "Selection changed", index=index)
        except Exception as e:
            Logger.error("ShopModel.setSelectedIndex", e)
    
    def getPurchaseMessage(self):
        """
        Get the last purchase message.
        
        Returns:
            str: Purchase message
        """
        try:
            return self.purchase_message
        except Exception as e:
            Logger.error("ShopModel.getPurchaseMessage", e)
            return ""
    
    def setPurchaseMessage(self, message):
        """
        Set the purchase message.
        
        Args:
            message: Purchase message string
        """
        try:
            self.purchase_message = str(message) if message else ""
            Logger.debug("ShopModel.setPurchaseMessage", "Purchase message set", message=self.purchase_message)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseMessage", e)
    
    def isPurchaseSuccess(self):
        """
        Check if the last purchase was successful.
        
        Returns:
            bool: True if purchase succeeded, False otherwise
        """
        try:
            return self.purchase_success
        except Exception as e:
            Logger.error("ShopModel.isPurchaseSuccess", e)
            return False
    
    def setPurchaseSuccess(self, success):
        """
        Set the purchase success status.
        
        Args:
            success: True if purchase succeeded, False otherwise
        """
        try:
            self.purchase_success = bool(success)
            Logger.debug("ShopModel.setPurchaseSuccess", "Purchase success set", success=self.purchase_success)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseSuccess", e)
    
    # === PURCHASE LOGIC ===
    
    def purchaseItem(self, item_index):
        """
        Attempt to purchase an item.
        
        Args:
            item_index: Index of the item to purchase
            
        Returns:
            bool: True if purchase succeeded, False otherwise
        """
        try:
            if item_index < 0 or item_index >= len(self.available_items):
                self.setPurchaseMessage("Invalid item selection")
                self.setPurchaseSuccess(False)
                Logger.debug("ShopModel.purchaseItem", "Invalid item index", index=item_index)
                return False
            
            item = self.available_items[item_index]
            price = item["price"]
            
            # Check if player has enough currency
            if self.player_currency < price:
                self.setPurchaseMessage(f"Not enough currency! Need {price}, have {self.player_currency}")
                self.setPurchaseSuccess(False)
                Logger.debug("ShopModel.purchaseItem", "Insufficient currency", 
                           required=price, available=self.player_currency)
                return False
            
            # Apply item effect
            try:
                if item["type"] == "consumable":
                    if item["effect"] == "heal_50":
                        current_hp = self.player.getHealth()
                        self.player.setHealth(min(100, current_hp + 50))
                        self.setPurchaseMessage(f"Purchased {item['name']}! Restored 50 HP.")
                        Logger.debug("ShopModel.purchaseItem", "Health potion purchased", 
                                   new_hp=self.player.getHealth())
                
                elif item["type"] == "bottle":
                    from Models.BottleModel import BottleModel
                    if item["effect"] == "bottle_beer":
                        bottle = BottleModel("Beer", 15, 3, 5)
                        self.player.setSelectedBottle(bottle)
                        self.setPurchaseMessage(f"Purchased {item['name']}! Bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", "Beer purchased")
                    elif item["effect"] == "bottle_whiskey":
                        bottle = BottleModel("Whiskey", 25, 5, 10)
                        self.player.setSelectedBottle(bottle)
                        self.setPurchaseMessage(f"Purchased {item['name']}! Bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", "Whiskey purchased")
                
                elif item["type"] == "upgrade":
                    if item["effect"] == "upgrade_damage":
                        current_damage = self.player.getDamage()
                        self.player.setDamage(current_damage + 2)
                        self.setPurchaseMessage(f"Purchased {item['name']}! Damage increased by +2.")
                        Logger.debug("ShopModel.purchaseItem", "Damage upgrade purchased", 
                                   new_damage=self.player.getDamage())
                
                # Deduct currency
                self.setPlayerCurrency(self.player_currency - price)
                self.setPurchaseSuccess(True)
                Logger.debug("ShopModel.purchaseItem", "Purchase successful", 
                           item=item["name"], remaining_currency=self.player_currency)
                return True
                
            except Exception as e:
                Logger.error("ShopModel.purchaseItem", e)
                self.setPurchaseMessage(f"Error applying item effect: {str(e)}")
                self.setPurchaseSuccess(False)
                return False
                
        except Exception as e:
            Logger.error("ShopModel.purchaseItem", e)
            self.setPurchaseMessage(f"Purchase failed: {str(e)}")
            self.setPurchaseSuccess(False)
            return False

