"""
LoginController Module

Controls the login flow and transitions between login and game screens.
Manages user authentication and session state.
"""

from Models.LoginModel import LoginModel
from Views.LoginPageView import LoginPageView
from Utils.Logger import Logger


class LoginController:
    """
    Controller for managing the login flow.
    Coordinates between LoginModel and LoginPageView.
    """
    
    def __init__(self):
        """Initialize the login controller."""
        try:
            self.login_model = LoginModel()
            self.login_view = None
            Logger.debug("LoginController.__init__", "Login controller initialized")
        except Exception as e:
            Logger.error("LoginController.__init__", e)
            raise
    
    def start_login_flow(self):
        """
        Start the login flow by displaying the login page.
        
        Returns:
            Username of logged-in user or None if user quit
        """
        try:
            # Create and display login view
            self.login_view = LoginPageView(
                "Connexion",
                800,
                800,
                0,
                "Game/Assets/welcomePage.png"
            )
            
            # Run login view (this will transition to game on successful login)
            self.login_view.run()
            
            # Return current user if successfully logged in
            return self.login_model.get_current_user()
        except Exception as e:
            Logger.error("LoginController.start_login_flow", e)
            return None
    
    def get_current_user(self):
        """
        Get the currently logged-in user.
        
        Returns:
            Username or None if no user logged in
        """
        return self.login_model.get_current_user()
    
    def get_user_progression(self):
        """
        Get progression data for current user.
        
        Returns:
            Progression data dict or None
        """
        return self.login_model.get_user_progression()
    
    def save_progression(self, progression_data):
        """
        Save progression for current user.
        
        Args:
            progression_data: Progression data to save
            
        Returns:
            True if save successful, False otherwise
        """
        return self.login_model.save_user_progression(progression_data)
    
    def logout(self):
        """Logout the current user."""
        self.login_model.logout()
        Logger.debug("LoginController.logout", "User logged out")
