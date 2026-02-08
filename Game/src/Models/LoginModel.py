from Utils.UserManager import UserManager
from Utils.Logger import Logger


class LoginModel:

    def __init__(self):
        try:
            self.userManager = UserManager()
            self.currentUser = None
            self.isAdmin = False
            self.loginError = None
            self.registrationError = None
            Logger.debug("LoginModel.__init__", "Login model initialized")
        except Exception as e:
            Logger.error("LoginModel.__init__", e)
            raise


    def login(self, username, password):
        try:
            self.loginError = None
            self.isAdmin = False
            
            if not username or not password:
                self.loginError = "Username et mot de passe requis"
                return False
            
            if not self.userManager.authenticate_user(username, password):
                self.loginError = "Nom d'utilisateur ou mot de passe incorrect"
                return False
            
            progression = self.userManager.load_progression(username)
            
            if progression is None:
                self.loginError = "Impossible de charger la progression"
                return False
            
            self.currentUser = username
            self.isAdmin = (username.lower() == "admin")
            
            if self.isAdmin:
                Logger.debug("LoginModel.login", "Admin user logged in", username=username)
            else:
                Logger.debug("LoginModel.login", "User logged in successfully", username=username)
            
            return True
        except Exception as e:
            Logger.error("LoginModel.login", e)
            self.loginError = "Erreur lors de la connexion"
            return False


    def register(self, username, password, passwordConfirm):
        try:
            self.registrationError = None
            
            if not username or not password or not passwordConfirm:
                self.registrationError = "Tous les champs sont requis"
                return False
            
            if len(username) < 3:
                self.registrationError = "Le nom d'utilisateur doit avoir au moins 3 caractères"
                return False
            
            if len(password) < 4:
                self.registrationError = "Le mot de passe doit avoir au moins 4 caractères"
                return False
            
            if password != passwordConfirm:
                self.registrationError = "Les mots de passe ne correspondent pas"
                return False
            
            if self.userManager.user_exists(username):
                self.registrationError = "Ce nom d'utilisateur existe déjà"
                return False
            
            if not self.userManager.register_user(username, password):
                self.registrationError = "Erreur lors de l'enregistrement"
                return False
            
            self.currentUser = username
            Logger.debug("LoginModel.register", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("LoginModel.register", e)
            self.registrationError = "Erreur lors de l'enregistrement"
            return False


    def getCurrentUser(self):
        return self.currentUser
    
    def logout(self):
        try:
            self.currentUser = None
            self.isAdmin = False
            self.loginError = None
            self.registrationError = None
            Logger.debug("LoginModel.logout", "User logged out")
        except Exception as e:
            Logger.error("LoginModel.logout", e)
    
    def isUserAdmin(self):
        return self.isAdmin


    def getUserProgression(self, username=None):
        try:
            targetUser = username if username else self.currentUser
            
            if not targetUser:
                return None
            
            return self.userManager.load_progression(targetUser)
        except Exception as e:
            Logger.error("LoginModel.getUserProgression", e)
            return None
    
    def saveUserProgression(self, progressionData, username=None):
        try:
            targetUser = username if username else self.currentUser
            
            if not targetUser:
                return False
            
            return self.userManager.save_progression(targetUser, progressionData)
        except Exception as e:
            Logger.error("LoginModel.saveUserProgression", e)
            return False


    def getAllUsers(self):
        try:
            return self.userManager.get_all_users()
        except Exception as e:
            Logger.error("LoginModel.getAllUsers", e)
            return []
    
    def clearErrors(self):
        try:
            self.loginError = None
            self.registrationError = None
        except Exception as e:
            Logger.error("LoginModel.clearErrors", e)
