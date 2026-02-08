"""
InventoryView Module

Displays the inventory UI showing selected bottles and consumption options.
Used in rhythm combat for bottle selection and consumption.
"""

import pygame


class InventoryView:
    """
    View for displaying and managing inventory (bottles).
    Shows selected bottle with navigation arrows.
    """
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts (reduced by 20% for inventory)
        self.font = pygame.font.SysFont("Arial", int(screen_height * 0.015), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.022), bold=True)
    
    def draw_inventory_display(self, screen, inventory_model, x, y):
        """
        Draw the inventory display showing selected bottle.
        
        Args:
            screen: Pygame surface to draw on
            inventory_model: InventoryModel instance
            x: X position for display
            y: Y position for display
        """
        try:
            selected_bottle = inventory_model.get_selected_item()
            selected_index = inventory_model.get_selected_index()
            unique_bottles = inventory_model.get_unique_bottles()
            
            if not selected_bottle or len(unique_bottles) == 0:
                return
            
            # Get count of selected bottle type
            selected_unique = unique_bottles[selected_index] if 0 <= selected_index < len(unique_bottles) else None
            if not selected_unique:
                return
            
            bottle_count = selected_unique['count']
            
            # Display selected bottle info
            bottle_name = selected_bottle.getName()
            bottle_alcohol = selected_bottle.getAlcoholLevel()
            bottle_damage = selected_bottle.getBonusDamage()
            
            # Draw background box (reduced size)
            box_width = 200
            box_height = 100
            pygame.draw.rect(screen, (20, 20, 40), (x - box_width//2, y, box_width, box_height), border_radius=8)
            pygame.draw.rect(screen, (100, 100, 150), (x - box_width//2, y, box_width, box_height), 2, border_radius=8)
            
            # Title
            title_surf = self.big_font.render("INVENTORY", True, (200, 200, 255))
            screen.blit(title_surf, (x - title_surf.get_width()//2, y + 5))
            
            # Selected bottle name with count
            count_text = f"{bottle_name} x{bottle_count}"
            name_surf = self.big_font.render(count_text, True, (255, 215, 0))
            screen.blit(name_surf, (x - name_surf.get_width()//2, y + 25))
            
            # Stats (smaller)
            alcohol_txt = self.font.render(f"Alc: {bottle_alcohol}% | Dmg: +{bottle_damage}", True, (200, 200, 200))
            screen.blit(alcohol_txt, (x - alcohol_txt.get_width()//2, y + 48))
            
            # Navigation arrows (showing unique bottles count)
            nav_txt = self.font.render(f"<- {selected_index + 1}/{len(unique_bottles)} ->", True, (200, 200, 200))
            screen.blit(nav_txt, (x - nav_txt.get_width()//2, y + 67))
            
        except Exception as e:
            pass
    
    def draw_shop_inventory(self, screen, inventory_model, x, y):
        """
        Draw inventory summary for shop (showing bottle counts).
        
        Args:
            screen: Pygame surface to draw on
            inventory_model: InventoryModel instance
            x: X position (bottom right area)
            y: Y position
        """
        try:
            unique_bottles = inventory_model.get_unique_bottles()
            
            if not unique_bottles:
                return
            
            # Smaller font for inventory
            small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.018), bold=True)
            small_title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.022), bold=True)
            
            # Draw background
            box_width = 220
            box_height = 25 + (len(unique_bottles) * 22)
            
            # Shift left and up from bottom right
            adjusted_x = x - box_width - 50  # Decal vers la gauche
            adjusted_y = y - box_height - 80  # Remonter
            
            pygame.draw.rect(screen, (20, 20, 40), (adjusted_x, adjusted_y, box_width, box_height), border_radius=10)
            pygame.draw.rect(screen, (100, 100, 150), (adjusted_x, adjusted_y, box_width, box_height), 2, border_radius=10)
            
            # Title
            title_surf = small_title_font.render("INVENTORY", True, (200, 200, 255))
            screen.blit(title_surf, (adjusted_x + 10, adjusted_y + 3))
            
            # List each bottle type
            current_y = adjusted_y + 28
            for bottle_info in unique_bottles:
                bottle_name = bottle_info['name']
                count = bottle_info['count']
                
                text_surf = small_font.render(f"{bottle_name}: x{count}", True, (255, 215, 0))
                screen.blit(text_surf, (adjusted_x + 12, current_y))
                current_y += 22
        
        except Exception as e:
            pass
