import pygame
import random
import math
from Songs.TheFinalCountdown import loadFinalCountdown
from Utils.Logger import Logger

class RhythmCombatController:

    def __init__(self, rhythm_model, player_model, boss_model, screen_height, view, song_loader=loadFinalCountdown()):
        self.rhythm = rhythm_model
        self.player = player_model
        self.boss = boss_model
        self.view = view
        self.context = "rhythm_combat"

        self.boss_max_health = getattr(self.boss, '_rhythm_combat_max_health', self.boss.getHealth())

        if song_loader is None:
            song_loader = loadFinalCountdown()

        self.current_song = song_loader
        self.rhythm.notes = self.current_song.get_notes()

        for note in self.rhythm.notes:
            note["y"] = -1000

        pygame.mixer.init()

        self.track_guitar = pygame.mixer.Sound(self.current_song.audio_guitar)
        self.track_backing = pygame.mixer.Sound(self.current_song.audio_backing)

        self.guitar_channel = pygame.mixer.Channel(1)
        self.track_guitar.set_volume(1.0)
        self.track_backing.set_volume(1.0)

        self.fail_sounds = []
        self.hit_sounds = []

        try:
            for i in range(1, 6):
                fail = pygame.mixer.Sound(f"Game/Assets/Sounds/fail{i}.ogg")
                fail.set_volume(0.6)
                self.fail_sounds.append(fail)
        except FileNotFoundError:
            pass

        self.note_speed = 0.5

        self.waiting_to_start = True
        self.countdown_duration = 5000
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5
        self.is_paused = False

        self.start_time = 0
        self.is_playing = False
        self.game_over = False
        self.victory = False

        self.last_hit_time = -1000

        self.rhythm.hit_line_y = int(screen_height * 0.85)

        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }

        self.total_notes = len([n for n in self.rhythm.notes if n.get("active", True)])
        self.notes_hit = 0
        self.notes_missed = 0

        Logger.debug("RhythmCombatController.__init__", "MODE COMBAT RHYTHM", boss=self.boss.getName(), player=self.player.getName(), totalNotes=self.total_notes)

    def playRandomFail(self):
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()

    def playRandomHit(self):
        if self.hit_sounds:
            sound = random.choice(self.hit_sounds)
            sound.play()

    def stopAllAudio(self):
        try:
            self.guitar_channel.stop()
            self.track_backing.stop()
            self.track_guitar.stop()
            for sound in self.fail_sounds:
                sound.stop()
            for sound in self.hit_sounds:
                sound.stop()
        except Exception as e:
            Logger.error("RhythmCombatController.stopAllAudio", e)

    def pauseAudio(self):
        try:
            self.stored_guitar_volume = self.guitar_channel.get_volume()
            self.guitar_channel.set_volume(0)
            if self.track_backing:
                self.track_backing.set_volume(0)
        except Exception as e:
            Logger.error("RhythmCombatController.pauseAudio", e)

    def resumeAudio(self):
        try:
            if hasattr(self, 'stored_guitar_volume'):
                self.guitar_channel.set_volume(self.stored_guitar_volume)
            else:
                self.guitar_channel.set_volume(1.0)
            if self.track_backing:
                self.track_backing.set_volume(1.0)
        except Exception as e:
            Logger.error("RhythmCombatController.resumeAudio", e)

    def startMusic(self):
        self.start_time = pygame.time.get_ticks()
        self.track_backing.play()
        self.guitar_channel.play(self.track_guitar)
        self.is_playing = True
        Logger.debug("RhythmCombatController.startMusic", "Combat music started")

    def update(self):
        if self.game_over or self.is_paused:
            return

        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            Logger.debug("RhythmCombatController.update", "Game over - player KO")
            self.stopAllAudio()
            return

        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed

            self.current_countdown_val = math.ceil(remaining / 1000)

            if remaining <= 0:
                self.waiting_to_start = False
                self.startMusic()

            return

        if not self.is_playing:
            self.startMusic()

        currentTime = pygame.time.get_ticks() - self.startTime

        if self.rhythm.feedbackTimer > 0:
            self.rhythm.feedbackTimer -= 1
        else:
            self.rhythm.feedback = ""

        notesRemaining = False
        for note in self.rhythm.notes:
            if note["active"]:
                notesRemaining = True
                timeDiff = note["time"] - currentTime
                note["y"] = self.rhythm.hitLineY - (timeDiff * self.noteSpeed)

                if note["y"] > self.rhythm.hitLineY + 100:
                    note["active"] = False
                    self.triggerMiss()

        if not notesRemaining and self.is_playing:
            self.endCombat()

    def triggerMiss(self):
        currentRealTime = pygame.time.get_ticks()

        if currentRealTime - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0)
            self.playRandomFail()

        self.notes_missed += 1

        self.rhythm.feedback = "MISS!"
        self.rhythm.feedbackTimer = 30
        self.rhythm.combo = 0

        damageToPlayer = 10
        currentHp = self.player.getHealth()
        self.player.setHealth(max(0, currentHp - damageToPlayer))

        self.boss.setCurrentAction("attacking", 30)

        Logger.debug("RhythmCombatController.triggerMiss", "Player took damage", damage=damageToPlayer, playerHp=self.player.getHealth())

        bossHeal = 5
        bossHp = self.boss.getHealth()
        self.boss.setHealth(min(self.boss_max_health, bossHp + bossHeal))

        Logger.debug("RhythmCombatController.triggerMiss", "Boss healed", heal=bossHeal, bossHp=self.boss.getHealth())

        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            Logger.debug("RhythmCombatController.triggerMiss", "Game over - player KO")
            self.guitar_channel.stop()
            self.track_backing.stop()

    def handleInput(self, event):
        if self.waiting_to_start or self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.checkHit(lane)

    def checkHit(self, lane):
        currentTime = pygame.time.get_ticks() - self.start_time

        perfectWindow = 50
        excellentWindow = 100
        goodWindow = 150
        okWindow = 200
        missWindow = 250

        hitFound = False
        bestNote = None
        bestDistance = float('inf')

        for note in self.rhythm.notes:
            if note["active"] and note["lane"] == lane:
                timeDiff = abs(note["time"] - currentTime)

                if timeDiff < bestDistance and timeDiff < missWindow:
                    bestDistance = timeDiff
                    bestNote = note

        if bestNote:
            hitFound = True
            bestNote["active"] = False
            self.notes_hit += 1
            self.rhythm.total_hits = self.notes_hit

            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()

            baseDamage = 0

            if bestDistance <= perfectWindow:
                baseDamage = 15
                feedback = "PERFECT!"
                particleColor = (255, 255, 0)
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hitLineY, particleColor)

            elif bestDistance <= excellentWindow:
                baseDamage = 12
                feedback = "EXCELLENT!"
                particleColor = (100, 255, 255)
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hitLineY, particleColor)

            elif bestDistance <= goodWindow:
                baseDamage = 8
                feedback = "GOOD"

            elif bestDistance <= okWindow:
                baseDamage = 5
                feedback = "OK"

            else:
                baseDamage = 2
                feedback = "LATE!" if (bestNote["time"] - currentTime) < 0 else "EARLY!"

            self.dealDamageToBoss(baseDamage, feedback)

        else:
            self.rhythm.combo = 0
            self.playRandomFail()

            damage = 3
            currentHp = self.player.getHealth()
            self.player.setHealth(max(0, currentHp - damage))

            if self.player.getHealth() <= 0:
                self.game_over = True
                self.victory = False
                self.stopAllAudio()

    def dealDamageToBoss(self, damage, feedback):
        self.rhythm.combo += 1
        comboMultiplier = 1 + (self.rhythm.combo // 5) * 0.2
        finalDamage = int(damage * comboMultiplier)

        try:
            drunkenness = self.player.getDrunkenness()
        except Exception:
            drunkenness = 0

        drunkennessDamagePenalty = int((drunkenness / 100) * 20)
        finalDamage = max(1, finalDamage - drunkennessDamagePenalty)

        if drunkenness >= 50:
            finalDamage = int(finalDamage * 1.2)

        finalDamage = finalDamage // 2

        self.player.setCurrentAction("attacking", 30)

        bossHp = self.boss.getHealth()
        newBossHp = max(0, bossHp - finalDamage)
        self.boss.setHealth(newBossHp)

        Logger.debug("RhythmCombatController.dealDamageToBoss",
                    f"Boss health: {bossHp} -> {newBossHp}",
                    feedback=feedback,
                    damage=finalDamage)

        self.rhythm.feedback = feedback
        self.rhythm.feedbackTimer = 20

        self.playRandomHit()

        if self.boss.getHealth() <= 0:
            self.victory = True
            self.game_over = True
            Logger.debug("RhythmCombatController.dealDamageToBoss", "Boss defeated")
            self.stopAllAudio()

    def endCombat(self):
        self.game_over = True
        self.victory = False
        self.rhythm.cashEarned = 0

        if self.boss.getHealth() > 0:
            self.victory = False
            Logger.debug("RhythmCombatController.endCombat", "Defeat - boss survived", bossHp=self.boss.getHealth())
        else:
            self.victory = True

            try:
                playerLevel = self.player.getLevel() if self.player else 0
                levelMultiplier = playerLevel + 1
                baseReward = 250

                baseCash = int(baseReward * levelMultiplier)

                bonusCash = 0
                if self.notes_missed == 0 and self.total_notes > 0:
                    bonusCash = int(baseCash * 0.20)

                cash = baseCash + bonusCash
                self.rhythm.cashEarned = cash

                if self.player:
                    self.player.addCurrency(cash)

                Logger.debug("RhythmCombatController.endCombat", "Victory reward calculated", baseCash=baseCash, bonusCash=bonusCash, totalCash=cash)

            except Exception as e:
                Logger.error("RhythmCombatController.endCombat", e)
                self.rhythm.cashEarned = 0

        Logger.debug("RhythmCombatController.endCombat", "Combat ended", victory=self.victory, notesHit=self.notes_hit, notesMissed=self.notes_missed)

        self.stopAllAudio()

    def getLaneX(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.laneX[idx]

    def playRandomFail(self):
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()
    
    def playRandomHit(self):
        if self.hit_sounds:
            sound = random.choice(self.hit_sounds)
            sound.play()

    def stopAllAudio(self):
        try:
            self.guitar_channel.stop()
            self.track_backing.stop()
            self.track_guitar.stop()
            for sound in self.fail_sounds:
                sound.stop()
            for sound in self.hit_sounds:
                sound.stop()
        except Exception as e:
            print(f"Erreur en arrêtant les audios: {e}")

    def pauseAudio(self):
        try:
            self.stored_guitar_volume = self.guitar_channel.get_volume()
            self.guitar_channel.set_volume(0)
            if self.track_backing:
                self.track_backing.set_volume(0)
        except Exception as e:
            print(f"Erreur en mettant en pause les audios: {e}")

    def resumeAudio(self):
        try:
            if hasattr(self, 'stored_guitar_volume'):
                self.guitar_channel.set_volume(self.stored_guitar_volume)
            else:
                self.guitar_channel.set_volume(1.0)
            if self.track_backing:
                self.track_backing.set_volume(1.0)
        except Exception as e:
            print(f"Erreur en reprenant les audios: {e}")

    def startMusic(self):
        self.start_time = pygame.time.get_ticks()
        self.track_backing.play()
        self.guitar_channel.play(self.track_guitar)
        self.is_playing = True
        print("Musique lancée - LE COMBAT COMMENCE !")

    def update(self):
        if self.game_over or self.is_paused:
            return
        
        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            print(f"GAME OVER : {self.player.getName()} est K.O. !")
            self.stopAllAudio()
            return

        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            if remaining <= 0:
                self.waiting_to_start = False
                self.startMusic()
            
            return

        if not self.is_playing:
            self.startMusic()

        current_time = pygame.time.get_ticks() - self.start_time

        if self.rhythm.feedback_timer > 0:
            self.rhythm.feedback_timer -= 1
        else:
            self.rhythm.feedback = ""

        notes_remaining = False
        for note in self.rhythm.notes:
            if note["active"]:
                notes_remaining = True
                time_diff = note["time"] - current_time
                note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)

                if note["y"] > self.rhythm.hit_line_y + 100:
                    note["active"] = False
                    self.triggerMiss()
        
        if not notes_remaining and self.is_playing:
            self.endCombat()

    def triggerMiss(self):
        current_real_time = pygame.time.get_ticks()
        
        if current_real_time - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0)
            self.playRandomFail()

        self.notes_missed += 1
        
        self.rhythm.feedback = "MISS!"
        self.rhythm.feedback_timer = 30
        self.rhythm.combo = 0
        
        damage_to_player = 10
        current_hp = self.player.getHealth()
        self.player.setHealth(max(0, current_hp - damage_to_player))
        
        self.boss.setCurrentAction("attacking", 30)
        
        print(f"MISS → {self.player.getName()} prend {damage_to_player} dégâts ! (HP: {self.player.getHealth()})")
        
        boss_heal = 5
        boss_hp = self.boss.getHealth()
        self.boss.setHealth(min(self.boss_max_health, boss_hp + boss_heal))
        
        print(f"Le boss récupère {boss_heal} HP ! (HP: {self.boss.getHealth()})")
        
        if self.player.getHealth() <= 0:
            self.game_over = True
            self.victory = False
            print(f"GAME OVER : {self.player.getName()} est K.O. !")
            self.guitar_channel.stop()
            self.track_backing.stop()

    def handleInput(self, event):
        if self.waiting_to_start or self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.checkHit(lane)

    def checkHit(self, lane):
        current_time = pygame.time.get_ticks() - self.start_time
        
        perfect_window = 50
        excellent_window = 100
        good_window = 150
        ok_window = 200
        miss_window = 250
        
        hit_found = False
        best_note = None
        best_distance = float('inf')

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
            self.rhythm.total_hits = self.notes_hit
            
            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()
            
            base_damage = 0
            
            if best_distance <= perfect_window:
                base_damage = 15 
                feedback = "PERFECT!"
                particle_color = (255, 255, 0)
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= excellent_window:
                base_damage = 12  
                feedback = "EXCELLENT!"
                particle_color = (100, 255, 255)
                self.view.create_particles(self.get_lane_x(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= good_window:
                base_damage = 8  
                feedback = "GOOD"
                
            elif best_distance <= ok_window:
                base_damage = 5 
                feedback = "OK"
                
            else:
                base_damage = 2  
                feedback = "LATE!" if (best_note["time"] - current_time) < 0 else "EARLY!"
            
            
            self.dealDamageToBoss(base_damage, feedback)
            
        else:
            self.rhythm.combo = 0
            self.playRandomFail()
            
            damage = 3
            current_hp = self.player.getHealth()
            self.player.setHealth(max(0, current_hp - damage))
            
            if self.player.getHealth() <= 0:
                self.game_over = True
                self.victory = False
                self.stopAllAudio()

    def dealDamageToBoss(self, damage, feedback):
        self.rhythm.combo += 1
        combo_multiplier = 1 + (self.rhythm.combo // 5) * 0.2
        final_damage = int(damage * combo_multiplier)

        try:
            drunkenness = self.player.getDrunkenness()
        except Exception:
            drunkenness = 0
        
        drunkenness_damage_penalty = int((drunkenness / 100) * 20)
        final_damage = max(1, final_damage - drunkenness_damage_penalty)
        
        if drunkenness >= 50:
            final_damage = int(final_damage * 1.2)

        final_damage = final_damage // 2
        
        self.player.setCurrentAction("attacking", 30)
        
        boss_hp = self.boss.getHealth()
        new_boss_hp = max(0, boss_hp - final_damage)
        self.boss.setHealth(new_boss_hp)
        
        from Utils.Logger import Logger
        Logger.debug("RhythmCombatController.dealDamageToBoss", 
                    f"Boss health: {boss_hp} -> {new_boss_hp} ({feedback})", 
                    damage=final_damage)
        
        self.rhythm.feedback = feedback
        self.rhythm.feedback_timer = 20
        
        self.playRandomHit()
        
        if self.boss.getHealth() <= 0:
            self.victory = True
            self.game_over = True
            print(f"VICTOIRE ! {self.boss.getName()} est vaincu !")
            self.stopAllAudio()

    def endCombat(self):
        self.game_over = True
        self.victory = False
        self.rhythm.cash_earned = 0
        
        if self.boss.getHealth() > 0:
            self.victory = False
            print(f"DÉFAITE : {self.boss.getName()} a survécu avec {self.boss.getHealth()} HP !")
        else:
            self.victory = True
            
            try:
                player_level = self.player.getLevel() if self.player else 0
                level_multiplier = player_level + 1
                base_reward = 250
                
                base_cash = int(base_reward * level_multiplier)
                
                bonus_cash = 0
                if self.notes_missed == 0 and self.total_notes > 0:
                    bonus_cash = int(base_cash * 0.20)
                
                cash = base_cash + bonus_cash
                self.rhythm.cash_earned = cash
                
                if self.player:
                    self.player.addCurrency(cash)
                
                print(f"=== BOSS DEFEATED - VICTORY! ===")
                print(f"Base Reward: ${base_reward} × {level_multiplier} (level multiplier) = ${base_cash}")
                print(f"Performance: {self.notes_hit}/{self.total_notes} notes hit")
                if bonus_cash > 0:
                    print(f"Perfect Performance Bonus: +${bonus_cash}")
                print(f"Total Earnings: ${cash}")
                print(f"Player Total Currency: ${self.player.getCurrency() if self.player else '?'}")
                
            except Exception as e:
                print(f"ERROR calculating victory rewards: {e}")
                self.rhythm.cash_earned = 0
            
            print(f"VICTOIRE : {self.boss.getName()} vaincu !")
        
    
        print(f"STATS FINALES :")
        print(f"   Notes touchées : {self.notes_hit}/{self.total_notes}")
        print(f"   Notes ratées : {self.notes_missed}")
        print(f"   Combo max : {self.rhythm.combo}")
        print(f"   HP Joueur : {self.player.getHealth() if self.player else '?'}")
        print(f"   HP Boss : {self.boss.getHealth()}")
        
        self.stopAllAudio()

    def get_lane_x(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.lane_x[idx]