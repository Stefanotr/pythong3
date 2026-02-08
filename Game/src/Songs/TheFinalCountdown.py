from Models.SongModel import SongModel

def loadFinalCountdown():

    song = SongModel(
        "The Final Countdown",
        "Europe",
        118, 
        "Game/Assets/Sounds/pg3.ogg",
        "Game/Assets/Sounds/pr3.ogg"
    )

    # --- NOTES DU MORCEAU ---
    # Timings et durées d'origine conservés à 100%.
    # Répartition logique des Lanes (1=Vert, 2=Rouge, 3=Jaune, 4=Bleu)

    # MESURE 1 à 6 (Intro)
    
    # MESURE 7 (Le Riff commence : Tu-tu-tu-tuuu)
    t = 6 * 4
    song.addNote(t + 1.5,  "LANE3", 0.15) # Note rapide
    song.addNote(t + 1.75, "LANE2", 0.15) # Note rapide
    song.addNote(t + 2,    "LANE3", 0.75) # Note moyenne
    song.addNote(t + 3,    "LANE1", 1)    # Note longue (Basse)

    # MESURE 8
    t = 7 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.50, "LANE3", 0.15)
    song.addNote(t + 3,    "LANE1", 1.5)

    # MESURE 9
    t = 8 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 10
    t = 9 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 11
    t = 10 * 4
    song.addNote(t + 0,    "LANE1", 1.25)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 0.75)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 12
    t = 11 * 4
    song.addNote(t + 1.5,    "LANE4", 0.15)
    song.addNote(t + 1.75,   "LANE3", 0.15)
    song.addNote(t + 2,      "LANE4", 0.15)
    song.addNote(t + 2.5,    "LANE3", 0.15)
    song.addNote(t + 3,      "LANE2", 1.5)

    # MESURE 13
    t = 12 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.75)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 14
    t = 13 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 15
    t = 14 * 4
    song.addNote(t + 0,    "LANE1", 1.50)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 16
    t = 15 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 17
    t = 16 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 18
    t = 17 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 19
    t = 18 * 4
    song.addNote(t + 0,    "LANE1", 1.5)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 20
    t = 19 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 21
    t = 20 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE4", 1)

    # MESURE 22
    t = 21 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 23
    t = 22 * 4
    song.addNote(t + 0,    "LANE1", 1.5)
    song.addNote(t + 1.5,  "LANE2", 0.5)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1.5)
    song.addNote(t + 3.5,  "LANE2", 0.25)
    song.addNote(t + 3.75, "LANE1", 0.25)

    # MESURE 24
    t = 23 * 4
    song.addNote(t + 0,   "LANE1", 0.75)
    song.addNote(t + 0.5, "LANE2", 0.5)
    song.addNote(t + 1,   "LANE3", 0.5)
    song.addNote(t + 1.5, "LANE4", 0.5)
    song.addNote(t + 2,   "LANE1", 1)
    song.addNote(t + 3,   "LANE1", 1)

    # MESURE 25
    t = 24 * 4
    song.addNote(t + 0,    "LANE1", 1.75)
    song.addNote(t + 2,    "LANE4", 0.65)
    song.addNote(t + 2.65, "LANE3", 0.70)
    song.addNote(t + 3.35, "LANE2", 0.25)
    song.addNote(t + 3.75, "LANE1", 0.20)

    # MESURE 26
    t = 25 * 4
    song.addNote(t + 0,    "LANE1", 2.90)

    # MESURE 27
    t = 26 * 4
    song.addNote(t + 1.5,    "LANE3", 0.15)
    song.addNote(t + 1.75,   "LANE2", 0.10)
    song.addNote(t + 2,      "LANE3", 0.75)
    song.addNote(t + 3,      "LANE1", 1)

    # MESURE 28
    t = 27 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 29
    t = 28 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 30
    t = 29 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 31
    t = 30 * 4 
    song.addNote(t + 0,    "LANE1", 1.5)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 32
    t = 31 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 33
    t = 32 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 34
    t = 33 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 35
    t = 34 * 4
    song.addNote(t + 0,    "LANE1", 1.25)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1.5)
    song.addNote(t + 3.5,  "LANE2", 0.25)
    song.addNote(t + 3.75, "LANE1", 0.25)

    # MESURE 36
    t = 35 * 4
    song.addNote(t + 0,   "LANE1", 0.5)
    song.addNote(t + 0.5, "LANE2", 0.5)
    song.addNote(t + 1,   "LANE3", 0.5)
    song.addNote(t + 1.5, "LANE4", 0.5)
    song.addNote(t + 2,   "LANE1", 1)
    song.addNote(t + 3,   "LANE1", 1)

    # MESURE 37
    t = 36 * 4
    song.addNote(t + 0,    "LANE1", 2.75)
    song.addNote(t + 3,    "LANE2", 0.25)
    song.addNote(t + 3.25, "LANE3", 0.25)
    song.addNote(t + 3.5,  "LANE4", 0.25)
    song.addNote(t + 3.75, "LANE4", 0.50)

    # MESURE 38
    t = 37 * 4
    song.addNote(t + 0,    "LANE1", 3.25)

    # MESURE 40
    t = 39 * 4
    song.addNote(t + 2,    "LANE1", 1)
    song.addNote(t + 3,    "LANE1", 1)

    # MESURE 41
    t = 40 * 4
    song.addNote(t + 0,  "LANE1", 1)
    song.addNote(t + 1,  "LANE2", 1)
    song.addNote(t + 2,  "LANE3", 1)
    song.addNote(t + 3,  "LANE4", 1)

    # MESURE 42
    t = 41 * 4
    song.addNote(t + 0,  "LANE1", 4)

    # MESURE 54
    t = 53 * 4
    song.addNote(t + 1.9,  "LANE2", 1)
    song.addNote(t + 3,    "LANE3", 0.95)
    song.addNote(t + 3.95, "LANE4", 0.75)

    # MESURE 55
    t = 54 * 4
    song.addNote(t + 0.65, "LANE4", 0.25)
    song.addNote(t + 0.9,  "LANE1", 3)

    # MESURE 57
    t = 56 * 4
    song.addNote(t + 0.5, "LANE1", 0.25)
    song.addNote(t + 1,   "LANE2", 0.75)
    song.addNote(t + 2,   "LANE3", 0.35)
    song.addNote(t + 2.5, "LANE4", 0.5)
    song.addNote(t + 3.5, "LANE3", 1.35)

    # MESURE 59
    t = 58 * 4
    song.addNote(t + 1.5,    "LANE3", 0.15)
    song.addNote(t + 1.75,   "LANE2", 0.15)
    song.addNote(t + 2,      "LANE3", 0.75)
    song.addNote(t + 3,      "LANE1", 1)

    # MESURE 60
    t = 59 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 61
    t = 60 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 62
    t = 61 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 63
    t = 62 * 4
    song.addNote(t + 0,    "LANE1", 1.5)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 64
    t = 63 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 65
    t = 64 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE4", 1)

    # MESURE 66
    t = 65 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 67
    t = 66 * 4
    song.addNote(t + 0,    "LANE1", 1.25)

    # MESURE 78
    t = 77 * 4
    song.addNote(t + 2,    "LANE3", 0.9)
    song.addNote(t + 2.9,  "LANE4", 1)

    # MESURE 79
    t = 78 * 4
    song.addNote(t + 0,    "LANE4", 0.7)
    song.addNote(t + 0.7,  "LANE3", 0.4)
    song.addNote(t + 0.9,  "LANE1", 2.85)

    # MESURE 81
    t = 80 * 4
    song.addNote(t + 0.5, "LANE1", 0.25)
    song.addNote(t + 1,   "LANE2", 0.75)
    song.addNote(t + 2,   "LANE3", 0.35)
    song.addNote(t + 2.5, "LANE4", 0.5)
    song.addNote(t + 3.5, "LANE1", 1.35)

    # MESURE 83
    t = 82 * 4
    song.addNote(t + 1.5,    "LANE3", 0.15)
    song.addNote(t + 1.75,   "LANE2", 0.15)
    song.addNote(t + 2,      "LANE3", 0.75)
    song.addNote(t + 3,      "LANE1", 1)

    # MESURE 84
    t = 83 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 85
    t = 84 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE2", 1)

    # MESURE 86
    t = 85 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 87
    t = 86 * 4
    song.addNote(t + 0,    "LANE1", 1.5)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1)
    song.addNote(t + 3,    "LANE1", 1.25)

    # MESURE 88
    t = 87 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 0.15)
    song.addNote(t + 2.5,  "LANE3", 0.15)
    song.addNote(t + 3,    "LANE2", 1.5)

    # MESURE 89
    t = 88 * 4
    song.addNote(t + 1.5,  "LANE4", 0.15)
    song.addNote(t + 1.75, "LANE3", 0.15)
    song.addNote(t + 2,    "LANE4", 1)
    song.addNote(t + 3,    "LANE4", 1)

    # MESURE 90
    t = 89 * 4
    song.addNote(t + 1.5,  "LANE2", 0.15)
    song.addNote(t + 1.75, "LANE1", 0.15)
    song.addNote(t + 2,    "LANE2", 0.15)
    song.addNote(t + 2.5,  "LANE1", 0.15)
    song.addNote(t + 3,    "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE2", 0.15)

    # MESURE 91
    t = 90 * 4
    song.addNote(t + 0,    "LANE1", 1.25)
    song.addNote(t + 1.5,  "LANE3", 0.15)
    song.addNote(t + 1.75, "LANE2", 0.15)
    song.addNote(t + 2,    "LANE3", 1.5)
    song.addNote(t + 3.5,  "LANE2", 0.15)
    song.addNote(t + 3.75, "LANE1", 0.15)

    # MESURE 92
    t = 91 * 4
    song.addNote(t + 0,   "LANE1", 0.5)
    song.addNote(t + 0.5, "LANE2", 0.5)
    song.addNote(t + 1,   "LANE3", 0.5)
    song.addNote(t + 1.5, "LANE4", 0.5)
    song.addNote(t + 2,   "LANE1", 1)
    song.addNote(t + 3,   "LANE4", 1)

    # MESURE 93
    t = 92 * 4
    song.addNote(t + 0,    "LANE1", 2.75)
    song.addNote(t + 3,    "LANE2", 0.15)
    song.addNote(t + 3.25, "LANE3", 0.15)
    song.addNote(t + 3.5,  "LANE4", 0.15)
    song.addNote(t + 3.75, "LANE4", 0.5)

    # MESURE 94
    t = 93 * 4
    song.addNote(t + 0,    "LANE1", 3.25)

    # MESURE 95
    t = 94 * 4
    song.addNote(t + 0.15, "LANE1", 7.5) # Finale sur C

    return song