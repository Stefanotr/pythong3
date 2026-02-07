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
    """
    Manages user authentication and progression data.
    Handles credential encryption and linking with player progression files.
    """

    # === CONSTANTS ===
    
    PROGRESSION_DIR = "Game/Progression"
    CREDENTIALS_FILE = ".credentials.json"  # Hidden file for credentials
    KEY_FILE = ".secret.key"  # Encryption key file
    
    # === INITIALIZATION ===
    
    def __init__(self):
        """Initialize UserManager and ensure necessary directories and keys exist."""
        try:
            # Ensure progression directory exists
            os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            
            # Initialize encryption key
            self._initialize_encryption_key()
            
            Logger.debug("UserManager.__init__", "UserManager initialized")
        except Exception as e:
            Logger.error("UserManager.__init__", e)
            raise
    
    # === ENCRYPTION KEY MANAGEMENT ===
    
    def _initialize_encryption_key(self):
        """Initialize or load the encryption key for password encryption."""
        try:
            key_path = os.path.join(self.PROGRESSION_DIR, self.KEY_FILE)
            
            if os.path.exists(key_path):
                # Load existing key
                with open(key_path, 'rb') as f:
                    self.cipher_key = f.read()
            else:
                # Generate new key
                self.cipher_key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(self.cipher_key)
                Logger.debug("UserManager._initialize_encryption_key", "New encryption key created")
            
            self.cipher = Fernet(self.cipher_key)
        except Exception as e:
            Logger.error("UserManager._initialize_encryption_key", e)
            raise
    
    # === PASSWORD ENCRYPTION/DECRYPTION ===
    
    def _encrypt_password(self, password):
        """
        Encrypt a password using Fernet symmetric encryption.
        
        Args:
            password: Plain text password
            
        Returns:
            Encrypted password as string
        """
        try:
            encrypted = self.cipher.encrypt(password.encode())
            return encrypted.decode()
        except Exception as e:
            Logger.error("UserManager._encrypt_password", e)
            raise
    
    def _decrypt_password(self, encrypted_password):
        """
        Decrypt a password using Fernet symmetric encryption.
        
        Args:
            encrypted_password: Encrypted password string
            
        Returns:
            Decrypted password as string
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            Logger.error("UserManager._decrypt_password", e)
            raise
    
    # === CREDENTIALS FILE MANAGEMENT ===
    
    def _get_credentials_data(self):
        """
        Load all credentials from the hidden credentials file.
        
        Returns:
            Dictionary of credentials or empty dict if file doesn't exist
        """
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
        """
        Save credentials to the hidden credentials file.
        
        Args:
            credentials: Dictionary of credentials to save
        """
        try:
            cred_path = os.path.join(self.PROGRESSION_DIR, self.CREDENTIALS_FILE)
            
            # Ensure directory exists
            try:
                os.makedirs(self.PROGRESSION_DIR, exist_ok=True)
            except Exception as e:
                Logger.error("UserManager._save_credentials_data", f"Could not create directory: {e}")
            
            # Try to remove old file if it exists (to handle locked files)
            try:
                if os.path.exists(cred_path):
                    os.remove(cred_path)
                    Logger.debug("UserManager._save_credentials_data", "Removed old credentials file")
            except PermissionError:
                Logger.debug("UserManager._save_credentials_data", "Old credentials file is locked, will overwrite")
            except Exception as e:
                Logger.debug("UserManager._save_credentials_data", f"Could not remove old file: {e}")
            
            # Write new credentials file
            with open(cred_path, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2)
            
            Logger.debug("UserManager._save_credentials_data", "Credentials saved successfully", path=cred_path)
            
            # Try to hide the file on Windows
            try:
                import subprocess
                subprocess.run(['attrib', '+h', cred_path], check=False, capture_output=True)
            except Exception:
                pass  # Non-Windows system, file hiding not needed
        except Exception as e:
            Logger.error("UserManager._save_credentials_data", e)
            raise
    
    # === USER REGISTRATION ===
    
    def register_user(self, username, password):
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
            # Check if user already exists
            if self.user_exists(username):
                Logger.debug("UserManager.register_user", "Registration failed: username already exists", username=username)
                return False
            
            # Load existing credentials
            credentials = self._get_credentials_data()
            
            # Add new user with encrypted password
            encrypted_pwd = self._encrypt_password(password)
            credentials[username] = {
                "password": encrypted_pwd,
                "created_date": datetime.now().isoformat(),
                "progression_file": f"{username}_progression.json"
            }
            
            # Save updated credentials
            self._save_credentials_data(credentials)
            
            # Create empty progression file
            self._create_empty_progression(username)
            
            Logger.debug("UserManager.register_user", "User registered successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.register_user", e)
            raise
    
    # === USER AUTHENTICATION ===
    
    def authenticate_user(self, username, password):
        """
        Authenticate user with username and password.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            credentials = self._get_credentials_data()
            
            if username not in credentials:
                Logger.debug("UserManager.authenticate_user", "Authentication failed: username not found", username=username)
                return False
            
            # Decrypt stored password and compare
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
    
    # === USER EXISTENCE CHECK ===
    
    def user_exists(self, username):
        """
        Check if a user already exists.
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        try:
            credentials = self._get_credentials_data()
            return username in credentials
        except Exception as e:
            Logger.error("UserManager.user_exists", e)
            return False
    
    # === PROGRESSION FILE MANAGEMENT ===
    
    def _create_empty_progression(self, username):
        """
        Create an empty progression file for a new user.
        
        Args:
            username: Username for the progression file
        """
        try:
            # Note: Game character is always "Lola Coma" - username is only for login
            # Username is associated via the progression filename, not stored in the data
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
        """
        Get the full filepath for a user's progression file.
        
        Args:
            username: Username
            
        Returns:
            Full path to progression file
        """
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
        """
        Load player progression data from file.
        
        Args:
            username: Username whose progression to load
            
        Returns:
            Progression data dictionary or None if file doesn't exist
        """
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
        """
        Save player progression data to file.
        
        Args:
            username: Username whose progression to save
            progression_data: Dictionary of progression data to save
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            filepath = self.get_progression_filepath(username)
            
            if filepath is None:
                Logger.debug("UserManager.save_progression", "Cannot save: user progression file not mapped", username=username)
                return False
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Update last save timestamp
            progression_data["last_save"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(progression_data, f, indent=2, ensure_ascii=False)
            
            Logger.debug("UserManager.save_progression", "Progression saved successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.save_progression", e)
            return False
    
    # === UTILITY METHODS ===
    
    def get_all_users(self):
        """
        Get list of all registered usernames.
        
        Returns:
            List of usernames
        """
        try:
            credentials = self._get_credentials_data()
            return list(credentials.keys())
        except Exception as e:
            Logger.error("UserManager.get_all_users", e)
            return []
    
    def delete_user(self, username):
        """
        Delete a user account and their progression file.
        
        Args:
            username: Username to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            credentials = self._get_credentials_data()
            
            if username not in credentials:
                return False
            
            # Delete from credentials
            del credentials[username]
            self._save_credentials_data(credentials)
            
            # Delete progression file
            filepath = self.get_progression_filepath(username)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            
            Logger.debug("UserManager.delete_user", "User deleted successfully", username=username)
            return True
        except Exception as e:
            Logger.error("UserManager.delete_user", e)
            return False
