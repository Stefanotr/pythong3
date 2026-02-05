"""
FinTransitionPageView Module

Displays a transition screen after rhythm combat/end of stage.
Auto-transitions to the next stage after 5 seconds.
"""

import pygame
from Views.PageView import PageView
from Controllers.GameState import GameState
from Utils.Logger import Logger


class FinTransitionPageView(PageView):
    """
    Transition view shown at the end of a rhythm combat or stage.
    Displays a message and automatically transitions after 5 seconds.
    """
    
    def __init__(self, screen, message="Stage Complete!", next_stage_name="Next Stage", duration_seconds=5):
        """
        Initialize the transition view.
        
        Args:
            screen: Pygame display surface
            message: Main message to display
            next_stage_name: Name of the next stage for secondary message
            duration_seconds: How long to show the transition (default 5 seconds)
        """
        try:
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            
            # Initialize PageView without background
            super().__init__("Stage Transition", screen_width, screen_height, pygame.RESIZABLE, None)
            self.screen = screen
            self.message = message
            self.next_stage_name = next_stage_name
            self.duration_seconds = duration_seconds
            self.duration_frames = duration_seconds * 60  # 60 FPS
            self.elapsed_frames = 0
            
            Logger.debug("FinTransitionPageView.__init__", "Transition view created",
                        duration_seconds=duration_seconds, next_stage=next_stage_name)
        except Exception as e:
            Logger.error("FinTransitionPageView.__init__", e)
            raise
    
    def run(self):
        """
        Main loop for the transition view.
        Displays the transition screen and auto-returns after duration.
        
        Returns:
            str: Empty string or next state code
        """
        try:
            clock = pygame.time.Clock()
            running = True
            
            Logger.debug("FinTransitionPageView.run", "Transition loop started",
                        duration_seconds=self.duration_seconds)
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("FinTransitionPageView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.KEYDOWN:
                            # Skip with any key
                            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                                Logger.debug("FinTransitionPageView.run", "Transition skipped by key press")
                                return ""
                    
                    # === INCREMENT TIMER ===
                    self.elapsed_frames += 1
                    
                    # Log progress every 30 frames (0.5 seconds at 60 FPS)
                    if self.elapsed_frames % 30 == 0:
                        time_remaining = max(0, self.duration_seconds - (self.elapsed_frames / 60))
                        Logger.debug("FinTransitionPageView.run", "Transition progress",
                                    elapsed_frames=self.elapsed_frames, time_remaining=time_remaining)
                    
                    # Check if duration elapsed
                    if self.elapsed_frames >= self.duration_frames:
                        Logger.debug("FinTransitionPageView.run", "Transition duration elapsed",
                                    total_frames=self.elapsed_frames, duration_frames=self.duration_frames)
                        return ""
                    
                    # === RENDERING ===
                    try:
                        # Fill background with dark overlay
                        self.screen.fill((20, 20, 30))
                        
                        # Calculate progress (0 to 1)
                        progress = self.elapsed_frames / self.duration_frames
                        
                        # Log rendering start on first frame
                        if self.elapsed_frames == 1:
                            Logger.debug("FinTransitionPageView.run", "Starting render loop",
                                        screen_width=self.screen.get_width(), screen_height=self.screen.get_height())
                        
                        # Fade in/out effect: alpha increases then decreases
                        if progress < 0.5:
                            alpha = int(255 * (progress * 2))  # Fade in for first half
                        else:
                            alpha = int(255 * ((1 - progress) * 2))  # Fade out for second half
                        
                        # Draw main message
                        try:
                            font_main = pygame.font.SysFont('Arial', 60, bold=True)
                        except Exception:
                            font_main = pygame.font.Font(None, 60)
                        
                        text_main = font_main.render(self.message, True, (100, 255, 100))
                        # Create a surface with alpha for fade effect
                        text_main.set_alpha(alpha)
                        text_rect = text_main.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
                        self.screen.blit(text_main, text_rect)
                        
                        # Draw next stage info
                        try:
                            font_sub = pygame.font.SysFont('Arial', 32)
                        except Exception:
                            font_sub = pygame.font.Font(None, 32)
                        
                        text_sub = font_sub.render(f"Next: {self.next_stage_name}", True, (200, 200, 255))
                        text_sub.set_alpha(alpha)
                        sub_rect = text_sub.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
                        self.screen.blit(text_sub, sub_rect)
                        
                        # Draw skip hint (fade in/out)
                        try:
                            font_hint = pygame.font.SysFont('Arial', 18)
                        except Exception:
                            font_hint = pygame.font.Font(None, 18)
                        
                        time_remaining = max(0, self.duration_seconds - (self.elapsed_frames / 60))
                        text_hint = font_hint.render(f"Auto-transition in {time_remaining:.1f}s (Press SPACE to skip)", True, (150, 150, 150))
                        hint_rect = text_hint.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                        self.screen.blit(text_hint, hint_rect)
                        
                        pygame.display.flip()
                        
                        # Log every 60 frames (1 second at 60 FPS)
                        if self.elapsed_frames % 60 == 0:
                            Logger.debug("FinTransitionPageView.run", "Rendering frame",
                                        frame=self.elapsed_frames, progress=progress, alpha=alpha)
                    except Exception as e:
                        Logger.error("FinTransitionPageView.run", e)
                    
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("FinTransitionPageView.run", e)
                    continue
            
            return ""
        except Exception as e:
            Logger.error("FinTransitionPageView.run", e)
            return GameState.QUIT.value
