from Utils.Logger import Logger


class ShopModel:

    def __init__(self, player):
        try:
            self.player = player
            
            self.availableItems = [
                {"name": "Light Beer", "type": "bottle", "price": 8, "category": "Light Beers", "description": "8% alc. Light: +1 damage", "effect": "bottle_light_beer", "alcohol_level": 8, "bonus_damage": 1, "accuracy_penalty": 0},
                {"name": "Beer", "type": "bottle", "price": 15, "category": "Light Beers", "description": "15% alc. Classic: +3 damage, -5% accuracy", "effect": "bottle_beer", "alcohol_level": 15, "bonus_damage": 3, "accuracy_penalty": 5},
                {"name": "Mojito", "type": "bottle", "price": 16, "category": "Cocktails", "description": "10% alc. Refreshing: +2 damage", "effect": "bottle_mojito", "alcohol_level": 10, "bonus_damage": 2, "accuracy_penalty": 0},
                {"name": "Daiquiri", "type": "bottle", "price": 18, "category": "Cocktails", "description": "20% alc. Smooth: +3 damage, -5% accuracy", "effect": "bottle_daiquiri", "alcohol_level": 20, "bonus_damage": 3, "accuracy_penalty": 5},
                {"name": "Margarita", "type": "bottle", "price": 20, "category": "Cocktails", "description": "25% alc. Tangy: +4 damage, -8% accuracy", "effect": "bottle_margarita", "alcohol_level": 25, "bonus_damage": 4, "accuracy_penalty": 8},
                {"name": "Piña Colada", "type": "bottle", "price": 24, "category": "Cocktails", "description": "12% alc. Sweet: +2 damage, -3% accuracy", "effect": "bottle_pina_colada", "alcohol_level": 12, "bonus_damage": 2, "accuracy_penalty": 3},
                {"name": "Vodka", "type": "bottle", "price": 20, "category": "Vodka", "description": "40% alc. Clean: +4 damage, -8% accuracy", "effect": "bottle_vodka", "alcohol_level": 40, "bonus_damage": 4, "accuracy_penalty": 8},
                {"name": "Rum", "type": "bottle", "price": 25, "category": "Rum Varieties", "description": "50% alc. Classic: +0 damage, restores 50 HP", "effect": "bottle_rum", "alcohol_level": 50, "bonus_damage": 0, "accuracy_penalty": 0, "hpRestore": 50},
                {"name": "Spiced Rum", "type": "bottle", "price": 26, "category": "Rum Varieties", "description": "38% alc. Fiery: +5 damage, -10% accuracy", "effect": "bottle_spiced_rum", "alcohol_level": 38, "bonus_damage": 5, "accuracy_penalty": 10},
                {"name": "Whiskey", "type": "bottle", "price": 30, "category": "Whiskey & Spirits", "description": "25% alc. Smooth: +5 damage, -10% accuracy", "effect": "bottle_whiskey", "alcohol_level": 25, "bonus_damage": 5, "accuracy_penalty": 10},
                {"name": "Scotch", "type": "bottle", "price": 32, "category": "Whiskey & Spirits", "description": "45% alc. Premium: +7 damage, -15% accuracy", "effect": "bottle_scotch", "alcohol_level": 45, "bonus_damage": 7, "accuracy_penalty": 15},
                {"name": "Cognac", "type": "bottle", "price": 35, "category": "Whiskey & Spirits", "description": "40% alc. Refined: +6 damage, -12% accuracy", "effect": "bottle_cognac", "alcohol_level": 40, "bonus_damage": 6, "accuracy_penalty": 12},
                {"name": "Tequila", "type": "bottle", "price": 28, "category": "Tequila", "description": "35% alc. Wild: +6 damage, -12% accuracy", "effect": "bottle_tequila", "alcohol_level": 35, "bonus_damage": 6, "accuracy_penalty": 12},
                {"name": "Absinthe", "type": "bottle", "price": 50, "category": "Extreme", "description": "68% alc. EXTREME: +8 damage, -18% accuracy", "effect": "bottle_absinthe", "alcohol_level": 68, "bonus_damage": 8, "accuracy_penalty": 18},
                {"name": "Amplifier", "type": "upgrade", "price": 50, "category": "Upgrades", "description": "Damage upgrade: +3 permanently", "effect": "upgrade_damage"}
            ]
            
            self.selectedIndex = 0
            self.currentPage = 0
            self.itemsPerPage = 8
            self.purchaseSuccess = False
            self.purchaseMessage = ""
            
            Logger.debug("ShopModel.__init__", "Shop model initialized", 
                        currency=self.player.getCurrency(),
                        itemsCount=len(self.availableItems))
        except Exception as e:
            Logger.error("ShopModel.__init__", e)
            raise


    def getPlayer(self):
        try:
            return self.player
        except Exception as e:
            Logger.error("ShopModel.getPlayer", e)
            return None
    
    def setPlayer(self, player):
        try:
            self.player = player
            Logger.debug("ShopModel.setPlayer", "Player set", playerName=player.getName() if player else "None")
        except Exception as e:
            Logger.error("ShopModel.setPlayer", e)
    
    def getPlayerCurrency(self):
        try:
            return self.player.getCurrency()
        except Exception as e:
            Logger.error("ShopModel.getPlayerCurrency", e)
            return 0
    
    def setPlayerCurrency(self, amount):
        try:
            self.player.setCurrency(max(0, amount))
            Logger.debug("ShopModel.setPlayerCurrency", "Currency updated", amount=self.player.getCurrency())
        except Exception as e:
            Logger.error("ShopModel.setPlayerCurrency", e)
    
    def getAvailableItems(self):
        try:
            return self.availableItems.copy()
        except Exception as e:
            Logger.error("ShopModel.getAvailableItems", e)
            return []
    
    def setAvailableItems(self, items):
        try:
            if isinstance(items, list):
                self.availableItems = items.copy()
                Logger.debug("ShopModel.setAvailableItems", "Available items set", count=len(self.availableItems))
            else:
                Logger.error("ShopModel.setAvailableItems", ValueError("Items must be a list"))
        except Exception as e:
            Logger.error("ShopModel.setAvailableItems", e)
    
    def getSelectedIndex(self):
        try:
            return self.selectedIndex
        except Exception as e:
            Logger.error("ShopModel.getSelectedIndex", e)
            return 0
    
    def setSelectedIndex(self, index):
        try:
            if 0 <= index < len(self.availableItems):
                self.selectedIndex = index
                Logger.debug("ShopModel.setSelectedIndex", "Selection changed", index=index)
        except Exception as e:
            Logger.error("ShopModel.setSelectedIndex", e)
    
    def getPurchaseMessage(self):
        try:
            return self.purchaseMessage
        except Exception as e:
            Logger.error("ShopModel.getPurchaseMessage", e)
            return ""
    
    def setPurchaseMessage(self, message):
        try:
            self.purchase_message = str(message) if message else ""
            Logger.debug("ShopModel.setPurchaseMessage", "Purchase message set", purchaseMessage=self.purchaseMessage)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseMessage", e)
    
    def isPurchaseSuccess(self):
        try:
            return self.purchaseSuccess
        except Exception as e:
            Logger.error("ShopModel.isPurchaseSuccess", e)
            return False
    
    def setPurchaseSuccess(self, success):
        try:
            self.purchaseSuccess = bool(success)
            Logger.debug("ShopModel.setPurchaseSuccess", "Purchase success set", success=self.purchaseSuccess)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseSuccess", e)


    def purchaseItem(self, itemIndex):
        try:
            if itemIndex < 0 or itemIndex >= len(self.availableItems):
                self.setPurchaseMessage("Invalid item selection")
                self.setPurchaseSuccess(False)
                Logger.debug("ShopModel.purchaseItem", "Invalid item index", index=itemIndex)
                return False
            
            item = self.availableItems[itemIndex]
            price = item["price"]
            
            if self.player.getCurrency() < price:
                self.setPurchaseMessage(f"Not enough currency! Need ${price}, have ${self.player.getCurrency()}")
                self.setPurchaseSuccess(False)
                Logger.debug("ShopModel.purchaseItem", "Insufficient currency", 
                           required=price, available=self.player.getCurrency())
                return False
            
            try:
                if item["type"] == "bottle":
                    from Models.BottleModel import BottleModel
                    
                    alcohol_level = item.get("alcohol_level", 0)
                    bonus_damage = item.get("bonus_damage", 0)
                    accuracy_penalty = item.get("accuracy_penalty", 0)
                    hpRestore = item.get("hpRestore", 0)
                    
                    bottle = BottleModel(item["name"], alcohol_level, bonus_damage, accuracy_penalty)
                    
                    if hpRestore > 0:
                        current_hp = self.player.getHealth()
                        self.player.setHealth(min(100, current_hp + hpRestore))
                        self.setPurchaseMessage(f"Purchased {item['name']}! Restored {hpRestore} HP, bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", f"{item['name']} purchased", 
                                   newHp=self.player.getHealth())
                    else:
                        self.setPurchaseMessage(f"Purchased {item['name']}! Bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", f"{item['name']} purchased")
                    
                    if hasattr(self.player, 'inventory'):
                        self.player.inventory.addItem(bottle)
                    
                elif item["type"] == "upgrade":
                    if item["effect"] == "upgrade_damage":
                        current_damage = self.player.getDamage()
                        self.player.setDamage(current_damage + 3)
                        self.setPurchaseMessage(f"Purchased {item['name']}! Damage increased by +3.")
                        Logger.debug("ShopModel.purchaseItem", "Amplifier purchased", 
                                   new_damage=self.player.getDamage())
                
                self.player.setCurrency(self.player.getCurrency() - price)
                self.setPurchaseSuccess(True)
                Logger.debug("ShopModel.purchaseItem", "Purchase successful", 
                           item=item["name"], remainingCurrency=self.player.getCurrency())
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

    def nextPage(self):
        try:
            maxPage = (len(self.availableItems) - 1) // self.itemsPerPage
            if self.currentPage < maxPage:
                self.currentPage += 1
                self.selectedIndex = self.currentPage * self.itemsPerPage
                Logger.debug("ShopModel.nextPage", "Page changed", page=self.currentPage)
        except Exception as e:
            Logger.error("ShopModel.nextPage", e)

    def previousPage(self):
        try:
            if self.currentPage > 0:
                self.currentPage -= 1
                self.selectedIndex = self.currentPage * self.itemsPerPage
                Logger.debug("ShopModel.previousPage", "Page changed", page=self.currentPage)
        except Exception as e:
            Logger.error("ShopModel.previousPage", e)

    def getCurrentPage(self):
        return self.currentPage

    def getPageCount(self):
        try:
            return (len(self.availableItems) - 1) // self.itemsPerPage + 1
        except Exception as e:
            Logger.error("ShopModel.getPageCount", e)
            return 1

    def getItemsForCurrentPage(self):
        try:
            startIdx = self.currentPage * self.itemsPerPage
            endIdx = startIdx + self.itemsPerPage
            return self.availableItems[startIdx:endIdx]
        except Exception as e:
            Logger.error("ShopModel.getItemsForCurrentPage", e)
            return []

    def getItemIndexOnCurrentPage(self, pageIndex):
        try:
            if 0 <= pageIndex < len(self.getItemsForCurrentPage()):
                return self.currentPage * self.itemsPerPage + pageIndex
            return 0
        except Exception as e:
            Logger.error("ShopModel.getItemIndexOnCurrentPage", e)
            return 0
       

