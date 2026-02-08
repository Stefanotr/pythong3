
    
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
            
            if not self.user_manager.authenticate_user(username, password):
                self.login_error = "Nom d'utilisateur ou mot de passe incorrect"
                return False
            
            progression = self.user_manager.load_progression(username)
            
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
            
            if self.user_manager.user_exists(username):
                self.registration_error = "Ce nom d'utilisateur existe déjà"
                return False
            
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
    
    
    def get_current_user(self):
        return self.current_user
    
    def logout(self):
        self.current_user = None
        self.is_admin = False
        self.login_error = None
        self.registration_error = None
        Logger.debug("LoginModel.logout", "User logged out")
    
    def is_user_admin(self):
        return self.is_admin
    
    
    def get_user_progression(self, username=None):
        try:
            target_user = username if username else self.current_user
            
            if not target_user:
                return None
            
            return self.user_manager.load_progression(target_user)
        except Exception as e:
            Logger.error("LoginModel.get_user_progression", e)
            return None
    
    def save_user_progression(self, progression_data, username=None):
        try:
            target_user = username if username else self.current_user
            
            if not target_user:
                return False
            
            return self.user_manager.save_progression(target_user, progression_data)
        except Exception as e:
            Logger.error("LoginModel.save_user_progression", e)
            return False
    
    
    def get_all_users(self):
        try:
            return self.user_manager.get_all_users()
        except Exception as e:
            Logger.error("LoginModel.get_all_users", e)
            return []
    
    def clear_errors(self):
        self.login_error = None
        self.registration_error = None
