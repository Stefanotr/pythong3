

from Models.LoginModel import LoginModel
from Views.LoginPageView import LoginPageView
from Utils.Logger import Logger

class LoginController:

    
    def __init__(self):
       
        try:
            self.login_model = LoginModel()
            self.login_view = None
            Logger.debug("LoginController.__init__", "Login controller initialized")
        except Exception as e:
            Logger.error("LoginController.__init__", e)
            raise
    
    def start_login_flow(self):
        
        try:
            self.login_view = LoginPageView(
                "Connexion",
                800,
                800,
                0,
                "Game/Assets/welcomePage.png"
            )
            
            self.login_view.run()
            
            return self.login_model.get_current_user()
        except Exception as e:
            Logger.error("LoginController.start_login_flow", e)
            return None
    
    def get_current_user(self):
      
        return self.login_model.get_current_user()
    
    def get_user_progression(self):
        
        return self.login_model.get_user_progression()
    
    def save_progression(self, progression_data):
        
        return self.login_model.save_user_progression(progression_data)
    
    def logout(self):
        
        self.login_model.logout()
        Logger.debug("LoginController.logout", "User logged out")
