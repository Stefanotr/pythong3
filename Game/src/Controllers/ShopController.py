
        try:
            self.shop_model = shop_model
            self.view = view
            Logger.debug("ShopController.__init__", "Shop controller initialized")
        except Exception as e:
            Logger.error("ShopController.__init__", e)
            raise
    

    def handle_input(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    if current_index > 0:
                        self.shop_model.setSelectedIndex(current_index - 1)
                        Logger.debug("ShopController.handle_input", "Selection moved up")
                    else:
                        self.shop_model.previousPage()
                        current_page = self.shop_model.getCurrentPage()
                        page_end = min((current_page + 1) * self.shop_model.items_per_page, len(items))
                        self.shop_model.setSelectedIndex(page_end - 1)
                        Logger.debug("ShopController.handle_input", "Wrapped to previous page")

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    current_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    if current_index < len(items) - 1:
                        self.shop_model.setSelectedIndex(current_index + 1)
                        Logger.debug("ShopController.handle_input", "Selection moved down")
                    else:
                        self.shop_model.nextPage()
                        current_page = self.shop_model.getCurrentPage()
                        page_start = current_page * self.shop_model.items_per_page
                        self.shop_model.setSelectedIndex(page_start)
                        Logger.debug("ShopController.handle_input", "Wrapped to next page")

                elif event.key == pygame.K_LEFT:
                    self.shop_model.previousPage()
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Previous page", 
                               page=self.shop_model.getCurrentPage())

                elif event.key == pygame.K_RIGHT:
                    self.shop_model.nextPage()
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Next page", 
                               page=self.shop_model.getCurrentPage())

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_index = self.shop_model.getSelectedIndex()
                    items = self.shop_model.getAvailableItems()
                    
                    if 0 <= selected_index < len(items):
                        self.shop_model.purchaseItem(selected_index)
                        Logger.debug("ShopController.handle_input", "Purchase attempted", 
                                   item_index=selected_index)

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    Logger.debug("ShopController.handle_input", "Exit shop requested")
                    return "exit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.view, 'prev_button_rect') and self.view.prev_button_rect and \
                   self.view.prev_button_rect.collidepoint(event.pos):
                    self.shop_model.previousPage()
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Previous button clicked")
                
                elif hasattr(self.view, 'next_button_rect') and self.view.next_button_rect and \
                     self.view.next_button_rect.collidepoint(event.pos):
                    self.shop_model.nextPage()
                    current_page = self.shop_model.getCurrentPage()
                    first_item_index = current_page * self.shop_model.items_per_page
                    self.shop_model.setSelectedIndex(first_item_index)
                    Logger.debug("ShopController.handle_input", "Next button clicked")

            return None
        except Exception as e:
            Logger.error("ShopController.handle_input", e)
            return None

    def handleInput(self, event):
        return self.handle_input(event)
    
    
    def update(self):
        try:
            pass
        except Exception as e:
            Logger.error("ShopController.update", e)

