

from Utils.Logger import Logger





class ShopModel:
 
    

    
    def __init__(self, player):
    
        try:
            self.player = player
            
            
            self.available_items = [
               
                {
                    "name": "Light Beer",
                    "type": "bottle",
                    "price": 8,
                    "category": "Light Beers",
                    "description": "8% alc. Light: +1 damage",
                    "effect": "bottle_light_beer",
                    "alcohol_level": 8,
                    "bonus_damage": 1,
                    "accuracy_penalty": 0
                },
                {
                    "name": "Beer",
                    "type": "bottle",
                    "price": 15,
                    "category": "Light Beers",
                    "description": "15% alc. Classic: +3 damage, -5% accuracy",
                    "effect": "bottle_beer",
                    "alcohol_level": 15,
                    "bonus_damage": 3,
                    "accuracy_penalty": 5
                },
               
                {
                    "name": "Mojito",
                    "type": "bottle",
                    "price": 16,
                    "category": "Cocktails",
                    "description": "10% alc. Refreshing: +2 damage",
                    "effect": "bottle_mojito",
                    "alcohol_level": 10,
                    "bonus_damage": 2,
                    "accuracy_penalty": 0
                },
                {
                    "name": "Daiquiri",
                    "type": "bottle",
                    "price": 18,
                    "category": "Cocktails",
                    "description": "20% alc. Smooth: +3 damage, -5% accuracy",
                    "effect": "bottle_daiquiri",
                    "alcohol_level": 20,
                    "bonus_damage": 3,
                    "accuracy_penalty": 5
                },
                {
                    "name": "Margarita",
                    "type": "bottle",
                    "price": 20,
                    "category": "Cocktails",
                    "description": "25% alc. Tangy: +4 damage, -8% accuracy",
                    "effect": "bottle_margarita",
                    "alcohol_level": 25,
                    "bonus_damage": 4,
                    "accuracy_penalty": 8
                },
                {
                    "name": "Piña Colada",
                    "type": "bottle",
                    "price": 24,
                    "category": "Cocktails",
                    "description": "12% alc. Sweet: +2 damage, -3% accuracy",
                    "effect": "bottle_pina_colada",
                    "alcohol_level": 12,
                    "bonus_damage": 2,
                    "accuracy_penalty": 3
                },
               
                {
                    "name": "Vodka",
                    "type": "bottle",
                    "price": 20,
                    "category": "Vodka",
                    "description": "40% alc. Clean: +4 damage, -8% accuracy",
                    "effect": "bottle_vodka",
                    "alcohol_level": 40,
                    "bonus_damage": 4,
                    "accuracy_penalty": 8
                },
               
                {
                    "name": "Rum",
                    "type": "bottle",
                    "price": 25,
                    "category": "Rum Varieties",
                    "description": "50% alc. Classic: +0 damage, restores 50 HP",
                    "effect": "bottle_rum",
                    "alcohol_level": 50,
                    "bonus_damage": 0,
                    "accuracy_penalty": 0,
                    "hp_restore": 50
                },
                {
                    "name": "Spiced Rum",
                    "type": "bottle",
                    "price": 26,
                    "category": "Rum Varieties",
                    "description": "38% alc. Fiery: +5 damage, -10% accuracy",
                    "effect": "bottle_spiced_rum",
                    "alcohol_level": 38,
                    "bonus_damage": 5,
                    "accuracy_penalty": 10
                },
               
                {
                    "name": "Whiskey",
                    "type": "bottle",
                    "price": 30,
                    "category": "Whiskey & Spirits",
                    "description": "25% alc. Smooth: +5 damage, -10% accuracy",
                    "effect": "bottle_whiskey",
                    "alcohol_level": 25,
                    "bonus_damage": 5,
                    "accuracy_penalty": 10
                },
                {
                    "name": "Scotch",
                    "type": "bottle",
                    "price": 32,
                    "category": "Whiskey & Spirits",
                    "description": "45% alc. Premium: +7 damage, -15% accuracy",
                    "effect": "bottle_scotch",
                    "alcohol_level": 45,
                    "bonus_damage": 7,
                    "accuracy_penalty": 15
                },
                {
                    "name": "Cognac",
                    "type": "bottle",
                    "price": 35,
                    "category": "Whiskey & Spirits",
                    "description": "40% alc. Refined: +6 damage, -12% accuracy",
                    "effect": "bottle_cognac",
                    "alcohol_level": 40,
                    "bonus_damage": 6,
                    "accuracy_penalty": 12
                },
         
                {
                    "name": "Tequila",
                    "type": "bottle",
                    "price": 28,
                    "category": "Tequila",
                    "description": "35% alc. Wild: +6 damage, -12% accuracy",
                    "effect": "bottle_tequila",
                    "alcohol_level": 35,
                    "bonus_damage": 6,
                    "accuracy_penalty": 12
                },
               
                {
                    "name": "Absinthe",
                    "type": "bottle",
                    "price": 50,
                    "category": "Extreme",
                    "description": "68% alc. EXTREME: +8 damage, -18% accuracy",
                    "effect": "bottle_absinthe",
                    "alcohol_level": 68,
                    "bonus_damage": 8,
                    "accuracy_penalty": 18
                },
            
                {
                    "name": "Amplifier",
                    "type": "upgrade",
                    "price": 50,
                    "category": "Upgrades",
                    "description": "Damage upgrade: +3 permanently",
                    "effect": "upgrade_damage"
                }
            ]
            
            


            self.selected_index = 0
            self.current_page = 0
            self.items_per_page = 8
            self.purchase_success = False
            self.purchase_message = ""
            
            Logger.debug("ShopModel.__init__", "Shop model initialized", 
                        currency=self.player.getCurrency(),
                        items_count=len(self.available_items))
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
            Logger.debug("ShopModel.setPlayer", "Player set", player_name=player.getName() if player else "None")
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
            return self.available_items.copy()
        except Exception as e:
            Logger.error("ShopModel.getAvailableItems", e)
            return []
    


    def setAvailableItems(self, items):
       
        try:
            if isinstance(items, list):
                self.available_items = items.copy()  
                Logger.debug("ShopModel.setAvailableItems", "Available items set", count=len(self.available_items))
            else:
                Logger.error("ShopModel.setAvailableItems", ValueError("Items must be a list"))
        except Exception as e:
            Logger.error("ShopModel.setAvailableItems", e)
    

    def getSelectedIndex(self):
       
        try:
            return self.selected_index
        except Exception as e:
            Logger.error("ShopModel.getSelectedIndex", e)
            return 0
    
    def setSelectedIndex(self, index):
    
        try:
            if 0 <= index < len(self.available_items):
                self.selected_index = index
                Logger.debug("ShopModel.setSelectedIndex", "Selection changed", index=index)
        except Exception as e:
            Logger.error("ShopModel.setSelectedIndex", e)
    


    def getPurchaseMessage(self):
      
        try:
            return self.purchase_message
        except Exception as e:
            Logger.error("ShopModel.getPurchaseMessage", e)
            return ""
    


    def setPurchaseMessage(self, message):
        
        
        try:
            self.purchase_message = str(message) if message else ""
            Logger.debug("ShopModel.setPurchaseMessage", "Purchase message set", purchase_message=self.purchase_message)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseMessage", e)
    
    def isPurchaseSuccess(self):
        
        try:
            return self.purchase_success
        except Exception as e:
            Logger.error("ShopModel.isPurchaseSuccess", e)
            return False
    


    def setPurchaseSuccess(self, success):
      
        try:
            self.purchase_success = bool(success)
            Logger.debug("ShopModel.setPurchaseSuccess", "Purchase success set", success=self.purchase_success)
        except Exception as e:
            Logger.error("ShopModel.setPurchaseSuccess", e)
    
   
    
    def purchaseItem(self, item_index):
        
        try:
            if item_index < 0 or item_index >= len(self.available_items):
                self.setPurchaseMessage("Invalid item selection")
                self.setPurchaseSuccess(False)
                Logger.debug("ShopModel.purchaseItem", "Invalid item index", index=item_index)
                return False
            
            item = self.available_items[item_index]
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
                    hp_restore = item.get("hp_restore", 0)
                    
                
                
                    bottle = BottleModel(item["name"], alcohol_level, bonus_damage, accuracy_penalty)
                    
                   
                   
                    if hp_restore > 0:
                        current_hp = self.player.getHealth()
                        self.player.setHealth(min(100, current_hp + hp_restore))
                        self.setPurchaseMessage(f"Purchased {item['name']}! Restored {hp_restore} HP, bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", f"{item['name']} purchased", 
                                   new_hp=self.player.getHealth())
                    else:
                        self.setPurchaseMessage(f"Purchased {item['name']}! Bottle added to inventory.")
                        Logger.debug("ShopModel.purchaseItem", f"{item['name']} purchased")
                    
                  
                    if hasattr(self.player, 'inventory'):
                        self.player.inventory.add_item(bottle)
                    


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
                           item=item["name"], remaining_currency=self.player.getCurrency())
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
            max_page = (len(self.available_items) - 1) // self.items_per_page
            if self.current_page < max_page:
                self.current_page += 1
                self.selected_index = self.current_page * self.items_per_page
                Logger.debug("ShopModel.nextPage", "Page changed", page=self.current_page)
        except Exception as e:
            Logger.error("ShopModel.nextPage", e)

    def previousPage(self):

        try:
            if self.current_page > 0:
                self.current_page -= 1
                self.selected_index = self.current_page * self.items_per_page
                Logger.debug("ShopModel.previousPage", "Page changed", page=self.current_page)
        except Exception as e:
            Logger.error("ShopModel.previousPage", e)



    def getCurrentPage(self):
        return self.current_page

    def getPageCount(self):
        try:
            return (len(self.available_items) - 1) // self.items_per_page + 1
        except Exception as e:
            Logger.error("ShopModel.getPageCount", e)
            return 1



    def getItemsForCurrentPage(self):
        try:
            start_idx = self.current_page * self.items_per_page
            end_idx = start_idx + self.items_per_page
            return self.available_items[start_idx:end_idx]
        except Exception as e:
            Logger.error("ShopModel.getItemsForCurrentPage", e)
            return []

    def getItemIndexOnCurrentPage(self, page_index):
        try:
            return self.current_page * self.items_per_page + page_index
        except Exception as e:
            Logger.error("ShopModel.getItemIndexOnCurrentPage", e)
            return 0

