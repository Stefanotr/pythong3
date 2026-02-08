class SongModel:

    def __init__(self, name, artist, bpm, audio_file_guitar, audio_file_backing):
        self.name = name
        self.artist = artist
        self.bpm = bpm
        self.audio_guitar = audio_file_guitar
        self.audio_backing = audio_file_backing
        self.notes = []


    def addNote(self, beatStart, lane, beatDuration=0.5):
        msPerBeat = 60000 / self.bpm
        
        startMs = int(beatStart * msPerBeat)
        durationMs = int(beatDuration * msPerBeat)
        
        newNote = {
            "time": startMs,
            "lane": lane,
            "duration": durationMs,
            "active": True,
            "hit": False
        }
        
        self.notes.append(newNote)


    def getNotes(self):
        self.notes.sort(key=lambda x: x["time"])
        return self.notes


    def getName(self):
        return self.name

    def getArtist(self):
        return self.artist

    def getBpm(self):
        return self.bpm
