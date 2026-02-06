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
        
        Navigation:
        - UP/DOWN: Navigate items in current page
        - LEFT/RIGHT: Navigate pages
        - ENTER/SPACE: Purchase selected item
        - ESCAPE/E: Exit shop
        """
        try:
            if event.type == pygame.KEYDOWN:
                # Navigation up within page
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    if current_index > 0:
                        self.shop_model.setSelectedIndex(current_index - 1)
                        Logger.debug("ShopController.handle_input", "Selection moved up")
                    else:
                        # At top, wrap to bottom or go to previous page
                        self.shop_model.previousPage()
                        current_page = self.shop_model.getCurrentPage()
                        page_end = min((current_page + 1) * self.shop_model.items_per_page, len(items))
                        self.shop_model.setSelectedIndex(page_end - 1)
                        Logger.debug("ShopController.handle_input", "Wrapped to previous page")

                # Navigation down within page
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    current_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    if current_index < len(items) - 1:
                        self.shop_model.setSelectedIndex(current_index + 1)
                        Logger.debug("ShopController.handle_input", "Selection moved down")
                    else:
                        # At bottom, wrap to top or go to next page
                        self.shop_model.nextPage()
                        current_page = self.shop_model.getCurrentPage()
                        page_start = current_page * self.shop_model.items_per_page
                        self.shop_model.setSelectedIndex(page_start)
                        Logger.debug("ShopController.handle_input", "Wrapped to next page")

                # Page navigation (LEFT/RIGHT arrows)
                elif event.key == pygame.K_LEFT:
                    self.shop_model.previousPage()
                    # Auto-select first item on new page
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Previous page", 
                               page=self.shop_model.getCurrentPage())

                elif event.key == pygame.K_RIGHT:
                    self.shop_model.nextPage()
                    # Auto-select first item on new page
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Next page", 
                               page=self.shop_model.getCurrentPage())

                # Purchase
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    
                    # Verify selection is valid
                    if 0 <= selected_index < len(items):
                        self.shop_model.purchaseItem(selected_index)
                        Logger.debug("ShopController.handle_input", "Purchase attempted", 
                                   item_index=selected_index)

                # Exit shop
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    Logger.debug("ShopController.handle_input", "Exit shop requested")
                    return "exit"

            # Handle mouse clicks on Previous/Next buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.view, 'prev_button_rect') and self.view.prev_button_rect and \
                   self.view.prev_button_rect.collidepoint(event.pos):
                    self.shop_model.previousPage()
                    # Auto-select first item on new page
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Previous button clicked")
                
                elif hasattr(self.view, 'next_button_rect') and self.view.next_button_rect and \
                     self.view.next_button_rect.collidepoint(event.pos):
                    self.shop_model.nextPage()
                    # Auto-select first item on new page
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
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

