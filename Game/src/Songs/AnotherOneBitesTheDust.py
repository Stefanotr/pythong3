from Models.SongModel import SongModel

def load_another_one():
    # 110 BPM - Queen
    song = SongModel(
        "Another One Bites the Dust",
        "Queen",
        110, 
        "Game/Assets/Sounds/pg2.ogg",
        "Game/Assets/Sounds/pr2.ogg"
    )

    # --- NOTES DU MORCEAU ---
    # On définit t manuellement pour chaque mesure pour que ce soit clair.
    # 1 Mesure = 4 Temps.

    # MESURE 1 (Intro)
    t = 0 * 4
    song.add_note(t + 3.5,  "LANE1", 0.25) 
    song.add_note(t + 3.75, "LANE2", 0.25) 
            
    # MESURE 2
    t = 1 * 4
    song.add_note(t + 0,    "LANE1", 0.5) 
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.15)

    # MESURE 3 
    t = 2 * 4
    song.add_note(t + 0,    "LANE3", 0.25)
    song.add_note(t + 0.5,  "LANE4", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)
        
    # MESURE 4
    t = 3 * 4
    song.add_note(t + 0,    "LANE1", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 5
    t = 4 * 4
    song.add_note(t + 0,    "LANE3", 0.25)
    song.add_note(t + 0.5,  "LANE4", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 6
    t = 5 * 4
    song.add_note(t + 0,    "LANE1", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.30)

    # MESURE 7 
    t = 6 * 4
    song.add_note(t + 0.5,  "LANE3", 0.45)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 8
    t = 7 * 4
    song.add_note(t + 0,    "LANE1", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.10)

    # MESURE 9
    t = 8 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.25, "LANE4", 0.25)
    song.add_note(t + 0.5,  "LANE3", 0.10)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 10
    t = 9 * 4
    song.add_note(t + 0,    "LANE1", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.15)

    # MESURE 11
    t = 10 * 4
    song.add_note(t + 0,    "LANE3", 0.25)
    song.add_note(t + 0.5,  "LANE4", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 12
    t = 11 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.4)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 13
    t = 12 * 4
    song.add_note(t + 0,    "LANE3", 0.9)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 14
    t = 13 * 4
    song.add_note(t + 0,    "LANE1", 0.20)
    song.add_note(t + 0.5,  "LANE2", 0.25)
    song.add_note(t + 1.25, "LANE1", 0.20)
    song.add_note(t + 1.75, "LANE2", 0.15)
    song.add_note(t + 2,    "LANE1", 0.25)
    song.add_note(t + 2.25, "LANE2", 0.50)
    song.add_note(t + 3,    "LANE1", 0.55)

    # MESURE 15
    t = 14 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.5,  "LANE4", 0.30)
    song.add_note(t + 1.25, "LANE3", 0.20)
    song.add_note(t + 1.75, "LANE4", 0.10)
    song.add_note(t + 2,    "LANE3", 0.30)
    song.add_note(t + 3,    "LANE3", 0.90)

    # MESURE 16
    t = 15 * 4
    song.add_note(t + 0,    "LANE1", 0.25)
    song.add_note(t + 0.5,  "LANE2", 0.20)
    song.add_note(t + 1.25, "LANE1", 0.20)
    song.add_note(t + 1.75, "LANE2", 0.10)
    song.add_note(t + 2,    "LANE1", 0.30)
    song.add_note(t + 2.25, "LANE1", 0.70)
    song.add_note(t + 3,    "LANE2", 0.40)

    # MESURE 17 (Correction virgule manquante)
    t = 16 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.5,  "LANE4", 0.20)
    song.add_note(t + 1,    "LANE3", 0.30)
    song.add_note(t + 1.5,  "LANE4", 0.30)
    song.add_note(t + 1.75, "LANE3", 0.30) 
    song.add_note(t + 3,    "LANE3", 0.80)

    # MESURE 18
    t = 17 * 4
    song.add_note(t + 0,    "LANE1", 0.40)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 19
    t = 18 * 4
    song.add_note(t + 0,    "LANE3", 0.25)
    song.add_note(t + 0.5,  "LANE4", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 20
    t = 19 * 4
    song.add_note(t + 0,    "LANE1", 0.5)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 21
    t = 20 * 4
    song.add_note(t + 0,    "LANE3", 0.90)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.20)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 22 (Correction virgule manquante)
    t = 21 * 4
    song.add_note(t + 0,    "LANE1", 0.45)
    song.add_note(t + 1,    "LANE2", 0.5) 
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.15)

    # MESURE 23
    t = 22 * 4
    song.add_note(t + 0,    "LANE3", 0.3)
    song.add_note(t + 0.5,  "LANE4", 0.55)
    song.add_note(t + 1,    "LANE2", 0.55)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 24 (Correction LANE5 -> LANE4)
    t = 23 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1.5,  "LANE4", 0.25) # LANE5 n'existe pas !
    song.add_note(t + 1.75, "LANE4", 0.25)
    song.add_note(t + 2,    "LANE1", 0.25)
    song.add_note(t + 2.5,  "LANE1", 0.20)
    song.add_note(t + 3,    "LANE1", 0.90)

    # MESURE 25
    t = 24 * 4
    song.add_note(t + 0,    "LANE3", 0.30)
    song.add_note(t + 3,    "LANE4", 0.90)

    # MESURE 26
    t = 25 * 4
    song.add_note(t + 0,    "LANE1", 0.30)
    song.add_note(t + 1,    "LANE2", 0.40)
    song.add_note(t + 2,    "LANE1", 0.40)
    song.add_note(t + 3.75, "LANE2", 0.30)

    # MESURE 27
    t = 26 * 4
    song.add_note(t + 0.5,  "LANE3", 0.45)
    song.add_note(t + 1,    "LANE4", 0.45)
    song.add_note(t + 1.5,  "LANE2", 0.20)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 28
    t = 27 * 4
    song.add_note(t + 0,    "LANE1", 0.55)
    song.add_note(t + 1,    "LANE2", 0.55)
    song.add_note(t + 2,    "LANE1", 0.55)
    song.add_note(t + 3.75, "LANE2", 0.10)

    # MESURE 29
    t = 28 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.25, "LANE4", 0.25)
    song.add_note(t + 0.5,  "LANE3", 0.10)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 30
    t = 29 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.15)

    # MESURE 31
    t = 30 * 4
    song.add_note(t + 0,    "LANE3", 0.30)
    song.add_note(t + 0.5,  "LANE4", 0.55)
    song.add_note(t + 1,    "LANE2", 0.55)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 32
    t = 31 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1,    "LANE2", 0.45)
    song.add_note(t + 2,    "LANE1", 0.45)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 33
    t = 32 * 4
    song.add_note(t + 0,    "LANE3", 0.95)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 34
    t = 33 * 4
    song.add_note(t + 0,    "LANE1", 0.15)
    song.add_note(t + 0.5,  "LANE2", 0.20)
    song.add_note(t + 1.25, "LANE1", 0.20)
    song.add_note(t + 1.75, "LANE2", 0.10)
    song.add_note(t + 2,    "LANE1", 0.25)
    song.add_note(t + 2.25, "LANE2", 0.60)
    song.add_note(t + 3,    "LANE1", 0.35)

    # MESURE 35
    t = 34 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.5,  "LANE4", 0.30)
    song.add_note(t + 1.25, "LANE3", 0.20)
    song.add_note(t + 1.75, "LANE4", 0.10)
    song.add_note(t + 2,    "LANE3", 0.30)
    song.add_note(t + 3,    "LANE3", 0.90)

    # MESURE 36
    t = 35 * 4
    song.add_note(t + 0,    "LANE1", 0.20)
    song.add_note(t + 0.5,  "LANE2", 0.20)
    song.add_note(t + 1.25, "LANE1", 0.20)
    song.add_note(t + 1.75, "LANE2", 0.10)
    song.add_note(t + 2,    "LANE1", 0.30)
    song.add_note(t + 2.25, "LANE1", 0.70)
    song.add_note(t + 3,    "LANE2", 0.35)

    # MESURE 37
    t = 36 * 4
    song.add_note(t + 0,    "LANE3", 0.20)
    song.add_note(t + 0.5,  "LANE4", 0.20)
    song.add_note(t + 1,    "LANE3", 0.30)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)
    song.add_note(t + 3,    "LANE3", 0.85)

    # MESURE 38
    t = 37 * 4
    song.add_note(t + 0,    "LANE1", 0.40)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 39
    t = 38 * 4
    song.add_note(t + 0,    "LANE3", 0.30)
    song.add_note(t + 0.5,  "LANE4", 0.55)
    song.add_note(t + 1,    "LANE2", 0.55)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 40
    t = 39 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1,    "LANE2", 0.4)
    song.add_note(t + 2,    "LANE1", 0.4)
    song.add_note(t + 3.75, "LANE2", 0.20)

    # MESURE 41
    t = 40 * 4
    song.add_note(t + 0,    "LANE3", 0.95)
    song.add_note(t + 1,    "LANE4", 0.5)
    song.add_note(t + 1.5,  "LANE2", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.30)

    # MESURE 42
    t = 41 * 4
    song.add_note(t + 0,    "LANE1", 0.40)
    song.add_note(t + 1,    "LANE2", 0.5)
    song.add_note(t + 2,    "LANE1", 0.5)
    song.add_note(t + 3.75, "LANE2", 0.15)

    # MESURE 43
    t = 42 * 4
    song.add_note(t + 0,    "LANE3", 0.30)
    song.add_note(t + 0.5,  "LANE4", 0.50)
    song.add_note(t + 1,    "LANE2", 0.50)
    song.add_note(t + 1.5,  "LANE4", 0.25)
    song.add_note(t + 1.75, "LANE3", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE2", 0.25)

    # MESURE 44 (Correction LANE5 -> LANE4)
    t = 43 * 4
    song.add_note(t + 0,    "LANE1", 0.4)
    song.add_note(t + 1.5,  "LANE4", 0.20) # LANE5 n'existe pas !
    song.add_note(t + 1.75, "LANE4", 0.25)
    song.add_note(t + 2,    "LANE1", 0.25)
    song.add_note(t + 2.5,  "LANE1", 0.20)
    song.add_note(t + 3,    "LANE1", 0.90)

    # MESURE 45
    t = 44 * 4
    song.add_note(t + 0,    "LANE3", 0.30)
    song.add_note(t + 3,    "LANE4", 0.90)

    # MESURE 46
    t = 45 * 4
    song.add_note(t + 0,    "LANE1", 0.6)

    return song