"""
ShopController Module

Handles shop input, navigation, and purchase actions.
Manages interaction between ShopModel and ShopPageView.
"""

import pygame
from Utils.Logger import Logger
from Controllers import BaseController


# === SHOP CONTROLLER CLASS ===

class ShopController(BaseController):
    """
    Controller for managing shop interactions.
    Handles input processing, item selection, and purchase actions.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, shop_model, view):
        """
        Initialize the shop controller.
        
        Args:
            shop_model: ShopModel instance containing shop state
            view: ShopPageView instance for rendering
        """
        try:
            self.shop_model = shop_model
            self.view = view
            Logger.debug("ShopController.__init__", "Shop controller initialized")
        except Exception as e:
            Logger.error("ShopController.__init__", e)
            raise
    
    # === INPUT HANDLING ===

    def handle_input(self, event):
        """
        Handle input events for the shop.
        
        Args:
            event: Pygame event to process
        """
        try:
            if event.type == pygame.KEYDOWN:
                # Navigation up/down within page
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_index = self.shop_model.getSelectedIndex()
                    current_page = self.shop_model.getCurrentPage()
                    page_start = current_page * self.shop_model.items_per_page
                    page_end = page_start + self.shop_model.items_per_page
                    
                    if current_index > page_start:
                        # Move up within the same page
                        self.shop_model.setSelectedIndex(current_index - 1)
                    else:
                        # At top of page, go to previous page
                        self.shop_model.previousPage()
                        new_index = self.shop_model.getCurrentPage() * self.shop_model.items_per_page + self.shop_model.items_per_page - 1
                        if new_index < len(self.shop_model.getAvailableItems()):
                            self.shop_model.setSelectedIndex(new_index)
                    Logger.debug("ShopController.handle_input", "Selection moved up")

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    current_index = self.shop_model.getSelectedIndex()
                    current_page = self.shop_model.getCurrentPage()
                    page_start = current_page * self.shop_model.items_per_page
                    page_end = min(page_start + self.shop_model.items_per_page, len(self.shop_model.getAvailableItems()))
                    
                    if current_index < page_end - 1:
                        # Move down within the same page
                        self.shop_model.setSelectedIndex(current_index + 1)
                    else:
                        # At bottom of page, go to next page
                        self.shop_model.nextPage()
                        new_index = self.shop_model.getCurrentPage() * self.shop_model.items_per_page
                        self.shop_model.setSelectedIndex(new_index)
                    Logger.debug("ShopController.handle_input", "Selection moved down")

                # Page navigation
                elif event.key == pygame.K_LEFT:
                    self.shop_model.previousPage()
                    Logger.debug("ShopController.handle_input", "Previous page")

                elif event.key == pygame.K_RIGHT:
                    self.shop_model.nextPage()
                    Logger.debug("ShopController.handle_input", "Next page")

                # Purchase
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_index = self.shop_model.getSelectedIndex()
                    self.shop_model.purchaseItem(selected_index)
                    Logger.debug("ShopController.handle_input", "Purchase attempted", index=selected_index)

                # Exit shop
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    Logger.debug("ShopController.handle_input", "Exit shop requested")
                    return "exit"

            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.view, 'prev_button_rect') and self.view.prev_button_rect.collidepoint(event.pos):
                    self.shop_model.previousPage()
                    Logger.debug("ShopController.handle_input", "Previous button clicked")
                
                elif hasattr(self.view, 'next_button_rect') and self.view.next_button_rect.collidepoint(event.pos):
                    self.shop_model.nextPage()
                    Logger.debug("ShopController.handle_input", "Next button clicked")

            return None
        except Exception as e:
            Logger.error("ShopController.handle_input", e)
            return None

    # Backwards compatible alias
    def handleInput(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handle_input(event)
    
    # === UPDATE ===
    
    def update(self):
        """
        Update shop controller state.
        Called each frame to update shop logic.
        """
        try:
            # Reset purchase message after a delay (handled in view)
            pass
        except Exception as e:
            Logger.error("ShopController.update", e)

