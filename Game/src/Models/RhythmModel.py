class RhythmModel:
    """
    Modèle de données pour le Mode Concert (Jeu de Rythme).
    Gère le score, le combo, l'argent et la satisfaction du public (Hype).
    """
    def __init__(self):
        # --- 1. SCORES & COMBO ---
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        
        # --- 2. SYSTÈME DE CONCERT (HYPE) ---
        # Remplace la barre de vie classique.
        # 50  = Public neutre (Début)
        # 100 = Public en délire (Légendaire / Star Power)
        # 0   = Public hostile (Game Over / Tomates)
        self.crowd_satisfaction = 50 
        
        # Argent accumulé (sera calculé par le Controller en fonction du score)
        self.cash_earned = 0
        
        # --- 3. FEEDBACK VISUEL ---
        # Le texte affiché au centre (Perfect, Miss, Excellent...)
        self.feedback = ""
        self.feedback_timer = 0
        
        # --- 4. CONFIGURATION DE LA GRILLE ---
        # Position Y de la ligne de frappe (sera ajusté par le Controller selon l'écran)
        self.hit_line_y = 0 
        
        # Les 4 colonnes correspondant aux touches C, V, B, N
        self.lanes = ["LANE1", "LANE2", "LANE3", "LANE4"]
        
        # La liste des notes (sera remplie par le contrôleur via le SongModel)
        self.notes = []

    def get_crowd_status(self):
        """
        Retourne un texte décrivant l'humeur du public (pour le Debug ou l'UI).
        """
        if self.crowd_satisfaction >= 80:
            return "EN FEU"
        elif self.crowd_satisfaction >= 50:
            return "CONTENT"
        elif self.crowd_satisfaction >= 20:
            return "ENNUYÉ"
        else:
            return "EN COLÈRE"

    def reset(self):
        """Remet les stats à zéro pour recommencer une chanson sans recréer l'objet."""
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.crowd_satisfaction = 50
        self.cash_earned = 0
        self.feedback = ""
        # On réactive les notes pour une nouvelle tentative
        for note in self.notes:
            note["active"] = True