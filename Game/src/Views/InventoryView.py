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
        self.font = pygame.font.SysFont("Arial", int(screen_height * 0.02), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.032), bold=True)
    
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
            total_items = len(inventory_model.get_all_items())
            
            if not selected_bottle or total_items == 0:
                return
            
            # Display selected bottle info
            bottle_name = selected_bottle.getName()
            bottle_alcohol = selected_bottle.getAlcoholLevel()
            bottle_damage = selected_bottle.getBonusDamage()
            
            # Draw background box
            box_width = 300
            box_height = 150
            pygame.draw.rect(screen, (20, 20, 40), (x - box_width//2, y, box_width, box_height), border_radius=10)
            pygame.draw.rect(screen, (100, 100, 150), (x - box_width//2, y, box_width, box_height), 2, border_radius=10)
            
            # Title
            title_surf = self.big_font.render("INVENTORY", True, (200, 200, 255))
            screen.blit(title_surf, (x - title_surf.get_width()//2, y + 10))
            
            # Selected bottle name
            name_surf = self.big_font.render(bottle_name, True, (255, 215, 0))
            screen.blit(name_surf, (x - name_surf.get_width()//2, y + 40))
            
            # Stats
            alcohol_txt = self.font.render(f"Alcohol: {bottle_alcohol}%", True, (255, 100, 100))
            screen.blit(alcohol_txt, (x - alcohol_txt.get_width()//2, y + 75))
            
            damage_txt = self.font.render(f"Damage Bonus: +{bottle_damage}", True, (100, 255, 100))
            screen.blit(damage_txt, (x - damage_txt.get_width()//2, y + 100))
            
            # Navigation arrows
            nav_txt = self.font.render(f"<- {selected_index + 1}/{total_items} ->", True, (255, 255, 255))
            screen.blit(nav_txt, (x - nav_txt.get_width()//2, y + 125))
            
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
