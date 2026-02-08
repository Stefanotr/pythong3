

    
    PROGRESSION_DIR = "Game/Progression"
    CREDENTIALS_FILE = ".credentials.json"
    KEY_FILE = ".secret.key"
    
    
    def __init__(self):
        try:
            os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            
            self._initialize_encryption_key()
            
            Logger.debug("UserManager.__init__", "UserManager initialized")
        except Exception as e:
            Logger.error("UserManager.__init__", e)
            raise
    
    
    def _initialize_encryption_key(self):
        try:
            key_path = os.path.join(self.PROGRESSION_DIR, self.KEY_FILE)
            
            if os.path.exists(key_path):
                with open(key_path, 'rb') as f:
                    self.cipher_key = f.read()
            else:
                self.cipher_key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(self.cipher_key)
                Logger.debug("UserManager._initialize_encryption_key", "New encryption key created")
            
            self.cipher = Fernet(self.cipher_key)
        except Exception as e:
            Logger.error("UserManager._initialize_encryption_key", e)
            raise
    
    
    def _encrypt_password(self, password):
        try:
            encrypted = self.cipher.encrypt(password.encode())
            return encrypted.decode()
        except Exception as e:
            Logger.error("UserManager._encrypt_password", e)
            raise
    
    def _decrypt_password(self, encrypted_password):
        try:
            decrypted = self.cipher.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            Logger.error("UserManager._decrypt_password", e)
            raise
    
    
    def _get_credentials_data(self):
        try:
            cred_path = os.path.join(self.PROGRESSION_DIR, self.CREDENTIALS_FILE)
            
            if os.path.exists(cred_path):
                with open(cred_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            Logger.error("UserManager._get_credentials_data", e)
            raise
    
    def _save_credentials_data(self, credentials):
        try:
            cred_path = os.path.join(self.PROGRESSION_DIR, self.CREDENTIALS_FILE)
            
            try:
                os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            except Exception as e:
                Logger.error("UserManager._save_credentials_data", f"Could not create directory: {e}")
            
            try:
                if os.path.exists(cred_path):
                    os.remove(cred_path)
                    Logger.debug("UserManager._save_credentials_data", "Removed old credentials file")
            except PermissionError:
                Logger.debug("UserManager._save_credentials_data", "Old credentials file is locked, will overwrite")
            except Exception as e:
                Logger.debug("UserManager._save_credentials_data", f"Could not remove old file: {e}")
            
            with open(cred_path, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2)
            
            Logger.debug("UserManager._save_credentials_data", "Credentials saved successfully", path=cred_path)
            
            try:
                import subprocess
                subprocess.run(['attrib', '+h', cred_path], check=False, capture_output=True)
            except Exception:
                pass
        except Exception as e:
            Logger.error("UserManager._save_credentials_data", e)
            raise
    
    
    def register_user(self, username, password):
        try:
            if self.user_exists(username):
                Logger.debug("UserManager.register_user", "Registration failed: username already exists", username=username)
                return False
            
            credentials = self._get_credentials_data()
            
            encrypted_pwd = self._encrypt_password(password)
            credentials[username] = {
                "password": encrypted_pwd,
                "created_date": datetime.now().isoformat(),
                "progression_file": f"{username}_progression.json"
            }
            
            self._save_credentials_data(credentials)
            
            self._create_empty_progression(username)
            
            Logger.debug("UserManager.register_user", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.register_user", e)
            raise
    
    
    def authenticate_user(self, username, password):
        try:
            credentials = self._get_credentials_data()
            
            if username not in credentials:
                Logger.debug("UserManager.authenticate_user", "Authentication failed: username not found", username=username)
                return False
            
            stored_encrypted_pwd = credentials[username]["password"]
            stored_password = self._decrypt_password(stored_encrypted_pwd)
            
            result = stored_password == password
            if result:
                Logger.debug("UserManager.authenticate_user", "User authenticated successfully", username=username)
            else:
                Logger.debug("UserManager.authenticate_user", "Authentication failed: wrong password", username=username)
            
            return result
        except Exception as e:
            Logger.error("UserManager.authenticate_user", e)
            return False
    
    
    def user_exists(self, username):
        try:
            credentials = self._get_credentials_data()
            return username in credentials
        except Exception as e:
            Logger.error("UserManager.user_exists", e)
            return False
    
    
    def _create_empty_progression(self, username):
        try:
            progression_data = {
                "created_date": datetime.now().isoformat(),
                "last_save": datetime.now().isoformat(),
                "current_stage": 1,
                "level": 0,
                "hp": 100,
                "max_hp": 100,
                "damage": 10,
                "drunkenness": 0,
                "coma_risk": 0,
                "position": {"x": 175, "y": 175},
                "inventory": [],
                "completed_acts": [],
                "completed_rhythms": []
            }
            
            self.save_progression(username, progression_data)
            Logger.debug("UserManager._create_empty_progression", "Empty progression file created", username=username)
        except Exception as e:
            Logger.error("UserManager._create_empty_progression", e)
            raise
    
    def get_progression_filepath(self, username):
        try:
            credentials = self._get_credentials_data()
            
            if username not in credentials:
                return None
            
            progression_filename = credentials[username]["progression_file"]
            return os.path.join(self.PROGRESSION_DIR, progression_filename)
        except Exception as e:
            Logger.error("UserManager.get_progression_filepath", e)
            return None
    
    def load_progression(self, username):
        try:
            filepath = self.get_progression_filepath(username)
            
            if filepath is None or not os.path.exists(filepath):
                Logger.debug("UserManager.load_progression", "Progression file not found", username=username)
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                progression_data = json.load(f)
            
            Logger.debug("UserManager.load_progression", "Progression loaded successfully", username=username)
            return progression_data
        except Exception as e:
            Logger.error("UserManager.load_progression", e)
            return None
    
    def save_progression(self, username, progression_data):
        try:
            filepath = self.get_progression_filepath(username)
            
            if filepath is None:
                Logger.debug("UserManager.save_progression", "Cannot save: user progression file not mapped", username=username)
                return False
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            progression_data["last_save"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(progression_data, f, indent=2, ensure_ascii=False)
            
            Logger.debug("UserManager.save_progression", "Progression saved successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.save_progression", e)
            return False
    
    
    def get_all_users(self):
        try:
            credentials = self._get_credentials_data()
            return list(credentials.keys())
        except Exception as e:
            Logger.error("UserManager.get_all_users", e)
            return []
    
    def delete_user(self, username):
        try:
            credentials = self._get_credentials_data()
            
            if username not in credentials:
                return False
            
            del credentials[username]
            self._save_credentials_data(credentials)
            
            filepath = self.get_progression_filepath(username)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            
            Logger.debug("UserManager.delete_user", "User deleted successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.delete_user", e)
            return False
