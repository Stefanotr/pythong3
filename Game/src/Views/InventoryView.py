import pygame


class InventoryView:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.SysFont("Arial", int(screen_height * 0.015), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.022), bold=True)





    def draw_inventory_display(self, screen, inventory_model, x, y):


        try:
            selected_bottle = inventory_model.get_selected_item()
            selected_index = inventory_model.get_selected_index()
            unique_bottles = inventory_model.get_unique_bottles()

            if not selected_bottle or len(unique_bottles) == 0:
                return

            selected_unique = (
                unique_bottles[selected_index]
                if 0 <= selected_index < len(unique_bottles)
                else None
            )

            if not selected_unique:
                return

            bottle_count = selected_unique["count"]

            bottle_name = selected_bottle.getName()


            bottle_alcohol = selected_bottle.getAlcoholLevel()
            bottle_damage = selected_bottle.getBonusDamage()

            box_width = 200
            box_height = 100
            pygame.draw.rect(
                screen,

                (20, 20, 40),
                (x - box_width // 2, y, box_width, box_height),
                border_radius=8,
            )
            pygame.draw.rect(


                screen,
                (100, 100, 150),
                (x - box_width // 2, y, box_width, box_height),
                2,
                border_radius=8,
            )

            title_surf = self.big_font.render("INVENTORY", True, (200, 200, 255))
            screen.blit(title_surf, (x - title_surf.get_width() // 2, y + 5))

            count_text = f"{bottle_name} x{bottle_count}"
            name_surf = self.big_font.render(count_text, True, (255, 215, 0))
            screen.blit(name_surf, (x - name_surf.get_width() // 2, y + 25))


            alcohol_txt = self.font.render(
                f"Alc: {bottle_alcohol}% | Dmg: +{bottle_damage}",
                True,
                (200, 200, 200),
            )
            screen.blit(alcohol_txt, (x - alcohol_txt.get_width() // 2, y + 48))

            nav_txt = self.font.render(
                f"<- {selected_index + 1}/{len(unique_bottles)} ->",
                True,
                (200, 200, 200),
            )
            screen.blit(nav_txt, (x - nav_txt.get_width() // 2, y + 67))

        except Exception:
            pass




    def draw_shop_inventory(self, screen, inventory_model, x, y):
        try:
            unique_bottles = inventory_model.get_unique_bottles()

            if not unique_bottles:
                return

            small_font = pygame.font.SysFont(
                "Arial", int(self.screen_height * 0.018), bold=True
            )
            small_title_font = pygame.font.SysFont(
                "Arial", int(self.screen_height * 0.022), bold=True

            )

            box_width = 220
            box_height = 25 + (len(unique_bottles) * 22)

            adjusted_x = x - box_width - 50
            adjusted_y = y - box_height - 80

            pygame.draw.rect(
                screen,
                (20, 20, 40),
                (adjusted_x, adjusted_y, box_width, box_height),
                border_radius=10,
            )
            pygame.draw.rect(
                screen,
                (100, 100, 150),

                (adjusted_x, adjusted_y, box_width, box_height),
                2,
                border_radius=10,
            )

            title_surf = small_title_font.render(

                "INVENTORY", True, (200, 200, 255)
            )
            screen.blit(title_surf, (adjusted_x + 10, adjusted_y + 3))

            current_y = adjusted_y + 28


            for bottle_info in unique_bottles:
                bottle_name = bottle_info["name"]
                count = bottle_info["count"]

                text_surf = small_font.render(
                    f"{bottle_name}: x{count}", True, (255, 215, 0)
                )
                screen.blit(text_surf, (adjusted_x + 12, current_y))
                current_y += 22

        except Exception:
            pass
