"""
ShopPageView Module

Handles the visual representation of the shop page.
Displays shop interface for purchasing items (View-only, MVC pattern).
"""

import pygame
from Utils.Logger import Logger


# === SHOP PAGE VIEW CLASS ===

class ShopPageView:
    """
    View class for rendering the shop interface.
    Displays shop background, items, and UI elements (view-only, no logic).
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, shop_model):
        """
        Initialize the shop page view.
        
        Args:
            screen: Pygame surface to draw on
            shop_model: ShopModel instance containing shop state
        """
        try:
            self.screen = screen
            self.shop_model = shop_model
            self.screen_width = screen.get_width()
            self.screen_height = screen.get_height()
            
            Logger.debug("ShopPageView.__init__", "Shop page view initialized", 
                        width=self.screen_width, height=self.screen_height)
            
            # Load background image
            try:
                self.background = pygame.image.load('Game/Assets/Shop.png')
                # Scale to screen size
                self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
                Logger.debug("ShopPageView.__init__", "Background image loaded")
            except FileNotFoundError as e:
                Logger.error("ShopPageView.__init__", e)
                # Create default background if image not found
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill((50, 50, 50))
                Logger.debug("ShopPageView.__init__", "Using default background")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                raise
            
            # Font setup
            try:
                self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
                self.item_font = pygame.font.SysFont("Arial", 24)
                self.small_font = pygame.font.SysFont("Arial", 18)
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                self.title_font = pygame.font.Font(None, 48)
                self.item_font = pygame.font.Font(None, 24)
                self.small_font = pygame.font.Font(None, 18)
            
            # Message timer
            self.message_timer = 0
                
        except Exception as e:
            Logger.error("ShopPageView.__init__", e)
            raise

    # === RENDERING ===
    
    def draw(self):
        """
        Draw the shop interface to the screen.
        Renders background, items, currency, and UI elements.
        """
        try:
            # Draw background
            try:
                self.screen.blit(self.background, (0, 0))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw title
            try:
                title_text = "🛒 SHOP 🛒"
                title_surf = self.title_font.render(title_text, True, (255, 215, 0))  # Gold
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = 30
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw currency
            try:
                currency_text = f"💰 Currency: {self.shop_model.getPlayerCurrency()}"
                currency_surf = self.item_font.render(currency_text, True, (255, 255, 0))
                currency_x = 20
                currency_y = 100
                self.screen.blit(currency_surf, (currency_x, currency_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw items
            try:
                items = self.shop_model.getAvailableItems()
                selected_index = self.shop_model.getSelectedIndex()
                
                item_y_start = 150
                item_spacing = 80
                
                for i, item in enumerate(items):
                    item_y = item_y_start + i * item_spacing
                    
                    # Highlight selected item
                    if i == selected_index:
                        highlight_rect = pygame.Rect(50, item_y - 10, self.screen_width - 100, 70)
                        pygame.draw.rect(self.screen, (255, 215, 0, 100), highlight_rect, 3)
                    
                    # Item name
                    name_text = item["name"]
                    name_color = (255, 255, 255) if i == selected_index else (200, 200, 200)
                    name_surf = self.item_font.render(name_text, True, name_color)
                    self.screen.blit(name_surf, (70, item_y))
                    
                    # Price
                    price_text = f"${item['price']}"
                    price_color = (0, 255, 0) if self.shop_model.getPlayerCurrency() >= item['price'] else (255, 0, 0)
                    price_surf = self.item_font.render(price_text, True, price_color)
                    price_x = self.screen_width - price_surf.get_width() - 70
                    self.screen.blit(price_surf, (price_x, item_y))
                    
                    # Description
                    desc_text = item["description"]
                    desc_surf = self.small_font.render(desc_text, True, (180, 180, 180))
                    self.screen.blit(desc_surf, (70, item_y + 30))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw purchase message
            try:
                if self.shop_model.getPurchaseMessage():
                    message = self.shop_model.getPurchaseMessage()
                    message_color = (0, 255, 0) if self.shop_model.isPurchaseSuccess() else (255, 0, 0)
                    message_surf = self.item_font.render(message, True, message_color)
                    message_x = self.screen_width // 2 - message_surf.get_width() // 2
                    message_y = self.screen_height - 100
                    self.screen.blit(message_surf, (message_x, message_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw instructions
            try:
                instruction_text = "↑↓ Navigate | ENTER/SPACE Purchase | ESC/E Exit"
                instruction_surf = self.small_font.render(instruction_text, True, (150, 150, 150))
                instruction_x = self.screen_width // 2 - instruction_surf.get_width() // 2
                instruction_y = self.screen_height - 40
                self.screen.blit(instruction_surf, (instruction_x, instruction_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
                
        except Exception as e:
            Logger.error("ShopPageView.draw", e)
