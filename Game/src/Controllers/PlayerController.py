import pygame
from Utils.Logger import Logger
from Controllers import BaseController


class PlayerController(BaseController):

    def __init__(self, screen, player, collisionRects=None):
        try:
            self.player = player
            self.collisionRects = collisionRects if collisionRects is not None else []

            screenWidth, screenHeight = screen.get_size()
            self.SCREEN_SIZE = max(screenWidth, screenHeight)
            self.PLAYER_SIZE = 50
            self.SPEED = 6
            self.screenWidth = screenWidth
            self.screenHeight = screenHeight
            Logger.debug("PlayerController.__init__", "Player controller initialized", playerName=player.getName(), collisions=len(self.collisionRects))
        except Exception as e:
            Logger.error("PlayerController.__init__", e)
            raise


    def handleInput(self, event):
        try:
            if event.type != pygame.KEYDOWN:
                return

            if event.key == pygame.K_b:
                try:
                    selected_bottle = self.player.getSelectedBottle()
                    if selected_bottle:
                        self.player.drink(selected_bottle)
                        Logger.debug(
                            "PlayerController.handleInput",
                            "Player drank",
                            bottle=selected_bottle.getName(),
                            drunkenness=self.player.getDrunkenness(),
                        )
                    else:
                        Logger.debug("PlayerController.handleInput", "No bottle selected")
                except Exception as e:
                    Logger.error("PlayerController.handleInput", e)
        except Exception as e:
            Logger.error("PlayerController.handleInput", e)


    def handleEvents(self, events):
        try:
            keys = pygame.key.get_pressed()

            dx = 0
            dy = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                dx -= self.SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += self.SPEED
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                dy -= self.SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += self.SPEED

            if dx == 0 and dy == 0:
                try:
                    self.player.setCurrentAction("idle")
                except Exception as e:
                    Logger.error("PlayerController.handleEvents", e)
                return
            
            try:
                if dx < 0:
                    self.player.setCurrentAction("moving_left", duration=10)
                elif dx > 0:
                    self.player.setCurrentAction("moving_right", duration=10)
                else:
                    action = self.player.getCurrentAction()
                    if action not in ["moving_left", "moving_right"]:
                        self.player.setCurrentAction("moving_right", duration=10)
            except Exception as e:
                Logger.error("PlayerController.handleEvents", e)

            try:
                currentX = self.player.getX()
                currentY = self.player.getY()
            except Exception as e:
                Logger.error("PlayerController.handleEvents", e)
                return

            newX = currentX + dx
            newY = currentY + dy

            if newX < 0:
                newX = 0
            if newY < 0:
                newY = 0

            half = self.PLAYER_SIZE // 2

            resolvedX = currentX
            resolvedY = currentY

            try:
                rectX = pygame.Rect(newX - half, currentY - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collidedX = any(rectX.colliderect(r) for r in self.collision_rects)
                if not collidedX:
                    resolvedX = newX
                else:
                    Logger.debug("PlayerController.handleEvents", "Collision on X axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_x", e)

            try:
                rectY = pygame.Rect(resolvedX - half, newY - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collidedY = any(rectY.colliderect(r) for r in self.collision_rects)
                if not collidedY:
                    resolvedY = newY
                else:
                    Logger.debug("PlayerController.handleEvents", "Collision on Y axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_y", e)

            try:
                self.player.setX(resolvedX)
                self.player.setY(resolvedY)
                Logger.debug(
                    "PlayerController.handleEvents",
                    "Player moved",
                    x=self.player.getX(),
                    y=self.player.getY(),
                )
            except Exception as e:
                Logger.error("PlayerController.handleEvents", e)
        except Exception as e:
            Logger.error("PlayerController.handleEvents", e)