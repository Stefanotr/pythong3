import pygame
import random
import math

# ❌ PLUS D'IMPORT DE CHANSON ICI (Le contrôleur attend qu'on lui donne la musique)

class RhythmController:
    """
    Contrôleur principal du MODE CONCERT (Acte 1 & 2).
    🎯 NOUVEAU : Système de précision progressive !
    Plus tu es précis, plus tu gagnes de points.
    """
    # 🆕 MODIFICATION : On ajoute 'song_data' dans les paramètres
    
    def __init__(self, rhythm_model, character_model, screen_height, view,song_data, context="act1"):
        self.rhythm = rhythm_model
        self.character = character_model 
        self.view = view
        self.context = context  # "act1", "act2", or "rhythm_combat"
        
        # --- 1. INITIALISATION DE LA MAP & AUDIO ---
        # On utilise la chanson reçue en paramètre
        self.current_song = song_data
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
        
        # --- 🎵 FIN DE CHANSON & ÉCRAN DE FIN ---
        self.song_finished = False  # True quand la musique est terminée
        self.finish_time = 0  # Quand la musique s'est terminée
        self.finish_delay = 5000  # 5 secondes avant auto-continue
        self.continue_pressed = False  # True si le joueur a cliqué sur "Continuer"
        
        # --- 🔒 PAUSE ---
        self.is_paused = False
        self.pause_time = 0  # Temps quand on a mis en pause
        self.pause_music_position = 0  # Position de la musique quand en pause
        
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
        
        # Initialize 'y' key for all notes to avoid KeyError
        for note in self.rhythm.notes:
            note["y"] = self.rhythm.hit_line_y

    def playRandomFail(self):
        """Play a random failure sound (SFX for missed notes)."""
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()

    def stop_all_audio(self):
        """Arrête tous les sons du jeu"""
        try:
            self.guitar_channel.stop()
            self.track_backing.stop()
            self.track_guitar.stop()
            # Arrêter tous les fail_sounds
            for sound in self.fail_sounds:
                sound.stop()
        except Exception as e:
            print(f"Erreur en arrêtant les audios: {e}")

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
        
        # Gérer la pause avec décompte
        if self.is_paused:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            if remaining <= 0:
                # Fin du décompte, reprendre la musique
                self.is_paused = False
                self.waiting_to_start = False
                # Unpause et recalculer le start_time
                pygame.mixer.unpause()
                pause_duration = pygame.time.get_ticks() - self.pause_time
                self.start_time += pause_duration  # Décaler start_time de la durée de la pause
                print("▶️ Reprise!")
            return

        # --- 1. GESTION DU COMPTE À REBOURS ---
        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            # Calcul du chiffre à afficher (5, 4, 3...)
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            # 🎵 Les notes descendent PENDANT le compte à rebours
            fake_time = -remaining
            
            for note in self.rhythm.notes:
                if note["active"]:
                    time_diff = note["time"] - fake_time
                    note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)
            
            if remaining <= 0:
                self.waiting_to_start = False
                self.startMusic()
            
            return

        # --- 2. JEU NORMAL ---
        if not self.is_playing:
            self.startMusic()

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
                    self.triggerMiss()
        
        # --- VÉRIFICATION FIN DE CHANSON ---
        self.checkSongFinished()
        
        # Auto-continue quand le timeout de 5 secondes est écoulé
        if self.song_finished and not self.continue_pressed:
            if self.get_auto_continue_remaining() <= 0:
                self.continue_pressed = True
        
        # Si continuer a été pressé, on arrête le jeu
        if self.continue_pressed:
            self.game_over = True

    def triggerMiss(self):
        """Handle a missed note - apply penalties to score, combo, and crowd satisfaction."""
        current_real_time = pygame.time.get_ticks()
        
        # Protection Audio
        if current_real_time - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0) 
            self.playRandomFail()

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
            self.stop_all_audio()

    def handleInput(self, event):
        # Gestion de la pause (ESC) - disponible même si le jeu a commencé
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self.waiting_to_start and self.is_playing and not self.game_over and not self.song_finished:
                self.togglePause()
            return
        
        # Gestion du bouton "Continuer" sur l'écran de fin (SPACE ou clic)
        if self.song_finished and not self.continue_pressed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.continue_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.continue_pressed = True
            return
        
        # On bloque les touches pendant le décompte, la pause, et après fin
        if self.waiting_to_start or self.game_over or self.is_paused or self.song_finished:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.checkHit(lane)

    # Backward compatible alias
    def handle_input(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handleInput(event)

    def checkHit(self, lane):
        current_time = pygame.time.get_ticks() - self.start_time
        
        # --- 🎯 SYSTÈME DE PRÉCISION PROGRESSIVE ---
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
            
            # --- 🎯 CALCUL DES POINTS SELON LA PRÉCISION ---
            # Plus on est proche de 0ms, plus on gagne !
            
            if best_distance <= perfect_window:
                # 🌟 PERFECT : ±50ms
                # Points : 300 (base élevée)
                # Hype : +5 (grosse récompense)
                points = 300
                hype_gain = 5
                feedback = "PERFECT! ⭐"
                particle_color = (255, 255, 0)  # Jaune éclatant
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= excellent_window:
                # ✨ EXCELLENT : ±100ms
                # Points : 150-300 - on perd des points progressivement
                # Formule : 300 - (distance * 1.5)
                # Ex: à 50ms → 300-75=225, à 100ms → 300-150=150
                points = max(150, int(300 - best_distance * 1.5))
                hype_gain = 3
                feedback = "EXCELLENT! ✨"
                particle_color = (100, 255, 255)  # Cyan
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= good_window:
                # 👍 GOOD : ±150ms
                # Points : 80-150 selon précision
                # Formule : 200 - distance
                # Ex: à 100ms → 200-100=100, à 150ms → 200-150=50
                points = max(80, int(200 - best_distance))
                hype_gain = 2
                feedback = "GOOD 👍"
                particle_color = (50, 255, 50)  # Vert
                
            elif best_distance <= ok_window:
                # 😐 OK : ±200ms
                # Points : 30-80 selon précision
                # Formule : 120 - (distance * 0.5)
                # Ex: à 150ms → 120-75=45, à 200ms → 120-100=20
                points = max(30, int(120 - best_distance * 0.5))
                hype_gain = 1
                feedback = "OK 😐"
                particle_color = (255, 200, 100)  # Orange pâle
                
            else:
                # 💩 LATE/EARLY : ±250ms (dernière chance)
                # Points : 5-30 (très peu)
                # Hype : 0 (aucun gain)
                # On garde le combo mais c'est la honte
                points = max(5, int(40 - best_distance * 0.1))
                hype_gain = 0
                feedback = "LATE! 💩" if (best_note["time"] - current_time) < 0 else "EARLY! 💩"
                particle_color = (150, 150, 150)  # Gris
            
            # Appliquer les gains
            self.registerHit(points, feedback, hype_gain)
            
        else:
            # --- ❌ MISS TOTAL ---
            # Aucune note dans la fenêtre = GROSSE PUNITION
            self.rhythm.feedback = "MISS! ❌"
            self.rhythm.feedback_timer = 30
            self.rhythm.score = max(0, self.rhythm.score - 20)  # Perte de points
            self.rhythm.combo = 0  # Reset combo
            self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 5)  # Perte de hype
            self.playRandomFail()

    def registerHit(self, points, text, hype_gain):
        """Apply hit rewards with combo multiplier to score and crowd satisfaction."""
        self.rhythm.feedback = text
        self.rhythm.feedback_timer = 20
        self.rhythm.combo += 1
        self.rhythm.total_hits += 1  # Incrémenter le compteur de bonnes notes
        
        # Multiplicateur de score basé sur le combo
        # Ex: Combo 10 = x1.5, Combo 20 = x2.0
        multiplier = 1 + (self.rhythm.combo // 10) * 0.5 
        final_points = int(points * multiplier)
        
        self.rhythm.score += final_points
        
        # Gain de Hype (plafonné à 100)
        self.rhythm.crowd_satisfaction = min(100, self.rhythm.crowd_satisfaction + hype_gain)
        
        # Debug pour voir l'effet de la précision
        if self.rhythm.combo % 10 == 0:  # Affiche tous les 10 combos
            print(f"🎯 Combo x{self.rhythm.combo} | Score: {self.rhythm.score} | Hype: {self.rhythm.crowd_satisfaction}%")
    def togglePause(self):
        """Toggle pause state and pause/resume audio tracks."""
        if self.is_paused:
            # Reprendre
            self.resume_pause()
        else:
            # Mettre en pause
            self.is_paused = True
            self.pause_time = pygame.time.get_ticks()
            # Pause les deux pistes audio
            pygame.mixer.pause()
            print("⏸️ PAUSE")

    def resume_pause(self):
        """Reprendre après une pause - avec décompte de 5s"""
        self.is_paused = False
        # Redémarrer le décompte
        self.waiting_to_start = True
        self.countdown_duration = 5000
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5
        # Pause toujours la musique (on va l'unpause après le décompte)
        pygame.mixer.pause()
        print("⏱️ Décompte avant reprise: 5s")

    def checkSongFinished(self):
        """Check if the song has finished by comparing current time with last note end time."""
        if self.is_playing and not self.song_finished:
            current_time = pygame.time.get_ticks() - self.start_time
            
            # Calculate song duration from the last note's end time
            if self.rhythm.notes:
                # Find the note that ends latest (time + duration)
                last_note_end = max(note["time"] + note["duration"] for note in self.rhythm.notes)
                # Add a small buffer to ensure the note fully completes
                song_duration = last_note_end + 500  # 500ms buffer
            else:
                # Fallback to old hardcoded duration if no notes
                song_duration = 13000
            
            if current_time >= song_duration:
                self.song_finished = True
                self.finish_time = pygame.time.get_ticks()
                pygame.mixer.stop()
                print("🎵 Chanson terminée!")
    
    def get_auto_continue_remaining(self):
        """Retourner le temps restant avant auto-continue (en secondes)"""
        if not self.song_finished:
            return 0
        elapsed = pygame.time.get_ticks() - self.finish_time
        remaining_ms = self.finish_delay - elapsed
        remaining_s = max(0, remaining_ms // 1000)
        return remaining_s
    def end_concert(self):
        """
        Calculate and award cash based on context, player level, and performance.
        
        Base rewards per hit:
        - Act 1: 1$ per hit
        - Act 2: 1$ per hit (same as Act 1)
        - Rhythm Combat: 2$ per hit (2x multiplier)
        
        All scale by (player_level + 1)
        """
        try:
            player_level = self.character.getLevel() if self.character else 0
            level_multiplier = player_level + 1  # Level 0 = 1x, Level 1 = 2x, etc.
            
            # Determine cash per hit by context
            if self.context == "rhythm_combat":
                cash_per_hit = 2  # Boss combat pays 2$ per hit
            else:  # "act1" or "act2"
                cash_per_hit = 1  # Regular concerts pay 1$ per hit
            
            # Calculate total cash based on total hits
            total_hits = getattr(self.rhythm, 'total_hits', 0)
            base_cash = total_hits * cash_per_hit * level_multiplier
            
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
            print(f"Total Hits: {total_hits} × ${cash_per_hit} × {level_multiplier} (level multiplier) = ${base_cash}")
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

    # Backward compatible aliases for old function names
    def play_random_fail(self):
        """Legacy alias."""
        return self.playRandomFail()
    
    def start_music(self):
        """Legacy alias."""
        return self.startMusic()
    
    def trigger_miss(self):
        """Legacy alias."""
        return self.triggerMiss()
    
    def check_hit(self, lane):
        """Legacy alias."""
        return self.checkHit(lane)
    
    def register_hit(self, points, text, hype_gain):
        """Legacy alias."""
        return self.registerHit(points, text, hype_gain)
    
    def toggle_pause(self):
        """Legacy alias."""
        return self.togglePause()
    
    def check_song_finished(self):
        """Legacy alias."""
        return self.checkSongFinished()
    
    def get_lane_x(self, lane):
        """Legacy alias."""
        return self.getLaneX(lane)

    def getLaneX(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.lane_x[idx]