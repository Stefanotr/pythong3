"""
ShopPageView Module

Handles the visual representation of the shop page.
Displays shop interface for purchasing items (View-only, MVC pattern).
"""

import pygame
from Utils.Logger import Logger
from Views.InventoryView import InventoryView


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
            
            # Inventory view for displaying owned bottles
            try:
                self.inventory_view = InventoryView(self.screen_width, self.screen_height)
                Logger.debug("ShopPageView.__init__", "Inventory view initialized")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                self.inventory_view = None
            
            # Message timer
            self.message_timer = 0
                
        except Exception as e:
            Logger.error("ShopPageView.__init__", e)
            raise

    # === RENDERING ===
    
    def draw(self, player=None):
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
                title_text = "SHOP"
                title_surf = self.title_font.render(title_text, True, (255, 215, 0))  # Gold
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = 30
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw currency
            try:
                currency_text = f"Currency: {self.shop_model.getPlayerCurrency()}"
                currency_surf = self.item_font.render(currency_text, True, (255, 255, 0))
                currency_x = 20
                currency_y = 100
                self.screen.blit(currency_surf, (currency_x, currency_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # Draw items
            try:
                items = self.shop_model.getItemsForCurrentPage()
                selected_index = self.shop_model.getSelectedIndex()
                current_page = self.shop_model.getCurrentPage()
                page_count = self.shop_model.getPageCount()
                
                item_y_start = 150
                item_spacing = 80
                
                for i, item in enumerate(items):
                    item_y = item_y_start + i * item_spacing
                    
                    # Highlight selected item
                    abs_index = self.shop_model.getItemIndexOnCurrentPage(i)
                    if abs_index == selected_index:
                        highlight_rect = pygame.Rect(50, item_y - 10, self.screen_width - 100, 70)
                        pygame.draw.rect(self.screen, (255, 215, 0, 100), highlight_rect, 3)
                    
                    # Item name
                    name_text = item["name"]
                    name_color = (255, 255, 255) if abs_index == selected_index else (200, 200, 200)
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
            
            # Draw pagination info
            try:
                current_page = self.shop_model.getCurrentPage()
                page_count = self.shop_model.getPageCount()
                page_text = f"Page {current_page + 1} / {page_count}"
                page_surf = self.small_font.render(page_text, True, (150, 150, 255))
                page_x = self.screen_width // 2 - page_surf.get_width() // 2
                page_y = self.screen_height - 200
                self.screen.blit(page_surf, (page_x, page_y))
            except Exception as e:
                Logger.error("ShopPageView.draw - pagination", e)
            
            # Draw navigation buttons
            try:
                current_page = self.shop_model.getCurrentPage()
                page_count = self.shop_model.getPageCount()
                
                button_y = self.screen_height - 150
                button_width = 150
                button_height = 40
                
                # Previous button
                prev_x = self.screen_width // 2 - 200
                prev_rect = pygame.Rect(prev_x, button_y, button_width, button_height)
                pygame.draw.rect(self.screen, (100, 100, 150) if current_page > 0 else (50, 50, 70), prev_rect)
                pygame.draw.rect(self.screen, (200, 200, 255), prev_rect, 2)
                prev_text = self.item_font.render("< Previous", True, (255, 255, 255))
                prev_text_x = prev_x + (button_width - prev_text.get_width()) // 2
                prev_text_y = button_y + (button_height - prev_text.get_height()) // 2
                self.screen.blit(prev_text, (prev_text_x, prev_text_y))
                
                # Next button
                next_x = self.screen_width // 2 + 50
                next_rect = pygame.Rect(next_x, button_y, button_width, button_height)
                pygame.draw.rect(self.screen, (100, 100, 150) if current_page < page_count - 1 else (50, 50, 70), next_rect)
                pygame.draw.rect(self.screen, (200, 200, 255), next_rect, 2)
                next_text = self.item_font.render("Next >", True, (255, 255, 255))
                next_text_x = next_x + (button_width - next_text.get_width()) // 2
                next_text_y = button_y + (button_height - next_text.get_height()) // 2
                self.screen.blit(next_text, (next_text_x, next_text_y))
                
                # Store button rects for click detection
                self.prev_button_rect = prev_rect
                self.next_button_rect = next_rect
            except Exception as e:
                Logger.error("ShopPageView.draw - buttons", e)
            
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
                instruction_text = "↑↓ Navigate | ← → Pages | ENTER/SPACE Purchase | ESC/E Exit"
                instruction_surf = self.small_font.render(instruction_text, True, (150, 150, 150))
                instruction_x = self.screen_width // 2 - instruction_surf.get_width() // 2
                instruction_y = self.screen_height - 40
                self.screen.blit(instruction_surf, (instruction_x, instruction_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            # --- DISPLAY PLAYER INVENTORY (Bottom Right) ---
            try:
                if player and hasattr(player, 'inventory') and self.inventory_view:
                    self.inventory_view.draw_shop_inventory(
                        self.screen,
                        player.inventory,
                        self.screen_width - 20,
                        self.screen_height - 20
                    )
            except Exception as e:
                Logger.error("ShopPageView.draw - inventory display", e)
                
        except Exception as e:
            Logger.error("ShopPageView.draw", e)
