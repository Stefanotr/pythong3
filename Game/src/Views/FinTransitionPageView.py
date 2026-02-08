import pygame
from Views.PageView import PageView
from Controllers.GameState import GameState
from Utils.Logger import Logger

class FinTransitionPageView(PageView):

    def __init__(self, screen, message="Stage Complete!", next_stage_name ="Next Stage", duration_seconds =5):

        try:
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            
            super().__init__("Stage Transition", screen_width, screen_height, pygame.RESIZABLE, None)
            self.screen = screen
            self.message = message
            self.next_stage_name = next_stage_name
            self.duration_seconds = duration_seconds
            self.duration_frames = duration_seconds * 60  
            self.elapsed_frames = 0
            
            Logger.debug("FinTransitionPageView.__init__", "Transition view created",
                        durationSeconds =duration_seconds, nextStage =next_stage_name)
        except Exception as e:
            Logger.error("FinTransitionPageView.__init__", e)
            raise
    
    def run(self):

        try:
            clock = pygame.time.Clock()
            running = True
            
            Logger.debug("FinTransitionPageView.run", "Transition loop started",
                        duration_seconds =self.duration_seconds)
            
            while running:
                try:
                    
                    try:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                Logger.debug("FinTransitionPageView.run", "QUIT event received")
                                return GameState.QUIT.value
                            
                            elif event.type == pygame.KEYDOWN:
                                
                                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                                    Logger.debug("FinTransitionPageView.run", "Transition skipped by key press", key=pygame.key.name(event.key))
                                    return ""
                    except Exception as e:
                        Logger.error("FinTransitionPageView.run - Event handling", e)
                        
                        pass
                    
                    self.elapsedFrames += 1
                    
                    if self.elapsed_frames % 30 == 0:
                        time_remaining = max(0, self.duration_seconds - (self.elapsed_frames / 60))
                        Logger.debug("FinTransitionPageView.run", "Transition progress",
                                    elapsed_frames =self.elapsed_frames, time_remaining =time_remaining)
                    
                    if self.elapsed_frames >= self.duration_frames:
                        Logger.debug("FinTransitionPageView.run", "Transition duration elapsed",
                                    total_frames =self.elapsed_frames, duration_frames =self.duration_frames)
                        return ""
                    
                    try:
                        
                        if self.screen and pygame.display.get_surface():
                            self.screen.fill((20, 20, 30))
                            
                            progress = self.elapsed_frames / self.duration_frames
                            
                            if self.elapsed_frames == 1:
                                Logger.debug("FinTransitionPageView.run", "Starting render loop",
                                            screen_width =self.screen.get_width(), screen_height =self.screen.get_height())
                            
                            if progress < 0.5:
                                alpha = int(255 * (progress * 2))  
                            else:
                                alpha = int(255 * ((1 - progress) * 2))  
                            
                            try:
                                font_main = pygame.font.SysFont('Arial', 60, bold=True)
                            except Exception:
                                font_main = pygame.font.Font(None, 60)
                            
                            text_main = font_main.render(self.message, True, (100, 255, 100))
                            
                            text_main.set_alpha(alpha)
                            text_rect = text_main.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
                            self.screen.blit(text_main, text_rect)
                            
                            try:
                                font_sub = pygame.font.SysFont('Arial', 32)
                            except Exception:
                                font_sub = pygame.font.Font(None, 32)
                            
                            text_sub = font_sub.render(f"Next: {self.next_stage_name}", True, (200, 200, 255))
                            text_sub.set_alpha(alpha)
                            sub_rect = text_sub.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
                            self.screen.blit(text_sub, sub_rect)
                            
                            try:
                                font_hint = pygame.font.SysFont('Arial', 18)
                            except Exception:
                                font_hint = pygame.font.Font(None, 18)
                            
                            timeRemaining = max(0, self.duration_seconds - (self.elapsed_frames / 60))
                            text_hint = font_hint.render(f"Auto-transition in {timeRemaining:.1f}s (Press SPACE to skip)", True, (150, 150, 150))
                            hint_rect = text_hint.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                            self.screen.blit(text_hint, hint_rect)
                            
                            pygame.display.flip()
                            
                            if self.elapsed_frames % 60 == 0:
                                Logger.debug("FinTransitionPageView.run", "Rendering frame",
                                            frame=self.elapsed_frames, progress=progress, alpha=alpha)
                    except Exception as e:
                        Logger.error("FinTransitionPageView.run - Rendering", e)
                        
                        pass
                    
                    try:
                        clock.tick(60)
                    except Exception as e:
                        Logger.error("FinTransitionPageView.run - Clock tick", e)
                    
                except Exception as e:
                    Logger.error("FinTransitionPageView.run - Inner loop", e)
                    
                    continue
            
            return ""
        except Exception as e:
            Logger.error("FinTransitionPageView.run", e)
            
            return ""
