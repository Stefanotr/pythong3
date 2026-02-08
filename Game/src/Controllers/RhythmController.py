import pygame
import random
import math
from Songs.SevenNationArmy import load_seven_nation_army





class RhythmController:


    
    def __init__(self, rhythm_model, character_model, screen_height, view,song_data=load_seven_nation_army(), context="act1"):
        self.rhythm = rhythm_model
        self.character = character_model 
        self.view = view
        self.context = context 
        
      
        self.current_song = song_data
        self.rhythm.notes = self.current_song.get_notes()
        
        pygame.mixer.init()
        
    
        self.track_guitar = pygame.mixer.Sound(self.current_song.audio_guitar)
        self.track_backing = pygame.mixer.Sound(self.current_song.audio_backing)
        
 
        self.guitar_channel = pygame.mixer.Channel(1)
        self.track_guitar.set_volume(1.0)
        self.track_backing.set_volume(1.0)

      
        self.fail_sounds = []
        try:
            for i in range(1, 6):
                sound = pygame.mixer.Sound(f"Game/Assets/Sounds/fail{i}.ogg")
                sound.set_volume(0.6)
                self.fail_sounds.append(sound)
        except FileNotFoundError:
            pass 

        self.note_speed = 0.5 
        
        self.waiting_to_start = True 
        self.countdown_duration = 5000 
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5

        self.start_time = 0
        self.is_playing = False
        self.is_paused = False  
        self.game_over = False
        
        self.song_finished = False  
        self.finish_time = 0  
        self.finish_delay = 5000  
        self.continue_pressed = False  
        
        self.is_paused = False
        self.pause_time = 0  
        self.pause_music_position = 0  
        
        self.last_hit_time = -1000 
        
        self.rhythm.hit_line_y = int(screen_height * 0.85)

        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }
        
        for note in self.rhythm.notes:
            note["y"] = self.rhythm.hit_line_y



    def playRandomFail(self):
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()


    def stop_all_audio(self):

        try:
            self.guitar_channel.stop()
            self.track_backing.stop()
            self.track_guitar.stop()
           
            for sound in self.fail_sounds:
                sound.stop()
        except Exception as e:
            print(f"Erreur en arrêtant les audios: {e}")


    def pause_audio(self):
        try:
            self.stored_guitar_volume = self.guitar_channel.get_volume()
            self.guitar_channel.set_volume(0)
            if self.track_backing:
                self.track_backing.set_volume(0)
        except Exception as e:
            print(f"Erreur en mettant en pause les audios: {e}")




    def resume_audio(self):
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




    def update(self):

        if self.game_over:
            return 
        

        if self.is_paused:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            
            self.current_countdown_val = math.ceil(remaining / 1000)
            
            if remaining <= 0:
                
                self.is_paused = False
                self.waiting_to_start = False
                
                pygame.mixer.unpause()
                pause_duration = pygame.time.get_ticks() - self.pause_time
                self.start_time += pause_duration  
                print("Reprise!")
            return

        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed
            

            self.current_countdown_val = math.ceil(remaining / 1000)
            
            fake_time = -remaining
            
            for note in self.rhythm.notes:
                if note["active"]:
                    time_diff = note["time"] - fake_time
                    note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)
            
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

        for note in self.rhythm.notes:
            if note["active"]:
                time_diff = note["time"] - current_time
                note["y"] = self.rhythm.hit_line_y - (time_diff * self.note_speed)

                
                if note["y"] > self.rhythm.hit_line_y + 100:
                    note["active"] = False
                    self.triggerMiss()
        
        
        
        self.checkSongFinished()
        
       
       
        if self.song_finished and not self.continue_pressed:
            if self.get_auto_continue_remaining() <= 0:
                self.continue_pressed = True
        
       
        if self.continue_pressed:
            self.game_over = True



    def triggerMiss(self):
        
        current_real_time = pygame.time.get_ticks()
        
       
        if current_real_time - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0) 
            self.playRandomFail()

   
        self.rhythm.feedback = "MISS!"
        self.rhythm.feedback_timer = 30
        self.rhythm.score = max(0, self.rhythm.score - 50) 
        self.rhythm.combo = 0
        
       
        self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 8)
        
       
        if self.rhythm.crowd_satisfaction <= 0:
            self.game_over = True
            print("GAME OVER : Le public vous a dégagé !")
            self.stop_all_audio()




    def handleInput(self, event):
       
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self.waiting_to_start and self.is_playing and not self.game_over and not self.song_finished:
                self.togglePause()
            return
        
        
        if self.song_finished and not self.continue_pressed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.continue_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.continue_pressed = True
            return
        
       
        if self.waiting_to_start or self.game_over or self.is_paused or self.song_finished:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.checkHit(lane)

   
    def handle_input(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handleInput(event)

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
            
            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()
            
           
            
            if best_distance <= perfect_window:
               
                points = 300
                hype_gain = 5
                feedback = "PERFECT!"
                particle_color = (255, 255, 0)  
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= excellent_window:
            
                points = max(150, int(300 - best_distance * 1.5))
                hype_gain = 3
                feedback = "EXCELLENT!"
                particle_color = (100, 255, 255)  
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hit_line_y, particle_color)
                
            elif best_distance <= good_window:
                
                points = max(80, int(200 - best_distance))
                hype_gain = 2
                feedback = "GOOD"
                particle_color = (50, 255, 50)  
                
            elif best_distance <= ok_window:
               
               
                points = max(30, int(120 - best_distance * 0.5))
                hype_gain = 1
                feedback = "OK"
                particle_color = (255, 200, 100)  
                
            else:
                
                points = max(5, int(40 - best_distance * 0.1))
                hype_gain = 0
                feedback = "LATE! 💩" if (best_note["time"] - current_time) < 0 else "EARLY! 💩"
                particle_color = (150, 150, 150)  
            
            
            self.registerHit(points, feedback, hype_gain)
            
        else:
           
           
            self.rhythm.feedback = "MISS!"
            self.rhythm.feedback_timer = 30
            self.rhythm.score = max(0, self.rhythm.score - 20)  
            self.rhythm.combo = 0  
            self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 5)  
            self.playRandomFail()



    def registerHit(self, points, text, hype_gain):
        
        self.rhythm.feedback = text
        self.rhythm.feedback_timer = 20
        self.rhythm.combo += 1
        self.rhythm.total_hits += 1 
        
       
        multiplier = 1 + (self.rhythm.combo // 10) * 0.5 
        final_points = int(points * multiplier)
        
        self.rhythm.score += final_points
        
        
        self.rhythm.crowd_satisfaction = min(100, self.rhythm.crowd_satisfaction + hype_gain)
        
        
        if self.rhythm.combo % 10 == 0:  
            print(f"🎯 Combo x{self.rhythm.combo} | Score: {self.rhythm.score} | Hype: {self.rhythm.crowd_satisfaction}%")


    def togglePause(self):
       
        if self.is_paused:
            
            self.resume_pause()
        else:
           
            self.is_paused = True
            self.pause_time = pygame.time.get_ticks()
            
            pygame.mixer.pause()
            print("⏸️ PAUSE")

    def resume_pause(self):
        
        self.is_paused = False
        
        self.waiting_to_start = True
        self.countdown_duration = 5000
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_countdown_val = 5
        
        pygame.mixer.pause()
        print("⏱️ Décompte avant reprise: 5s")

    def checkSongFinished(self):
        
        if self.is_playing and not self.song_finished:
            current_time = pygame.time.get_ticks() - self.start_time
            
            
            if self.rhythm.notes:
                
                last_note_end = max(note["time"] + note["duration"] for note in self.rhythm.notes)
                
                song_duration = last_note_end + 500  
            else:
               
                song_duration = 13000
            
            if current_time >= song_duration:
                self.song_finished = True
                self.finish_time = pygame.time.get_ticks()
                pygame.mixer.stop()
                print("🎵 Chanson terminée!")
    

    def get_auto_continue_remaining(self):
        
        if not self.song_finished:
            return 0
        elapsed = pygame.time.get_ticks() - self.finish_time
        remaining_ms = self.finish_delay - elapsed
        remaining_s = max(0, remaining_ms // 1000)
        return remaining_s
    


    def end_concert(self):
    
    
        try:
            player_level = self.character.getLevel() if self.character else 0
            level_multiplier = player_level + 1  
            
           
           
            if self.context == "rhythm_combat":
                cash_per_hit = 2  
            else:  
                cash_per_hit = 1  
            

            total_hits = getattr(self.rhythm, 'total_hits', 0)
            base_cash = total_hits * cash_per_hit * level_multiplier
            

            bonus_cash = 0
            if self.rhythm.crowd_satisfaction > 90:
                bonus_cash = int(base_cash * 0.20)
            
            cash = base_cash + bonus_cash
            
            self.rhythm.cash_earned = cash
            
            if self.character:
                self.character.addCurrency(cash)
            
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





    def play_random_fail(self):
        return self.playRandomFail()
    
    def start_music(self):
        return self.startMusic()
    
    def trigger_miss(self):

        return self.triggerMiss()
    

    def check_hit(self, lane):

        return self.checkHit(lane)
    
    def register_hit(self, points, text, hype_gain):

        return self.registerHit(points, text, hype_gain)
    

    def toggle_pause(self):
        return self.togglePause()
    



    def check_song_finished(self):

        return self.checkSongFinished()
    
    def get_lane_x(self, lane):

        return self.getLaneX(lane)

    def getLaneX(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.lane_x[idx]