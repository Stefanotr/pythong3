class SongModel:


    def __init__(self, name, artist, bpm, audio_file_guitar, audio_file_backing):
       
        self.name = name      
        self.artist = artist
        self.bpm = bpm
        
        
        self.audio_guitar = audio_file_guitar
        self.audio_backing = audio_file_backing
        
       
       
        self.notes = []


    def add_note(self, beat_start, lane, beat_duration=0.5):
       
       
        ms_per_beat = 60000 / self.bpm
        
        
        start_ms = int(beat_start * ms_per_beat)
        duration_ms = int(beat_duration * ms_per_beat)
        
       
        new_note = {
            "time": start_ms,       
            "lane": lane,          
            "duration": duration_ms,
            "active": True,         
            "hit": False            
        }
        
      
        self.notes.append(new_note)



    def get_notes(self):
      
      
       
        self.notes.sort(key=lambda x: x["time"])
        return self.notes