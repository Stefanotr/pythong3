import pygame
import random
import math
from Songs.SevenNationArmy import loadSevenNationArmy
from Utils.Logger import Logger


class RhythmController:

    def __init__(self, rhythmModel, characterModel, screenHeight, view, songData=loadSevenNationArmy(), context="act1"):
        self.rhythm = rhythmModel
        self.character = characterModel 
        self.view = view
        self.context = context

        self.current_song = songData
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
        self.current_count_down_val = 5

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

        self.rhythm.hit_line_y = int(screenHeight * 0.85)

        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }

        for note in self.rhythm.notes:
            note["y"] = self.rhythm.hit_line_y

        Logger.debug("RhythmController.__init__", "Initialized", context=context)

    def playRandomFail(self):
        if self.fail_sounds:
            sound = random.choice(self.fail_sounds)
            sound.play()

    def stopAllAudio(self):
        try:
            self.guitar_channel.stop()
            self.track_backing.stop()
            self.track_guitar.stop()
            for sound in self.fail_sounds:
                sound.stop()
        except Exception as e:
            Logger.error("RhythmController.stopAllAudio", e)

    def pauseAudio(self):
        try:
            self.stored_guitar_volume = self.guitar_channel.get_volume()
            self.guitar_channel.set_volume(0)
            if self.track_backing:
                self.track_backing.set_volume(0)
        except Exception as e:
            Logger.error("RhythmController.pauseAudio", e)

    def resumeAudio(self):
        try:
            if hasattr(self, 'stored_guitar_volume'):
                self.guitar_channel.set_volume(self.stored_guitar_volume)
            else:
                self.guitar_channel.set_volume(1.0)
            if self.track_backing:
                self.track_backing.set_volume(1.0)
        except Exception as e:
            Logger.error("RhythmController.resumeAudio", e)

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

            self.current_count_down_val = math.ceil(remaining / 1000)

            if remaining <= 0:
                self.is_paused = False
                self.waiting_to_start = False
                pygame.mixer.unpause()
                pauseDuration = pygame.time.get_ticks() - self.pause_time
                self.start_time += pauseDuration
                Logger.debug("RhythmController.update", "Resume from pause")
            return

        if self.waiting_to_start:
            now = pygame.time.get_ticks()
            elapsed = now - self.countdown_start_tick
            remaining = self.countdown_duration - elapsed

            self.current_count_down_val = math.ceil(remaining / 1000)

            fakeTime = -remaining

            for note in self.rhythm.notes:
                if note["active"]:
                    timeDiff = note["time"] - fakeTime
                    note["y"] = self.rhythm.hit_line_y - (timeDiff * self.note_speed)

            if remaining <= 0:
                self.waiting_to_start = False
                self.startMusic()

            return

        if not self.is_playing:
            self.startMusic()

        currentTime = pygame.time.get_ticks() - self.start_time

        if self.rhythm.feedback_timer > 0:
            self.rhythm.feedback_timer -= 1
        else:
            self.rhythm.feedback = ""

        for note in self.rhythm.notes:
            if note["active"]:
                timeDiff = note["time"] - currentTime
                note["y"] = self.rhythm.hit_line_y - (timeDiff * self.note_speed)

                if note["y"] > self.rhythm.hit_line_y + 100:
                    note["active"] = False
                    self.triggerMiss()

        self.checkSongFinished()

        if self.song_finished and not self.continue_pressed:
            if self.getAutoContinueRemaining() <= 0:
                self.continue_pressed = True

        if self.continue_pressed:
            self.game_over = True

    def triggerMiss(self):
        currentRealTime = pygame.time.get_ticks()

        if currentRealTime - self.last_hit_time > 200:
            self.guitar_channel.set_volume(0)
            self.playRandomFail()

        self.rhythm.feedback = "MISS!"
        self.rhythm.feedbackTimer = 30
        self.rhythm.score = max(0, self.rhythm.score - 50)
        self.rhythm.combo = 0

        self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 8)

        if self.rhythm.crowd_satisfaction <= 0:
            self.game_over = True
            Logger.debug("RhythmController.triggerMiss", "Game over - crowd left")
            self.stopAllAudio()

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

            self.guitar_channel.set_volume(1.0)
            self.last_hit_time = pygame.time.get_ticks()

            if bestDistance <= perfectWindow:
                points = 300
                hypeGain = 5
                feedback = "PERFECT! ⭐"
                particleColor = (255, 255, 0)
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hitLineY, particleColor)

            elif bestDistance <= excellentWindow:
                points = max(150, int(300 - bestDistance * 1.5))
                hypeGain = 3
                feedback = "EXCELLENT! ✨"
                particleColor = (100, 255, 255)
                self.view.create_particles(self.getLaneX(lane), self.rhythm.hitLineY, particleColor)

            elif bestDistance <= goodWindow:
                points = max(80, int(200 - bestDistance))
                hypeGain = 2
                feedback = "GOOD 👍"
                particleColor = (50, 255, 50)

            elif bestDistance <= okWindow:
                points = max(30, int(120 - bestDistance * 0.5))
                hypeGain = 1
                feedback = "OK 😐"
                particleColor = (255, 200, 100)

            else:
                points = max(5, int(40 - bestDistance * 0.1))
                hypeGain = 0
                feedback = "LATE! 💩" if (bestNote["time"] - currentTime) < 0 else "EARLY! 💩"
                particleColor = (150, 150, 150)

            self.registerHit(points, feedback, hypeGain)

        else:
            self.rhythm.feedback = "MISS! ❌"
            self.rhythm.feedback_timer = 30
            self.rhythm.score = max(0, self.rhythm.score - 20)
            self.rhythm.combo = 0
            self.rhythm.crowd_satisfaction = max(0, self.rhythm.crowd_satisfaction - 5)
            self.playRandomFail()

    def registerHit(self, points, text, hypeGain):
        self.rhythm.feedback = text
        self.rhythm.feedback_timer = 20
        self.rhythm.combo += 1
        self.rhythm.total_hits += 1

        multiplier = 1 + (self.rhythm.combo // 10) * 0.5
        finalPoints = int(points * multiplier)

        self.rhythm.score += finalPoints

        self.rhythm.crowd_satisfaction = min(100, self.rhythm.crowd_satisfaction + hypeGain)

        if self.rhythm.combo % 10 == 0:
            Logger.debug("RhythmController.registerHit", "Combo landmark", combo=self.rhythm.combo, score=self.rhythm.score, hype=self.rhythm.crowd_satisfaction)

    def togglePause(self):
        if self.is_paused:
            self.resumePause()
        else:
            self.is_paused = True
            self.pause_time = pygame.time.get_ticks()
            pygame.mixer.pause()
            Logger.debug("RhythmController.togglePause", "Paused")

    def resumePause(self):
        self.is_paused = False
        self.waiting_to_start = True
        self.countdown_duration = 5000
        self.countdown_start_tick = pygame.time.get_ticks()
        self.current_count_down_val = 5
        pygame.mixer.pause()
        Logger.debug("RhythmController.resumePause", "Resume countdown started")

    def checkSongFinished(self):
        if self.is_playing and not self.song_finished:
            currentTime = pygame.time.get_ticks() - self.start_time

            if self.rhythm.notes:
                lastNoteEnd = max(note["time"] + note["duration"] for note in self.rhythm.notes)
                songDuration = lastNoteEnd + 500
            else:
                songDuration = 13000

            if currentTime >= songDuration:
                self.song_finished = True
                self.finish_time = pygame.time.get_ticks()
                pygame.mixer.stop()
                Logger.debug("RhythmController.checkSongFinished", "Song finished")

    def getAutoContinueRemaining(self):
        if not self.song_finished:
            return 0
        elapsed = pygame.time.get_ticks() - self.finish_time
        remainingMs = self.finish_delay - elapsed
        remainingS = max(0, remainingMs // 1000)
        return remainingS

    def endConcert(self):
        try:
            player_level = self.character.getLevel() if self.character else 0
            levelMultiplier = player_level + 1

            if self.context == "rhythm_combat":
                cashPerHit = 2
            else:
                cashPerHit = 1

            totalHits = getattr(self.rhythm, 'total_hits', 0)
            baseCash = totalHits * cashPerHit * levelMultiplier

            bonusCash = 0
            if self.rhythm.crowd_satisfaction > 90:
                bonusCash = int(baseCash * 0.20)

            cash = baseCash + bonusCash

            self.rhythm.cash_earned = cash

            if self.character:
                self.character.addCurrency(cash)

            Logger.debug("RhythmController.endConcert", "Concert complete", context=self.context, totalHits=totalHits, cashEarned=cash)

            return cash
        except Exception as e:
            Logger.error("RhythmController.endConcert", e)
            self.rhythm.cash_earned = 0
            return 0

    def getLaneX(self, lane):
        idx = self.rhythm.lanes.index(lane)
        return self.view.laneX[idx]