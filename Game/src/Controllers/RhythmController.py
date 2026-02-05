import pygame
import random
import math
from Songs.SevenNationArmy import load_seven_nation_army

class RhythmController:
    """
    Contrôleur principal du MODE CONCERT (Acte 1 & 2).
    NOUVEAU : Système de précision progressive !
    Plus tu es précis, plus tu gagnes de points.
    """
    def __init__(self, rhythm_model, character_model, screen_height, view, context="act1"):
        self.rhythm = rhythm_model
        self.character = character_model 
        self.view = view
        self.context = context  # "act1", "act2", or "rhythm_combat"
        
        # --- 1. INITIALISATION DE LA MAP & AUDIO ---
        self.current_song = load_seven_nation_army()
        self.rhythm.notes = self.current_song.get_notes()
        
        pygame.mixer.init()
        
        # Pistes audio
        self.track_guitar = pygame.mixer.Sound(self.current_song.audio_guitar)
        self.track_backing = pygame.mixer.Sound(self.current_song.audio_backing)
        
        # Channel dédié
        self.guitar_channel = pygame.mixer.Channel(1)
        self.track_guitar.set_volume(1.0)
        self.track_backing.set_volume(1.0)

        # --- 2. CHARGEMENT DES SONS D'ERREUR (SFX) ---
        self.fail_sounds = []
        try:
            for i in range(1, 6):
                sound = pygame.mixer.Sound(f"Game/Assets/Sounds/fail{i}.ogg")
                sound.set_volume(0.6)
                self.fail_sounds.append(sound)
        except FileNotFoundError:
            pass # Pas grave si on ne les a pas

        # --- 3. PARAMÈTRES DE JEU ---
        self.note_speed = 0.5 
        
        # --- 🕒 SYSTÈME DE COMPTE À REBOURS ---
        self.waiting_to_start = True # Le jeu est en pause au début
        self.countdown_duration = 5000 # 5 secondes (5000 ms)
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5

        self.start_time = 0
        self.is_playing = False
        self.game_over = False
        
        # --- 🛡️ PROTECTION AUDIO ---
        self.last_hit_time = -1000 
        
        self.rhythm.hit_line_y = int(screen_height * 0.85)

        # Mapping Clavier -> Colonnes
        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }

    def play_random_fail(self):
        """Joue un 'COUAC' aléatoire."""
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()

    def start_music(self):
        """Lance vraiment la musique après le décompte"""
        self.start_time = pygame.time.get_ticks()
        self.track_backing.play()
        self.guitar_channel.play(self.track_guitar)
        self.is_playing = True

    def update(self):
        """Boucle principale"""
        if self.game_over:
            return 

        # --- 1. GESTION DU COMPTE À REBOURS ---
        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            # Calcul du chiffre à afficher (5, 4, 3...)
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            # NOUVEAU : Les notes descendent PENDANT le compte à rebours
            # On simule un temps négatif pour qu'elles arrivent pile quand la musique démarre
            fake_time = -remaining  # Ex: remaining=3000ms → fake_time=-3000ms
            
            for note in self.rhythm.notes:
                if note["active"]:
                    time_diff = note["time"] - fake_time
                    note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)
            
            if remaining <= 0:
                self.waiting_to_start = False
                self.start_music() # GO !
            
            return  # On ne fait que ça pendant le décompte

        # --- 2. JEU NORMAL ---
        if not self.is_playing:
            self.start_music()

        current_time = pygame.time.get_ticks() - self.start_time

        # Timer du texte Feedback
        if self.rhythm.feedback_timer > 0:
            self.rhythm.feedback_timer -= 1
        else:
            self.rhythm.feedback = ""

        # --- MISE À JOUR DES NOTES ---
        for note in self.rhythm.notes:
            if note["active"]:
                # Calcul Y
                time_diff = note["time"] - current_time
                note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)

                # --- DÉTECTION MISS (Sortie écran) ---
                if note["y"] > self.rhythm.hit_line_y + 100:
                    note["active"] = False
                    self.trigger_miss()

    def trigger_miss(self):
        """PUNITION SÉVÈRE : Le public te déteste"""
        current_real_time = pygame.time.get_ticks()
        
        # Protection Audio
        if current_real_time - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0) 
            self.play_random_fail()

        # Pénalités
        self.rhythm.feedback = "MISS!"
        self.rhythm.feedback_timer = 30
        self.rhythm.score = max(0, self.rhythm.score - 50) # Grosse perte de score
        self.rhythm.combo = 0
        
        # --- 📉 HARDCORE : GROSSE PERTE DE HYPE (-8) ---
        self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 8)
        
        # GAME OVER
        if self.rhythm.crowd_satisfaction <= 0:
            self.game_over = True
            print("GAME OVER : Le public vous a dégagé !")
            self.guitar_channel.stop()
            self.track_backing.stop()

    def handle_input(self, event):
        # On bloque les touches pendant le décompte
        if self.waiting_to_start or self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.check_hit(lane)

    def check_hit(self, lane):
        current_time = pygame.time.get_ticks() - self.start_time
        
        # --- SYSTÈME DE PRÉCISION PROGRESSIVE ---
        # Plus tu es proche du centre, plus tu gagnes !
        # On définit plusieurs zones de tolérance :
        
        perfect_window = 50      # ±50ms = PARFAIT (zone très étroite)
        excellent_window = 100   # ±100ms = EXCELLENT (zone étroite)
        good_window = 150        # ±150ms = BIEN (zone normale)
        ok_window = 200          # ±200ms = OK (zone large)
        miss_window = 250        # ±250ms = Dernière chance (pénalité)
        
        hit_found = False
        best_note = None
        best_distance = float('inf')

        # Trouver la note la plus proche dans cette lane
        for note in self.rhythm.notes:
            if note["active"] and note["lane"] == lane:
                time_diff = abs(note["time"] - current_time)
                
                # Chercher la note la plus proche (pour éviter de toucher la mauvaise)
                if time_diff < best_distance and time_diff < miss_window:
                    best_distance = time_diff
                    best_note = note
        
        if best_note:
            # On a trouvé une note touchable
            hit_found = True
            best_note["active"] = False
            
            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()
            
            # --- CALCUL DES POINTS SELON LA PRÉCISION ---
            # Plus on est proche de 0ms, plus on gagne !
            
            if best_distance <= perfect_window:
                # PERFECT : ±50ms
                # Points : 300 (base élevée)
                # Hype : +5 (grosse récompense)
                points = 300
                hype_gain = 5
                feedback = "PERFECT!"
                particle_color = (255, 255, 0)  # Jaune éclatant
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= excellent_window:
                # EXCELLENT : ±100ms
                # Points : 150-300 - on perd des points progressivement
                # Formule : 300 - (distance * 1.5)
                # Ex: à 50ms → 300-75=225, à 100ms → 300-150=150
                points = max(150, int(300 - best_distance * 1.5))
                hype_gain = 3
                feedback = "EXCELLENT!"
                particle_color = (100, 255, 255)  # Cyan
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= good_window:
                # GOOD : ±150ms
                # Points : 80-150 selon précision
                # Formule : 200 - distance
                # Ex: à 100ms → 200-100=100, à 150ms → 200-150=50
                points = max(80, int(200 - best_distance))
                hype_gain = 2
                feedback = "GOOD"
                particle_color = (50, 255, 50)  # Vert
                
            elif best_distance <= ok_window:
                # OK : ±200ms
                # Points : 30-80 selon précision
                # Formule : 120 - (distance * 0.5)
                # Ex: à 150ms → 120-75=45, à 200ms → 120-100=20
                points = max(30, int(120 - best_distance * 0.5))
                hype_gain = 1
                feedback = "OK"
                particle_color = (255, 200, 100)  # Orange pâle
                
            else:
                # LATE/EARLY : ±250ms (dernière chance)
                # Points : 5-30 (très peu)
                # Hype : 0 (aucun gain)
                # On garde le combo mais c'est la honte
                points = max(5, int(40 - best_distance * 0.1))
                hype_gain = 0
                feedback = "LATE!" if (best_note["time"] - current_time) < 0 else "EARLY!"
                particle_color = (150, 150, 150)  # Gris
            
            # Appliquer les gains
            self.register_hit(points, feedback, hype_gain)
            
        else:
            # --- MISS TOTAL ---
            # Aucune note dans la fenêtre = GROSSE PUNITION
            self.rhythm.feedback = "MISS!"
            self.rhythm.feedback_timer = 30
            self.rhythm.score = max(0, self.rhythm.score - 20)  # Perte de points
            self.rhythm.combo = 0  # Reset combo
            self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 5)  # Perte de hype
            self.play_random_fail()

    def register_hit(self, points, text, hype_gain):
        """Applique les gains avec multiplicateur de combo"""
        self.rhythm.feedback = text
        self.rhythm.feedback_timer = 20
        self.rhythm.combo += 1
        
        # Multiplicateur de score basé sur le combo
        # Ex: Combo 10 = x1.5, Combo 20 = x2.0
        multiplier = 1 + (self.rhythm.combo // 10) * 0.5 
        final_points = int(points * multiplier)
        
        self.rhythm.score += final_points
        
        # Gain de Hype (plafonné à 100)
        self.rhythm.crowd_satisfaction = min(100, self.rhythm.crowd_satisfaction + hype_gain)
        
        # Debug pour voir l'effet de la précision
        if self.rhythm.combo % 10 == 0:  # Affiche tous les 10 combos
            print(f"Combo x{self.rhythm.combo} | Score: {self.rhythm.score} | Hype: {self.rhythm.crowd_satisfaction}%")

    def end_concert(self):
        """
        Calculate and award cash based on context, player level, and performance.
        
        Base rewards:
        - Act 1: $100 at level 0
        - Act 2: $150 at level 0 (1.5x Act 1)
        - Rhythm Combat: $250 at level 0 (2.5x Act 1)
        
        All scale by (player_level + 1)
        """
        try:
            player_level = self.character.getLevel() if self.character else 0
            level_multiplier = player_level + 1  # Level 0 = 1x, Level 1 = 2x, etc.
            
            # Determine base reward by context
            if self.context == "rhythm_combat":
                base_reward = 250  # Final boss pays the most
            elif self.context == "act2":
                base_reward = 150  # Act 2 medium reward
            else:  # Default to "act1"
                base_reward = 100  # Act 1 beginner reward
            
            # Apply level scaling
            base_cash = int(base_reward * level_multiplier)
            
            # Bonus for excellent performance (satisfaction > 90)
            bonus_cash = 0
            if self.rhythm.crowd_satisfaction > 90:
                # 20% bonus for really good crowd
                bonus_cash = int(base_cash * 0.20)
            
            # Final cash
            cash = base_cash + bonus_cash
            
            self.rhythm.cash_earned = cash
            
            # Award currency to player
            if self.character:
                self.character.addCurrency(cash)
            
            # Debug output
            print(f"=== CONCERT COMPLETE ===")
            print(f"Context: {self.context} | Player Level: {player_level}")
            print(f"Base Reward: ${base_reward} × {level_multiplier} (level multiplier) = ${base_cash}")
            print(f"Crowd Satisfaction: {self.rhythm.crowd_satisfaction}%")
            if bonus_cash > 0:
                print(f"Performance Bonus: +${bonus_cash} (20% for satisfaction > 90%)")
            print(f"Total Earnings: ${cash}")
            if self.character:
                print(f"Player Total Currency: ${self.character.getCurrency()}")
            print(f"Stats:")
            print(f"   Score: {self.rhythm.score}")
            print(f"   Max Combo: {self.rhythm.max_combo}")
            print(f"   Final Hype: {self.rhythm.crowd_satisfaction}%")
            
            return cash
        except Exception as e:
            print(f"ERROR in end_concert: {e}")
            self.rhythm.cash_earned = 0
            return 0

    def get_lane_x(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.lane_x[idx]