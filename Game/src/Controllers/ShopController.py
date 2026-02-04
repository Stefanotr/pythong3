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
            if event.type != pygame.KEYDOWN:
                return None

            # Navigation
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                current_index = self.shop_model.getSelectedIndex()
                new_index = (current_index - 1) % len(self.shop_model.getAvailableItems())
                self.shop_model.setSelectedIndex(new_index)
                Logger.debug("ShopController.handle_input", "Selection moved up", index=new_index)

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                current_index = self.shop_model.getSelectedIndex()
                new_index = (current_index + 1) % len(self.shop_model.getAvailableItems())
                self.shop_model.setSelectedIndex(new_index)
                Logger.debug("ShopController.handle_input", "Selection moved down", index=new_index)

            # Purchase
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_index = self.shop_model.getSelectedIndex()
                self.shop_model.purchaseItem(selected_index)
                Logger.debug("ShopController.handle_input", "Purchase attempted", index=selected_index)

            # Exit shop
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                Logger.debug("ShopController.handle_input", "Exit shop requested")
                return "exit"

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

