from Utils.UserManager import UserManager
from Utils.Logger import Logger


class LoginModel:

    def __init__(self):
        try:
            self.user_manager = UserManager()
            self.current_user = None
            self.is_admin = False
            self.login_error = None
            self.registration_error = None
            Logger.debug("LoginModel.__init__", "Login model initialized")
        except Exception as e:
            Logger.error("LoginModel.__init__", e)
            raise


    def login(self, username, password):
        try:
            self.login_error = None
            self.is_admin = False
            
            if not username or not password:
                self.login_error = "Username et mot de passe requis"
                return False
            
            if not self.user_manager.authenticateUser(username, password):
                self.login_error = "Nom d'utilisateur ou mot de passe incorrect"
                return False
            
            progression = self.user_manager.loadProgression(username)
            
            if progression is None:
                self.login_error = "Impossible de charger la progression"
                return False
            
            self.current_user = username
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


    def register(self, username, password, password_confirm):
        try:
            self.registration_error = None
            
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
            
            if self.user_manager.userExists(username):
                self.registration_error = "Ce nom d'utilisateur existe déjà"
                return False
            
            if not self.user_manager.registerUser(username, password):
                self.registration_error = "Erreur lors de l'enregistrement"
                return False
            
            self.current_user = username
            Logger.debug("LoginModel.register", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("LoginModel.register", e)
            self.registration_error = "Erreur lors de l'enregistrement"
            return False


    def getCurrentUser(self):
        return self.current_user
    
    def logout(self):
        try:
            self.current_user = None
            self.is_admin = False
            self.login_error = None
            self.registration_error = None
            Logger.debug("LoginModel.logout", "User logged out")
        except Exception as e:
            Logger.error("LoginModel.logout", e)
    
    def isUserAdmin(self):
        return self.is_admin


    def getUserProgression(self, username=None):
        try:
            targe_user = username if username else self.current_user
            
            if not targe_user:
                return None
            
            return self.user_manager.loadProgression(targe_user)
        except Exception as e:
            Logger.error("LoginModel.getUserProgression", e)
            return None
    
    def saveUserProgression(self, progression_data, username=None):
        try:
            target_user = username if username else self.current_user
            
            if not target_user:
                return False
            
            return self.user_manager.saveProgression(target_user, progression_data)
        except Exception as e:
            Logger.error("LoginModel.saveUserProgression", e)
            return False


    def getAllUsers(self):
        try:
            return self.user_manager.get_all_users()
        except Exception as e:
            Logger.error("LoginModel.getAllUsers", e)
            return []
    
    def clearErrors(self):
        try:
            self.login_error = None
            self.registration_error = None
        except Exception as e:
            Logger.error("LoginModel.clearErrors", e)
