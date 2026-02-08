"""
UserManager Module

Manages user authentication, progression data, and the relationship between credentials and player data.
Handles encrypting/decrypting passwords and linking credentials to player progression files.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from Utils.Logger import Logger


class UserManager:

    PROGRESSION_DIR = "Game/Progression"
    CREDENTIALS_FILE = ".credentials.json"
    KEY_FILE = ".secret.key"

    def __init__(self):
        try:
            os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            self.initializeEncryptionKey()
            Logger.debug("UserManager.__init__", "UserManager initialized")
        except Exception as e:
            Logger.error("UserManager.__init__", e)
            raise
    

    def initializeEncryptionKey(self):
        try:
            key_path = os.path.join(self.PROGRESSION_DIR, self.KEY_FILE)
            if os.path.exists(key_path):
                with open(key_path, 'rb') as f:
                    self.cipher_key = f.read()
            else:
                self.cipher_key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(self.cipher_key)
                Logger.debug("UserManager.initializeEncryptionKey", "New encryption key created")
            
            self.cipher = Fernet(self.cipher_key)
        except Exception as e:
            Logger.error("UserManager.initializeEncryptionKey", e)
            raise
    
    def encryptPassword(self, password):
        try:
            encrypted = self.cipher.encrypt(password.encode())
            return encrypted.decode()
        except Exception as e:
            Logger.error("UserManager.encryptPassword", e)
            raise
    
    def decryptPassword(self, encrypted_password):
        try:
            decrypted = self.cipher.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            Logger.error("UserManager.decryptPassword", e)
            raise
    

    def getCredentialsData(self):
        try:
            cred_path = os.path.join(self.PROGRESSION_DIR, self.CREDENTIALS_FILE)
            
            if os.path.exists(cred_path):
                with open(cred_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            Logger.error("UserManager.getCredentialsData", e)
            raise
    
    def saveCredentialsData(self, credentials):
        try:
            cred_path = os.path.join(self.PROGRESSION_DIR, self.CREDENTIALS_FILE)
            try:
                os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            except Exception as e:
                Logger.error("UserManager.saveCredentialsData", f"Could not create directory: {e}")
            
            # Try to remove old file if it exists (to handle locked files)
            try:
                if os.path.exists(cred_path):
                    os.remove(cred_path)
                    Logger.debug("UserManager.saveCredentialsData", "Removed old credentials file")
            except PermissionError:
                Logger.debug("UserManager.saveCredentialsData", "Old credentials file is locked, will overwrite")
            except Exception as e:
                Logger.debug("UserManager.saveCredentialsData", f"Could not remove old file: {e}")
            
            # Write new credentials file
            with open(cred_path, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2)
            
            Logger.debug("UserManager.saveCredentialsData", "Credentials saved successfully", path=cred_path)
            
            # Try to hide the file on Windows
            try:
                import subprocess
                subprocess.run(['attrib', '+h', cred_path], check=False, capture_output=True)
            except Exception:
                pass  # Non-Windows system, file hiding not needed
        except Exception as e:
            Logger.error("UserManager.saveCredentialsData", e)
            raise
    

    def registerUser(self, username, password):
        """
        Register a new user with username and password.
        Creates player progression file.
        
        Args:
            username: Username for the new account
            password: Password for the new account
            
        Returns:
            True if registration successful, False if username already exists
        """
        try:
            if self.userExists(username):
                Logger.debug("UserManager.registerUser", "Registration failed: username already exists", username=username)
                return False
            
            credentials = self.getCredentialsData()
            
            encrypted_pwd = self.encryptPassword(password)
            credentials[username] = {
                "password": encrypted_pwd,
                "created_date": datetime.now().isoformat(),
                "progression_file": f"{username}_progression.json"
            }
            
            self.saveCredentialsData(credentials)
            
            self.createEmptyProgression(username)
            
            Logger.debug("UserManager.registerUser", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.registerUser", e)
            raise
    

    def authenticateUser(self, username, password):
        try:
            credentials = self.getCredentialsData()
            
            if username not in credentials:
                Logger.debug("UserManager.authenticateUser", "Authentication failed: username not found", username=username)
                return False
            
            stored_encrypted_pwd = credentials[username]["password"]
            stored_password = self.decryptPassword(stored_encrypted_pwd)
            
            result = stored_password == password
            if result:
                Logger.debug("UserManager.authenticateUser", "User authenticated successfully", username=username)
            else:
                Logger.debug("UserManager.authenticateUser", "Authentication failed: wrong password", username=username)
            
            return result
        except Exception as e:
            Logger.error("UserManager.authenticateUser", e)
            return False
    

    def userExists(self, username):
        try:
            credentials = self.getCredentialsData()
            return username in credentials
        except Exception as e:
            Logger.error("UserManager.userExists", e)
            return False
    

    def createEmptyProgression(self, username):
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
            
            self.saveProgression(username, progression_data)
            Logger.debug("UserManager.createEmptyProgression", "Empty progression file created", username=username)
        except Exception as e:
            Logger.error("UserManager.createEmptyProgression", e)
            raise
    
    def getProgressionFilepath(self, username):
        try:
            credentials = self.getCredentialsData()
            
            if username not in credentials:
                return None
            
            progression_filename = credentials[username]["progression_file"]
            return os.path.join(self.PROGRESSION_DIR, progression_filename)
        except Exception as e:
            Logger.error("UserManager.getProgressionFilepath", e)
            return None
    
    def loadProgression(self, username):
        try:
            filepath = self.getProgressionFilepath(username)
            
            if filepath is None or not os.path.exists(filepath):
                Logger.debug("UserManager.loadProgression", "Progression file not found", username=username)
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                progression_data = json.load(f)
            
            Logger.debug("UserManager.loadProgression", "Progression loaded successfully", username=username)
            return progression_data
        except Exception as e:
            Logger.error("UserManager.loadProgression", e)
            return None
    
    def saveProgression(self, username, progression_data):
        try:
            filepath = self.getProgressionFilepath(username)
            
            if filepath is None:
                Logger.debug("UserManager.saveProgression", "Cannot save: user progression file not mapped", username=username)
                return False
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            progression_data["last_save"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(progression_data, f, indent=2, ensure_ascii=False)
            
            Logger.debug("UserManager.saveProgression", "Progression saved successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.saveProgression", e)
            return False
    

    def getAllUsers(self):
        try:
            credentials = self.getCredentialsData()
            return list(credentials.keys())
        except Exception as e:
            Logger.error("UserManager.getAllUsers", e)
            return []
    
    def deleteUser(self, username):
        try:
            credentials = self.getCredentialsData()
            
            if username not in credentials:
                return False
            
            del credentials[username]
            self.saveCredentialsData(credentials)
            
            filepath = self.getProgressionFilepath(username)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            
            Logger.debug("UserManager.deleteUser", "User deleted successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.deleteUser", e)
            return False
