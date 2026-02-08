

import pygame
from Utils.Logger import Logger
from Controllers import BaseController

class PlayerController(BaseController):

    
    def __init__(self, screen, player, collision_rects=None):

        try:
            self.player = player
            self.collision_rects = collision_rects if collision_rects is not None else []

            screen_width, screen_height = screen.get_size()
            self.SCREEN_SIZE = max(screen_width, screen_height)
            self.PLAYER_SIZE = 50
            self.SPEED = 6
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("PlayerController.__init__", "Player controller initialized", player_name=player.getName(), collisions=len(self.collision_rects))
        except Exception as e:
            Logger.error("PlayerController.__init__", e)
            raise

    def handle_input(self, event):

        try:
            if event.type != pygame.KEYDOWN:
                return

            if event.key == pygame.K_b:
                try:
                    selected_bottle = self.player.getSelectedBottle()
                    if selected_bottle:
                        self.player.drink(selected_bottle)
                        Logger.debug(
                            "PlayerController.handle_input",
                            "Player drank",
                            bottle=selected_bottle.getName(),
                            drunkenness=self.player.getDrunkenness(),
                        )
                    else:
                        Logger.debug("PlayerController.handle_input", "No bottle selected")
                except Exception as e:
                    Logger.error("PlayerController.handle_input", e)
        except Exception as e:
            Logger.error("PlayerController.handle_input", e)

    def handleInput(self, event):

        return self.handle_input(event)

    def handle_events(self, events):

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
                    Logger.error("PlayerController.handle_events", e)
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
                Logger.error("PlayerController.handle_events", e)

            try:
                current_x = self.player.getX()
                current_y = self.player.getY()
            except Exception as e:
                Logger.error("PlayerController.handle_events", e)
                return

            new_x = current_x + dx
            new_y = current_y + dy

            if new_x < 0:
                new_x = 0
            if new_y < 0:
                new_y = 0

            half = self.PLAYER_SIZE // 2

            resolved_x = current_x
            resolved_y = current_y

            try:
                rect_x = pygame.Rect(new_x - half, current_y - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collided_x = any(rect_x.colliderect(r) for r in self.collision_rects)
                if not collided_x:
                    resolved_x = new_x
                else:
                    Logger.debug("PlayerController.handle_events", "Collision on X axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_x", e)

            try:
                rect_y = pygame.Rect(resolved_x - half, new_y - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collided_y = any(rect_y.colliderect(r) for r in self.collision_rects)
                if not collided_y:
                    resolved_y = new_y
                else:
                    Logger.debug("PlayerController.handle_events", "Collision on Y axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_y", e)

            try:
                self.player.setX(resolved_x)
                self.player.setY(resolved_y)
                Logger.debug(
                    "PlayerController.handle_events",
                    "Player moved",
                    x=self.player.getX(),
                    y=self.player.getY(),
                )
            except Exception as e:
                Logger.error("PlayerController.handle_events", e)
        except Exception as e:
            Logger.error("PlayerController.handle_events", e)