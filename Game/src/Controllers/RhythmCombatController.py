import pygame
import random
import math
from Songs.SevenNationArmy import load_seven_nation_army

class RhythmCombatController:
    """
    # MODE COMBAT RHYTHM - BOSS FINAL
    
    Combine le jeu de rythme avec le combat :
    - Bonnes notes → Dégâts au BOSS
    - Mauvaises notes / Miss → Dégâts au JOUEUR + Vie du boss augmente
    - Game Over si le boss a encore de la vie à la fin OU si le joueur meurt
    """
    def __init__(self, rhythm_model, player_model, boss_model, screen_height, view, song_loader=None):
        self.rhythm = rhythm_model
        self.player = player_model
        self.boss = boss_model
        self.view = view
        
        # Store boss max health for healing calculations
        self.boss_max_health = getattr(self.boss, '_rhythm_combat_max_health', self.boss.getHealth())
        
        # --- 1. INITIALISATION DE LA MAP & AUDIO ---
        if song_loader is None:
            song_loader = load_seven_nation_army
        
        self.current_song = song_loader()
        self.rhythm.notes = self.current_song.get_notes()
        
        # Initialiser les positions Y des notes
        for note in self.rhythm.notes:
            note["y"] = -1000
        
        pygame.mixer.init()
        
        # Pistes audio
        self.track_guitar = pygame.mixer.Sound(self.current_song.audio_guitar)
        self.track_backing = pygame.mixer.Sound(self.current_song.audio_backing)
        
        # Channel dédié
        self.guitar_channel = pygame.mixer.Channel(1)
        self.track_guitar.set_volume(1.0)
        self.track_backing.set_volume(1.0)

        # --- 2. SONS ---
        self.fail_sounds = []
        self.hit_sounds = []
        
        try:
            for i in range(1, 6):
                fail = pygame.mixer.Sound(f"Game/Assets/Sounds/fail{i}.ogg")
                fail.set_volume(0.6)
                self.fail_sounds.append(fail)
        except FileNotFoundError:
            pass
        
        # TODO: Ajouter des sons de coups pour les hits
        # try:
        #     for i in range(1, 4):
        #         hit = pygame.mixer.Sound(f"Game/Assets/Sounds/hit{i}.ogg")
        #         hit.set_volume(0.7)
        #         self.hit_sounds.append(hit)
        # except FileNotFoundError:
        #     pass

        # --- 3. PARAMÈTRES DE JEU ---
        self.note_speed = 0.5
        
        # --- 🕒 COMPTE À REBOURS ---
        self.waiting_to_start = True
        self.countdown_duration = 5000
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5

        self.start_time = 0
        self.is_playing = False
        self.game_over = False
        self.victory = False  # True si boss vaincu
        
        # --- 🛡️ PROTECTION AUDIO ---
        self.last_hit_time = -1000
        
        self.rhythm.hit_line_y = int(screen_height * 0.85)

        # Mapping Clavier
        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }
        
        # --- STATS DE COMBAT ---
        self.total_notes = len([n for n in self.rhythm.notes if n.get("active", True)])
        self.notes_hit = 0
        self.notes_missed = 0
        
        print(f"MODE COMBAT RHYTHM")
        print(f"Boss: {self.boss.getName()} (HP: {self.boss.getHealth()})")
        print(f"Player: {self.player.getName()} (HP: {self.player.getHealth()})")
        print(f"Total notes: {self.total_notes}")

    def play_random_fail(self):
        """Joue un couac"""
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()
    
    def play_random_hit(self):
        """Joue un son de coup"""
        if self.hit_sounds:
            sound = random.choice(self.hit_sounds)
            sound.play()

    def start_music(self):
        """Lance la musique"""
        self.start_time = pygame.time.get_ticks()
        self.track_backing.play()
        self.guitar_channel.play(self.track_guitar)
        self.is_playing = True
        print("Musique lancée - LE COMBAT COMMENCE !")

    def update(self):
        """Boucle principale"""
        if self.game_over:
            return
        
        # === CHECK PLAYER DEATH AT START ===
        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            print(f"GAME OVER : {self.player.getName()} est K.O. !")
            self.guitar_channel.stop()
            self.track_backing.stop()
            return

        # --- 1. COMPTE À REBOURS ---
        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            # Les notes descendent pendant le décompte
            fake_time = -remaining
            
            for note in self.rhythm.notes:
                if note["active"]:
                    time_diff = note["time"] - fake_time
                    note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)
            
            if remaining <= 0:
                self.waiting_to_start = False
                self.start_music()
            
            return

        # --- 2. JEU NORMAL ---
        if not self.is_playing:
            self.start_music()

        current_time = pygame.time.get_ticks() - self.start_time

        # Timer feedback
        if self.rhythm.feedback_timer > 0:
            self.rhythm.feedback_timer -= 1
        else:
            self.rhythm.feedback = ""

        # --- MISE À JOUR DES NOTES ---
        notes_remaining = False
        for note in self.rhythm.notes:
            if note["active"]:
                notes_remaining = True
                time_diff = note["time"] - current_time
                note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)

                # MISS (sortie écran)
                if note["y"] > self.rhythm.hit_line_y + 100:
                    note["active"] = False
                    self.trigger_miss()
        
        # --- FIN DE LA CHANSON ---
        if not notes_remaining and self.is_playing:
            self.end_combat()

    def trigger_miss(self):
        """
        MISS : Le joueur prend des dégâts ET le boss récupère de la vie
        """
        current_real_time = pygame.time.get_ticks()
        
        # Protection Audio
        if current_real_time - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0)
            self.play_random_fail()

        # Stats
        self.notes_missed += 1
        
        # Feedback
        self.rhythm.feedback = "MISS!"
        self.rhythm.feedback_timer = 30
        self.rhythm.combo = 0
        
        # --- DÉGÂTS AU JOUEUR ---
        damage_to_player = 10  # Le boss contre-attaque !
        current_hp = self.player.getHealth()
        self.player.setHealth(max(0, current_hp - damage_to_player))
        
        print(f"MISS → {self.player.getName()} prend {damage_to_player} dégâts ! (HP: {self.player.getHealth()})")
        
        # --- LE BOSS RÉCUPÈRE DE LA VIE ---
        boss_heal = 5
        boss_hp = self.boss.getHealth()
        self.boss.setHealth(min(self.boss_max_health, boss_hp + boss_heal))
        
        print(f"Le boss récupère {boss_heal} HP ! (HP: {self.boss.getHealth()})")
        
        # GAME OVER si le joueur meurt
        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            print(f"GAME OVER : {self.player.getName()} est K.O. !")
            self.guitar_channel.stop()
            self.track_backing.stop()

    def handle_input(self, event):
        """Gère les inputs"""
        if self.waiting_to_start or self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.check_hit(lane)

    def check_hit(self, lane):
        """Détecte les hits avec système de précision"""
        current_time = pygame.time.get_ticks() - self.start_time
        
        # Zones de précision
        perfect_window = 50
        excellent_window = 100
        good_window = 150
        ok_window = 200
        miss_window = 250
        
        hit_found = False
        best_note = None
        best_distance = float('inf')

        # Trouver la note la plus proche
        for note in self.rhythm.notes:
            if note["active"] and note["lane"] == lane:
                time_diff = abs(note["time"] - current_time)
                
                if time_diff < best_distance and time_diff < miss_window:
                    best_distance = time_diff
                    best_note = note
        
        if best_note:
            hit_found = True
            best_note["active"] = False
            self.notes_hit += 1
            
            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()
            
            # --- CALCUL DES DÉGÂTS AU BOSS ---
            base_damage = 0
            
            if best_distance <= perfect_window:
                base_damage = 15  # GROS dégâts
                feedback = "PERFECT!"
                particle_color = (255, 255, 0)
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= excellent_window:
                base_damage = 12  # Bons dégâts
                feedback = "EXCELLENT!"
                particle_color = (100, 255, 255)
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= good_window:
                base_damage = 8  # Dégâts normaux
                feedback = "GOOD"
                
            elif best_distance <= ok_window:
                base_damage = 5  # Petits dégâts
                feedback = "OK"
                
            else:
                base_damage = 2  # Dégâts minimes
                feedback = "LATE!" if (best_note["time"] - current_time) < 0 else "EARLY!"
            
            # Appliquer les dégâts au boss
            self.deal_damage_to_boss(base_damage, feedback)
            
        else:
            # Taper dans le vide = petit malus
            self.rhythm.combo = 0
            self.play_random_fail()
            
            # Petit dégât au joueur (moins que MISS)
            damage = 3
            current_hp = self.player.getHealth()
            self.player.setHealth(max(0, current_hp - damage))
            
            if self.player.getHealth() <= 0:
                self.game_over = True
                self.victory = False

    def deal_damage_to_boss(self, damage, feedback):
        """Inflige des dégâts au boss"""
        # Combo bonus
        self.rhythm.combo += 1
        combo_multiplier = 1 + (self.rhythm.combo // 5) * 0.2  # +20% tous les 5 combos
        final_damage = int(damage * combo_multiplier)

        # --- DRUNKENNESS ONLY AFFECTS DAMAGE OUTPUT, NOT HIT/MISS ---
        try:
            drunkenness = self.player.getDrunkenness()
        except Exception:
            drunkenness = 0
        
        # At high drunkenness: slight damage reduction (harder to aim well)
        # But if very drunk (50%+), the hits that DO connect are more powerful (aggression)
        drunkenness_damage_penalty = int((drunkenness / 100) * 20)  # -0 to -20% damage from poor aim
        final_damage = max(1, final_damage - drunkenness_damage_penalty)
        
        # Very drunk hits (50%+) get a small bonus (reckless aggression)
        if drunkenness >= 50:
            final_damage = int(final_damage * 1.2)

        # === RHYTHM COMBAT DAMAGE REDUCTION ===
        # Divide damage by 2 for rhythm combat balance
        final_damage = final_damage // 2  # Integer division to cut damage in half
        
        # Appliquer dégâts
        boss_hp = self.boss.getHealth()
        new_boss_hp = max(0, boss_hp - final_damage)
        self.boss.setHealth(new_boss_hp)
        
        # Debug logging
        from Utils.Logger import Logger
        Logger.debug("RhythmCombatController.deal_damage_to_boss", 
                    f"Boss health: {boss_hp} -> {new_boss_hp} ({feedback})", 
                    damage=final_damage)
        
        # Set feedback (just the rating, combo will be displayed below)
        self.rhythm.feedback = feedback
        self.rhythm.feedback_timer = 20
        
        # Son
        self.play_random_hit()
        
        # Vérifier si boss vaincu
        if self.boss.getHealth() <= 0:
            self.victory = True
            self.game_over = True
            print(f"VICTOIRE ! {self.boss.getName()} est vaincu !")
            self.guitar_channel.stop()
            self.track_backing.stop()

    def end_combat(self):
        """Fin de la chanson - Déterminer victoire/défaite"""
        self.game_over = True
        
        if self.boss.getHealth() > 0:
            # Le boss a survécu = Défaite
            self.victory = False
            print(f"DÉFAITE : {self.boss.getName()} a survécu avec {self.boss.getHealth()} HP !")
        else:
            # Boss vaincu = Victoire
            self.victory = True
            print(f"VICTOIRE : {self.boss.getName()} vaincu !")
        
        # Stats finales
        print(f"STATS FINALES :")
        print(f"   Notes touchées : {self.notes_hit}/{self.total_notes}")
        print(f"   Notes ratées : {self.notes_missed}")
        print(f"   Combo max : {self.rhythm.combo}")
        print(f"   HP Joueur : {self.player.getHealth()}")
        print(f"   HP Boss : {self.boss.getHealth()}")
        
        self.guitar_channel.stop()
        self.track_backing.stop()

    def get_lane_x(self, lane):
        """Retourne la position X d'une lane"""
        idx = self.rhythm.lanes.index(lane)
        return self.view.lane_x[idx]