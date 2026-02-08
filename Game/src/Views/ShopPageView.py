
        try:
            self.screen = screen
            self.shop_model = shop_model
            self.screen_width = screen.get_width()
            self.screen_height = screen.get_height()
            
            Logger.debug("ShopPageView.__init__", "Shop page view initialized", 
                        width=self.screen_width, height=self.screen_height)
            
            try:
                self.background = pygame.image.load('Game/Assets/Shop.png')
                self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
                Logger.debug("ShopPageView.__init__", "Background image loaded")
            except FileNotFoundError as e:
                Logger.error("ShopPageView.__init__", e)
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill((50, 50, 50))
                Logger.debug("ShopPageView.__init__", "Using default background")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                raise
            
            try:
                self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
                self.item_font = pygame.font.SysFont("Arial", 24)
                self.small_font = pygame.font.SysFont("Arial", 18)
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                self.title_font = pygame.font.Font(None, 48)
                self.item_font = pygame.font.Font(None, 24)
                self.small_font = pygame.font.Font(None, 18)
            
            try:
                self.inventory_view = InventoryView(self.screen_width, self.screen_height)
                Logger.debug("ShopPageView.__init__", "Inventory view initialized")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                self.inventory_view = None
            
            self.message_timer = 0
                
        except Exception as e:
            Logger.error("ShopPageView.__init__", e)
            raise

    
    def draw(self, player=None):
        try:
            try:
                self.screen.blit(self.background, (0, 0))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            try:
                title_text = "SHOP"
                title_surf = self.title_font.render(title_text, True, (255, 215, 0))
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = 30
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            try:
                currency_text = f"Currency: ${self.shop_model.getPlayerCurrency()}"
                currency_surf = self.item_font.render(currency_text, True, (255, 255, 0))
                currency_x = 20
                currency_y = 90
                self.screen.blit(currency_surf, (currency_x, currency_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            try:
                items = self.shop_model.getItemsForCurrentPage()
                selected_index = self.shop_model.getSelectedIndex()
                current_page = self.shop_model.getCurrentPage()
                page_count = self.shop_model.getPageCount()
                
                item_y_start = 140
                item_spacing = 55
                
                for i, item in enumerate(items):
                    item_y = item_y_start + i * item_spacing
                    
                    abs_index = self.shop_model.getItemIndexOnCurrentPage(i)
                    
                    if abs_index == selected_index:
                        highlight_rect = pygame.Rect(35, item_y - 8, self.screen_width - 70, 60)
                        pygame.draw.rect(self.screen, (255, 215, 0, 100), highlight_rect, 3)
                    
                    name_text = item["name"]
                    category_text = f"({item.get('category', 'Item')})"
                    name_color = (255, 255, 255) if abs_index == selected_index else (200, 200, 200)
                    name_surf = self.item_font.render(f"{name_text} {category_text}", True, name_color)
                    self.screen.blit(name_surf, (60, item_y))
                    
                    price_text = f"${item['price']}"
                    price_color = (0, 255, 0) if self.shop_model.getPlayerCurrency() >= item['price'] else (255, 100, 100)
                    price_surf = self.item_font.render(price_text, True, price_color)
                    price_x = self.screen_width - price_surf.get_width() - 50
                    self.screen.blit(price_surf, (price_x, item_y))
                    
                    desc_text = item["description"][:65]
                    desc_surf = self.small_font.render(desc_text, True, (150, 150, 150))
                    self.screen.blit(desc_surf, (60, item_y + 25))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
            try:
                current_page = self.shop_model.getCurrentPage()
                page_count = self.shop_model.getPageCount()
                
                button_y = self.screen_height - 140
                button_width = 130
                button_height = 40
                
                prev_x = self.screen_width // 2 - 180
                prev_rect = pygame.Rect(prev_x, button_y, button_width, button_height)
                prev_enabled = current_page > 0
                pygame.draw.rect(self.screen, (100, 150, 100) if prev_enabled else (60, 60, 60), prev_rect)
                pygame.draw.rect(self.screen, (200, 255, 200) if prev_enabled else (100, 100, 100), prev_rect, 2)
                prev_text = self.item_font.render("< Previous", True, (255, 255, 255))
                prev_text_x = prev_x + (button_width - prev_text.get_width()) // 2
                prev_text_y = button_y + (button_height - prev_text.get_height()) // 2
                self.screen.blit(prev_text, (prev_text_x, prev_text_y))
                self.prev_button_rect = prev_rect if prev_enabled else None
                
                next_x = self.screen_width // 2 + 50
                next_rect = pygame.Rect(next_x, button_y, button_width, button_height)
                next_enabled = current_page < page_count - 1
                pygame.draw.rect(self.screen, (100, 150, 100) if next_enabled else (60, 60, 60), next_rect)
                pygame.draw.rect(self.screen, (200, 255, 200) if next_enabled else (100, 100, 100), next_rect, 2)
                next_text = self.item_font.render("Next >", True, (255, 255, 255))
                next_text_x = next_x + (button_width - next_text.get_width()) // 2
                next_text_y = button_y + (button_height - next_text.get_height()) // 2
                self.screen.blit(next_text, (next_text_x, next_text_y))
                self.next_button_rect = next_rect if next_enabled else None
                
                page_text = f"Page {current_page + 1} / {page_count}"
                page_surf = self.small_font.render(page_text, True, (150, 150, 255))
                page_x = self.screen_width // 2 - page_surf.get_width() // 2
                page_y = button_y + button_height + 15
                self.screen.blit(page_surf, (page_x, page_y))
            except Exception as e:
                Logger.error("ShopPageView.draw - buttons", e)
            
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
            
            try:
                instruction_text = "UP/DOWN: Choose Item  |  LEFT/RIGHT: Change Page  |  ENTER: Buy  |  ESC: Exit"
                instruction_surf = self.small_font.render(instruction_text, True, (150, 150, 150))
                instruction_x = self.screen_width // 2 - instruction_surf.get_width() // 2
                instruction_y = self.screen_height - 55
                self.screen.blit(instruction_surf, (instruction_x, instruction_y))
            except Exception as e:
                Logger.error("ShopPageView.draw", e)
            
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
