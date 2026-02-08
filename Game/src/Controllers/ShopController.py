import pygame
from Utils.Logger import Logger
from Controllers import BaseController


class ShopController(BaseController):

    def __init__(self, shopModel, view):
        try:
            self.shopModel = shopModel
            self.view = view
            Logger.debug("ShopController.__init__", "Shop controller initialized")
        except Exception as e:
            Logger.error("ShopController.__init__", e)
            raise

    def handleInput(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    currentIndex = self.shopModel.getSelectedIndex()
                    items = self.shopModel.getAvailableItems()
                    if currentIndex > 0:
                        self.shopModel.setSelectedIndex(currentIndex - 1)
                        Logger.debug("ShopController.handleInput", "Selection moved up")
                    else:
                        self.shopModel.previousPage()
                        currentPage = self.shopModel.getCurrentPage()
                        pageEnd = min((currentPage + 1) * self.shopModel.itemsPerPage, len(items))
                        self.shopModel.setSelectedIndex(pageEnd - 1)
                        Logger.debug("ShopController.handleInput", "Wrapped to previous page")

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    currentIndex = self.shopModel.getSelectedIndex()
                    items = self.shopModel.getAvailableItems()
                    if currentIndex < len(items) - 1:
                        self.shopModel.setSelectedIndex(currentIndex + 1)
                        Logger.debug("ShopController.handleInput", "Selection moved down")
                    else:
                        self.shopModel.nextPage()
                        currentPage = self.shopModel.getCurrentPage()
                        pageStart = currentPage * self.shopModel.itemsPerPage
                        self.shopModel.setSelectedIndex(pageStart)
                        Logger.debug("ShopController.handleInput", "Wrapped to next page")

                elif event.key == pygame.K_LEFT:
                    self.shopModel.previousPage()
                    currentPage = self.shopModel.getCurrentPage()
                    firstItemIndex = currentPage * self.shopModel.itemsPerPage
                    self.shopModel.setSelectedIndex(firstItemIndex)
                    Logger.debug("ShopController.handleInput", "Previous page",
                               page=self.shopModel.getCurrentPage())

                elif event.key == pygame.K_RIGHT:
                    self.shopModel.nextPage()
                    currentPage = self.shopModel.getCurrentPage()
                    firstItemIndex = currentPage * self.shopModel.itemsPerPage
                    self.shopModel.setSelectedIndex(firstItemIndex)
                    Logger.debug("ShopController.handleInput", "Next page",
                               page=self.shopModel.getCurrentPage())

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selectedIndex = self.shopModel.getSelectedIndex()
                    items = self.shopModel.getAvailableItems()

                    if 0 <= selectedIndex < len(items):
                        self.shopModel.purchaseItem(selectedIndex)
                        Logger.debug("ShopController.handleInput", "Purchase attempted",
                                   itemIndex=selectedIndex)

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    Logger.debug("ShopController.handleInput", "Exit shop requested")
                    return "exit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.view, 'prevButtonRect') and self.view.prevButtonRect and \
                   self.view.prevButtonRect.collidepoint(event.pos):
                    self.shopModel.previousPage()
                    currentPage = self.shopModel.getCurrentPage()
                    firstItemIndex = currentPage * self.shopModel.itemsPerPage
                    self.shopModel.setSelectedIndex(firstItemIndex)
                    Logger.debug("ShopController.handleInput", "Previous button clicked")

                elif hasattr(self.view, 'nextButtonRect') and self.view.nextButtonRect and \
                     self.view.nextButtonRect.collidepoint(event.pos):
                    self.shopModel.nextPage()
                    currentPage = self.shopModel.getCurrentPage()
                    firstItemIndex = currentPage * self.shopModel.itemsPerPage
                    self.shopModel.setSelectedIndex(firstItemIndex)
                    Logger.debug("ShopController.handleInput", "Next button clicked")

            return None
        except Exception as e:
            Logger.error("ShopController.handleInput", e)
            return None

    def update(self):
        try:
            pass
        except Exception as e:
            Logger.error("ShopController.update", e)

