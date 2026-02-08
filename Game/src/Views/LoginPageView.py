import pygame
import sys
from Utils.Logger import Logger
from Utils.AssetManager import AssetManager
from Models.LoginModel import LoginModel
from Views.PageView import PageView
from Views.ButtonView import ButtonView
from Controllers.ButtonController import ButtonController


class LoginPageView(PageView):
    
    def __init__(self, name="Login", width=800, height=800, RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        try:
            super().__init__(name, width, height, pygame.FULLSCREEN, background_image)
            
            self.login_model = LoginModel()
            
            self.mode = "login"
            self.username_input = ""
            self.password_input = ""


            self.password_confirm_input = ""
            self.active_input = "username"
            self.show_password = False
            self.login_successful = False
            self.successful_user = None
            self.successful_progression = None
            
            input_width = 300
            input_x = (self.width - input_width) // 2
            self.input_fields = {
                "username": {"rect": pygame.Rect(input_x, 360, input_width, 40), "label": "Nom d'utilisateur"},
                "password": {"rect": pygame.Rect(input_x, 440, input_width, 40), "label": "Mot de passe"},
                "password_confirm": {"rect": pygame.Rect(input_x, 520, input_width, 40), "label": "Confirmer mot de passe"}
            }
            
            self.buttons = {}
            self.setup_buttons()
            
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
            
            self.color_text = (255, 255, 255)
            self.color_input_bg = (40, 40, 40)
            self.color_input_border = (100, 100, 100)
            self.color_input_active = (150, 150, 255)
            self.color_error = (255, 100, 100)
            self.color_success = (100, 255, 100)
            
            self.error_message = ""
            self.error_timer = 0
            

            self.clock = pygame.time.Clock()
            self.fps = 60
            
            Logger.debug("LoginPageView.__init__", "Login page view initialized")
        except Exception as e:
            Logger.error("LoginPageView.__init__", e)
            raise
    





    def setup_buttons(self):
        try:
            btn_width = 140
            btn_height = 50


            btn_gap = 30
            total_width = btn_width * 2 + btn_gap
            
            btn_x1 = (self.width - total_width) // 2
            btn_x2 = btn_x1 + btn_width + btn_gap
            btn_y = 610
            
            quit_x = self.width // 2
            quit_y = 700
            
            self.buttons["login_btn"] = {
                "rect": pygame.Rect(btn_x1, btn_y, btn_width, btn_height),
                "label": "Connexion",
                "action": self.handle_login
            }
            


            self.buttons["register_toggle_btn"] = {
                "rect": pygame.Rect(btn_x2, btn_y, btn_width, btn_height),
                "label": "S'inscrire",
                "action": self.switch_to_register
            }
            
            self.buttons["register_btn"] = {
                "rect": pygame.Rect(btn_x1, btn_y, btn_width, btn_height),
                "label": "S'inscrire",
                "action": self.handle_register
            }
            
            self.buttons["login_toggle_btn"] = {
                "rect": pygame.Rect(btn_x2, btn_y, btn_width, btn_height),
                "label": "Connexion",
                "action": self.switch_to_login
            }
            
            try:
                self.quit_button_view = ButtonView(
                    image_path='Game/Assets/buttonQuit.png',


                    position=(quit_x, quit_y),
                    size=(btn_width, btn_height)
                )
                self.quit_button_controller = ButtonController(self.quit_button_view, "quit_game")
                Logger.debug("LoginPageView.setup_buttons", "Quit button created as ButtonView")
            except Exception as e:
                Logger.error("LoginPageView.setup_buttons", e)
                self.quit_button_view = None
            
            Logger.debug("LoginPageView.setup_buttons", "Login buttons setup complete")
        except Exception as e:
            Logger.error("LoginPageView.setup_buttons", e)
    



    def handle_quit(self):
        try:
            Logger.debug("LoginPageView.handle_quit", "Quit requested from login page")
            pygame.quit()
            sys.exit()
        except Exception as e:
            Logger.error("LoginPageView.handle_quit", e)
            pygame.quit()
            sys.exit()
    
    def switch_to_login(self):
        self.mode = "login"
        self.clear_inputs()
        self.error_message = ""
    



    def switch_to_register(self):
        self.mode = "register"
        self.clear_inputs()
        self.error_message = ""
    
    def clear_inputs(self):
        self.username_input = ""
        self.password_input = ""


        self.password_confirm_input = ""
        self.active_input = "username"
    




    def handle_login(self):

        try:
            if self.login_model.login(self.username_input, self.password_input):
                Logger.debug("LoginPageView.handle_login", "Login successful")
                self.on_login_success()
            else:
                self.error_message = self.login_model.login_error or "Connexion échouée"
                self.error_timer = 300
                Logger.debug("LoginPageView.handle_login", "Login failed", error=self.error_message)
        except Exception as e:
            Logger.error("LoginPageView.handle_login", e)
            self.error_message = "Erreur lors de la connexion"
            self.error_timer = 300



    
    def handle_register(self):
        try:
            if self.login_model.register(self.username_input, self.password_input, self.password_confirm_input):
                Logger.debug("LoginPageView.handle_register", "Registration successful")
                self.error_message = "Inscription réussie! Vous êtes maintenant connecté."
                self.error_timer = 300
                self.on_login_success()
            else:
                self.error_message = self.login_model.registration_error or "Inscription échouée"
                self.error_timer = 300
                Logger.debug("LoginPageView.handle_register", "Registration failed", error=self.error_message)
        except Exception as e:
            Logger.error("LoginPageView.handle_register", e)
            self.error_message = "Erreur lors de l'inscription"
            self.error_timer = 300
    
    def on_login_success(self):
        try:
            progression = self.login_model.get_user_progression()
            
            self.login_successful = True
            self.successful_user = self.login_model.current_user
            self.successful_progression = progression


            
            Logger.debug("LoginPageView.on_login_success", "Login successful, stored data for transition")
        except Exception as e:
            Logger.error("LoginPageView.on_login_success", e)
            self.error_message = "Erreur lors du chargement du jeu"



    
    def handle_input(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            
            if self.login_successful:
                return False
            
            return True
        except Exception as e:
            Logger.error("LoginPageView.handle_input", e)
            return False
        
    
    def handle_key_press(self, event):
        try:
            if event.key == pygame.K_TAB:
                fields = ["username", "password"]
                if self.mode == "register":
                    fields.append("password_confirm")
                
                current_idx = fields.index(self.active_input)
                self.active_input = fields[(current_idx + 1) % len(fields)]
            
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == "username":
                    self.username_input = self.username_input[:-1]
                elif self.active_input == "password":


                    self.password_input = self.password_input[:-1]
                elif self.active_input == "password_confirm":
                    self.password_confirm_input = self.password_confirm_input[:-1]
            
            elif event.key == pygame.K_RETURN:
                if self.mode == "login":
                    self.handle_login()
                else:
                    self.handle_register()
            
            elif event.unicode and event.unicode.isprintable():
                if len(event.unicode) > 0:
                    char = event.unicode


                    if self.active_input == "username" and len(self.username_input) < 20:
                        self.username_input += char
                    elif self.active_input == "password" and len(self.password_input) < 20:
                        self.password_input += char
                    elif self.active_input == "password_confirm" and len(self.password_confirm_input) < 20:
                        self.password_confirm_input += char
        except Exception as e:
            Logger.error("LoginPageView.handle_key_press", e)






    
    def handle_mouse_click(self, pos):
        try:
            x, y = pos
            
            if self.quit_button_view and self.quit_button_view.rect.collidepoint(x, y):
                self.handle_quit()

                return
            
            for field_name, field_info in self.input_fields.items():
                if field_name != "password_confirm" or self.mode == "register":
                    if field_info["rect"].collidepoint(x, y):
                        self.active_input = field_name
                        return
            
            visible_buttons = self.get_visible_buttons()
            for btn_name, btn_info in visible_buttons.items():
                if btn_info["rect"].collidepoint(x, y):


                    btn_info["action"]()
                    return
        except Exception as e:
            Logger.error("LoginPageView.handle_mouse_click", e)
    
    def get_visible_buttons(self):
        if self.mode == "login":
            return {
                "login_btn": self.buttons["login_btn"],
                "register_toggle_btn": self.buttons["register_toggle_btn"]
            }
        else:
            return {
                "register_btn": self.buttons["register_btn"],
                "login_toggle_btn": self.buttons["login_toggle_btn"]
            }
        



    
    def render(self):
        try:
            self.screen.blit(self.background, (0, 0))
            
            title_text = "Connexion" if self.mode == "login" else "S'inscrire"
            title_surface = self.font_large.render(title_text, True, self.color_text)
            title_rect = title_surface.get_rect(center=(self.width // 2, 80))
            self.screen.blit(title_surface, title_rect)
            
            self.render_inputs()
            self.render_buttons()
            


            if self.quit_button_view:
                self.quit_button_view.draw(self.screen)
            
            if self.error_message:
                self.render_error()
            
            pygame.display.flip()
        except Exception as e:
            Logger.error("LoginPageView.render", e)
    




    def render_inputs(self):
        try:
            visible_fields = ["username", "password"]


            if self.mode == "register":
                visible_fields.append("password_confirm")
            
            for field_name in visible_fields:
                field_info = self.input_fields[field_name]
                rect = field_info["rect"]
                is_active = self.active_input == field_name
                
                border_color = self.color_input_active if is_active else self.color_input_border
                pygame.draw.rect(self.screen, border_color, rect, 3)
                pygame.draw.rect(self.screen, self.color_input_bg, rect.inflate(-6, -6))
                

                if field_name == "username":
                    display_value = self.username_input
                elif field_name == "password":
                    display_value = "*" * len(self.password_input)
                else:
                    display_value = "*" * len(self.password_confirm_input)
                
                text_surface = self.font_medium.render(display_value, True, self.color_text)
                text_rect = text_surface.get_rect(midleft=(rect.x + 10, rect.centery))
                self.screen.blit(text_surface, text_rect)


                
                label_surface = self.font_small.render(field_info["label"], True, self.color_text)
                self.screen.blit(label_surface, (rect.x, rect.y - 30))
                
                if is_active:
                    cursor_rect = pygame.Rect(rect.x + 10 + text_rect.width, rect.centery - 10, 2, 20)
                    pygame.draw.rect(self.screen, self.color_text, cursor_rect)
        except Exception as e:
            Logger.error("LoginPageView.render_inputs", e)





    
    def render_buttons(self):
        try:
            visible_buttons = self.get_visible_buttons()

            
            for btn_name, btn_info in visible_buttons.items():
                rect = btn_info["rect"]
                label = btn_info["label"]
                
                pygame.draw.rect(self.screen, (100, 100, 150), rect)
                pygame.draw.rect(self.screen, (200, 200, 255), rect, 2)
                
                text_surface = self.font_medium.render(label, True, self.color_text)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)
        except Exception as e:
            Logger.error("LoginPageView.render_buttons", e)



    
    def render_error(self):
        try:
            error_surface = self.font_small.render(self.error_message, True, self.color_error)
            error_rect = error_surface.get_rect(center=(self.width // 2, self.height - 100))
            self.screen.blit(error_surface, error_rect)
            
            if self.error_timer > 0:
                self.error_timer -= 1
            else:
                self.error_message = ""

        except Exception as e:
            Logger.error("LoginPageView.render_error", e)
    
    def run(self):
        try:
            Logger.debug("LoginPageView.run", "Login page run loop started")
            
            running = True
            while running:
                running = self.handle_input()
                
                if self.login_successful:
                    running = False
                    Logger.debug("LoginPageView.run", "Login successful, exiting run loop")
                
                self.render()
                self.clock.tick(self.fps)
            
            
            Logger.debug("LoginPageView.run", "Login page run loop ended")
            
            if self.login_successful:
                return {
                    "success": True,
                    "user": self.successful_user,
                    "progression": self.successful_progression,
                    "is_admin": self.login_model.is_user_admin(),
                    "width": self.width,
                    "height": self.height
                }
            else:
                return {"success": False}
        except Exception as e:
            Logger.error("LoginPageView.run", e)
            return {"success": False}
        finally:
            if not self.login_successful:
                try:
                    pygame.quit()
                except Exception:
                    pass
