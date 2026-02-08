from Models.SongModel import SongModel

def loadSevenNationArmy():
    song = SongModel(
        "Seven Nation Army",
        "The White Stripes",
        120, 
        "Game/Assets/Sounds/SNA-GUI.ogg", 
        "Game/Assets/Sounds/SNA-RES.ogg"
    )

    # Boucle de 4 mesures (0, 4, 8...)
    for measure in range(0, 32, 4):
        
        t = measure * 4 

        # MESURE 1
        song.addNote(t + 0,    "LANE1", 1) 
        song.addNote(t + 1.5,  "LANE1", 0.5) 
        song.addNote(t + 2,    "LANE2", 0.75) 
        song.addNote(t + 2.75, "LANE1", 0.75) 
        song.addNote(t + 3.5,  "LANE3", 0.75) # Celle-ci dure longtemps !

        # MESURE 2
        song.addNote(t + 4 + 0, "LANE4", 1.5) 
        song.addNote(t + 4 + 2, "LANE3", 1.5) # Longue finale

        # MESURE 3
        song.addNote(t + 8 + 0,    "LANE1", 1)
        song.addNote(t + 8 + 1.5,  "LANE1", 0.5)
        song.addNote(t + 8 + 2,    "LANE2", 0.75)
        song.addNote(t + 8 + 2.75, "LANE1", 0.75)
        song.addNote(t + 8 + 3.5,  "LANE3", 0.5)

        # MESURE 4
        song.addNote(t + 12 + 0,    "LANE4", 0.5)
        song.addNote(t + 12 + 0.75, "LANE3", 0.75)
        song.addNote(t + 12 + 1.5,  "LANE2", 0.5)
        song.addNote(t + 12 + 2,    "LANE1", 1.5) # Note finale longue

    return song