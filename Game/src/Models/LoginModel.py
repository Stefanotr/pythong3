"""
LoginModel Module

Represents the login system with user authentication and registration.
Manages login state and user session information.
"""

from Utils.UserManager import UserManager
from Utils.Logger import Logger


class LoginModel:
    """
    Login model handling user authentication and registration.
    Manages login state and current user session.
    """
    
    def __init__(self):
        """Initialize the login model."""
        try:
            self.user_manager = UserManager()
            self.current_user = None
            self.is_admin = False  # Flag for admin privileges
            self.login_error = None
            self.registration_error = None
            Logger.debug("LoginModel.__init__", "Login model initialized")
        except Exception as e:
            Logger.error("LoginModel.__init__", e)
            raise
    
    # === LOGIN OPERATIONS ===
    
    def login(self, username, password):
        """
        Attempt to login a user.
        
        Args:
            username: Username to login
            password: Password to verify
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            self.login_error = None
            self.is_admin = False  # Reset admin status
            
            if not username or not password:
                self.login_error = "Username et mot de passe requis"
                return False
            
            # Validate credentials
            if not self.user_manager.authenticate_user(username, password):
                self.login_error = "Nom d'utilisateur ou mot de passe incorrect"
                return False
            
            # Load player progression
            progression = self.user_manager.load_progression(username)
            
            if progression is None:
                self.login_error = "Impossible de charger la progression"
                return False
            
            self.current_user = username
            
            # Check if user is admin (username "admin" has admin privileges)
            self.is_admin = (username.lower() == "admin")
            
            if self.is_admin:
                Logger.debug("LoginModel.login", "Admin user logged in", username=username)
            else:
                Logger.debug("LoginModel.login", "User logged in successfully", username=username)
            
            return True
        except Exception as e:
            Logger.error("LoginModel.login", e)
            self.login_error = "Erreur lors de la connexion"
            return False
    
    # === REGISTRATION OPERATIONS ===
    
    def register(self, username, password, password_confirm):
        """
        Attempt to register a new user.
        
        Args:
            username: Username for new account
            password: Password for new account
            password_confirm: Password confirmation
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            self.registration_error = None
            
            # Validate input
            if not username or not password or not password_confirm:
                self.registration_error = "Tous les champs sont requis"
                return False
            
            if len(username) < 3:
                self.registration_error = "Le nom d'utilisateur doit avoir au moins 3 caractères"
                return False
            
            if len(password) < 4:
                self.registration_error = "Le mot de passe doit avoir au moins 4 caractères"
                return False
            
            if password != password_confirm:
                self.registration_error = "Les mots de passe ne correspondent pas"
                return False
            
            # Check if user already exists
            if self.user_manager.user_exists(username):
                self.registration_error = "Ce nom d'utilisateur existe déjà"
                return False
            
            # Register user
            if not self.user_manager.register_user(username, password):
                self.registration_error = "Erreur lors de l'enregistrement"
                return False
            
            self.current_user = username
            Logger.debug("LoginModel.register", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("LoginModel.register", e)
            self.registration_error = "Erreur lors de l'enregistrement"
            return False
    
    # === USER SESSION MANAGEMENT ===
    
    def get_current_user(self):
        """
        Get the current logged-in user.
        
        Returns:
            Current username or None if not logged in
        """
        return self.current_user
    
    def logout(self):
        """Logout the current user."""
        self.current_user = None
        self.is_admin = False
        self.login_error = None
        self.registration_error = None
        Logger.debug("LoginModel.logout", "User logged out")
    
    def is_user_admin(self):
        """
        Check if current user is admin.
        
        Returns:
            True if user is admin, False otherwise
        """
        return self.is_admin
    
    # === PROGRESSION MANAGEMENT ===
    
    def get_user_progression(self, username=None):
        """
        Get progression data for a user.
        
        Args:
            username: Username to get progression for (defaults to current user)
            
        Returns:
            Progression data dictionary or None
        """
        try:
            target_user = username if username else self.current_user
            
            if not target_user:
                return None
            
            return self.user_manager.load_progression(target_user)
        except Exception as e:
            Logger.error("LoginModel.get_user_progression", e)
            return None
    
    def save_user_progression(self, progression_data, username=None):
        """
        Save progression data for a user.
        
        Args:
            progression_data: Progression data dictionary to save
            username: Username to save for (defaults to current user)
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            target_user = username if username else self.current_user
            
            if not target_user:
                return False
            
            return self.user_manager.save_progression(target_user, progression_data)
        except Exception as e:
            Logger.error("LoginModel.save_user_progression", e)
            return False
    
    # === UTILITY METHODS ===
    
    def get_all_users(self):
        """
        Get list of all registered users.
        
        Returns:
            List of usernames
        """
        try:
            return self.user_manager.get_all_users()
        except Exception as e:
            Logger.error("LoginModel.get_all_users", e)
            return []
    
    def clear_errors(self):
        """Clear all error messages."""
        self.login_error = None
        self.registration_error = None
