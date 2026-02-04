class SongModel:
    def __init__(self, title, artist, bpm, audio_file_guitar, audio_file_backing):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.audio_guitar = audio_file_guitar
        self.audio_backing = audio_file_backing
        
        self.notes_data = []
        
    # ON AJOUTE 'duration' (par défaut 0.5 temps) 👇
    def add_note(self, beat_number, lane, duration=0.5):
        """
        beat_number : Quand la note commence (ex: 0)
        duration : Combien de temps elle dure (ex: 1.5)
        """
        ms_per_beat = 60000 / self.bpm
        
        timestamp = beat_number * ms_per_beat
        duration_ms = duration * ms_per_beat # On convertit la durée en millisecondes
        
        self.notes_data.append({
            "time": int(timestamp),
            "lane": lane,
            "duration": int(duration_ms), # On stocke la durée
            "active": True,
            "hit": False
        })

    def get_notes(self):
        return sorted(self.notes_data, key=lambda x: x["time"])