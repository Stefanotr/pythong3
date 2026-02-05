from Models.SongModel import SongModel

def load_another_one():
    # 118 BPM - Europe
    song = SongModel(
        "Another One Bites the Dust",
        "Queen",
        118, 
        "Game/Assets/Sounds/pg2.ogg",
        "Game/Assets/Sounds/pr2.ogg"
    )

    # --- NOTES DU MORCEAU ---
    # On définit t manuellement pour chaque mesure pour que ce soit clair.
    # 1 Mesure = 4 Temps.

    # MESURE 1 (Intro)
    t = 0 * 4
            
    # MESURE 2
    t = 1 * 4

    # MESURE 3 
    t = 2 * 4
        
    # MESURE 4
    t = 3 * 4

    # MESURE 5
    t = 4 * 4

    # MESURE 6
    t = 5 * 4

    # MESURE 7 (p1 m1)
    t = 6 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.75)
    song.add_note(t + 3,   "LANE1", 1)

    # MESURE 8 (p1 m2)
    t = 7 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.50, "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 9 (p1 m3)
    t = 8 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 10 (p1 m4)
    t = 9 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 11 (p1 m5)
    t = 10 * 4
    song.add_note(t + 0,    "LANE1", 1.25)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.75)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 12 (p1 m6)
    t = 11 * 4
    song.add_note(t + 1.5,    "LANE1", 0.15)
    song.add_note(t + 1.75,   "LANE1", 0.15)
    song.add_note(t + 2,      "LANE1", 0.15)
    song.add_note(t + 2.5,    "LANE1", 0.15)
    song.add_note(t + 3,      "LANE1", 1.5)

    # MESURE 13 (p1 m7)
    t = 12 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.75)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 14 (p1 m8)
    t = 13 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 15 (p1 m9)
    t = 14 * 4
    song.add_note(t + 0,    "LANE1", 1.50)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 16 (p1 m10)
    t = 15 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 17 (p1 m11)
    t = 16 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 18 (p1 m12)
    t = 17 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 19 (p1 m13)
    t = 18 * 4
    song.add_note(t + 0,    "LANE1", 1.5)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 20 (p1 m14)
    t = 19 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 21 (p1 m15)
    t = 20 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 22 (p1 m16)
    t = 21 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 23 (p1 m17)
    t = 22 * 4
    song.add_note(t + 0,    "LANE1", 1.5)
    song.add_note(t + 1.5,  "LANE1", 0.5)
    song.add_note(t + 1.75,    "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1.5)
    song.add_note(t + 3.5,    "LANE1", 0.25)
    song.add_note(t + 3.75,   "LANE1", 0.25)

    # MESURE 24 (p1 m18)
    t = 23 * 4
    song.add_note(t + 0,  "LANE1", 0.75)
    song.add_note(t + 0.5,  "LANE1", 0.5)
    song.add_note(t + 1,    "LANE1", 0.5)
    song.add_note(t + 1.5,  "LANE1", 0.5)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 25 (p1 m19)
    t = 24 * 4
    song.add_note(t + 0,    "LANE1", 1.75)
    song.add_note(t + 2, "LANE1", 0.65)
    song.add_note(t + 2.65, "LANE1", 0.70)
    song.add_note(t + 3.35,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE1", 0.20)

    # MESURE 26 (p1 m20)
    t = 25 * 4
    song.add_note(t + 0,    "LANE1", 2.90)

    # MESURE 27 (p1 m21)
    t = 26 * 4
    song.add_note(t + 1.5,    "LANE1", 0.15)
    song.add_note(t + 1.75,   "LANE1", 0.10)
    song.add_note(t + 2,      "LANE1", 0.75)
    song.add_note(t + 3,      "LANE1", 1)

    # MESURE 28 (p1 m22)
    t = 27 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 29 (p1 m23)
    t = 28 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 30 (p1 m24)
    t = 29 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 31
    t = 30 * 4 (p1 m25)
    song.add_note(t + 0,    "LANE1", 1.5)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 32 (p1 m26)
    t = 31 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 33 (p1 m27)
    t = 32 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 34 (p1 m28)
    t = 33 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 35 (p1 m29)
    t = 34 * 4
    song.add_note(t + 0,    "LANE1", 1.25)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1.5)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE1", 0.25)

    # MESURE 36 (p1 m30)
    t = 35 * 4
    song.add_note(t + 0,  "LANE1", 0.5)
    song.add_note(t + 0.5,  "LANE1", 0.5)
    song.add_note(t + 1,    "LANE1", 0.5)
    song.add_note(t + 1.5,  "LANE1", 0.5)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 37 (p1 m31)
    t = 36 * 4
    song.add_note(t + 0,    "LANE1", 2.75)
    song.add_note(t + 3, "LANE1", 0.25)
    song.add_note(t + 3.25, "LANE1", 0.25)
    song.add_note(t + 3.5,  "LANE1", 0.25)
    song.add_note(t + 3.75, "LANE1", 0.50)

    # MESURE 38 (p1 m32)
    t = 37 * 4
    song.add_note(t + 0,    "LANE1", 3.25)

    # MESURE 39
    t = 38 * 4

    # MESURE 40 (p2 m1)
    t = 39 * 4
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 41 (p2 m2)
    t = 40 * 4
    song.add_note(t + 0,  "LANE1", 1)
    song.add_note(t + 1,  "LANE1", 1)
    song.add_note(t + 2,  "LANE1", 1)
    song.add_note(t + 3,  "LANE1", 1)

    # MESURE 42 (p2 m3)
    t = 41 * 4
    song.add_note(t + 0,  "LANE1", 4)

    # MESURE 43
    t = 42 * 4


    # MESURE 44
    t = 43 * 4

    # MESURE 45
    t = 44 * 4

    # MESURE 46
    t = 45 * 4

    # MESURE 47
    t = 46 * 4

    # MESURE 48
    t = 47 * 4

    # MESURE 49
    t = 48 * 4

    # MESURE 50
    t = 49 * 4

    # MESURE 51
    t = 50 * 4

    # MESURE 52
    t = 51 * 4

    # MESURE 53 
    t = 52 * 4

    # MESURE 54 (p3 m1)
    t = 53 * 4
    song.add_note(t + 1.9,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 0.95)
    song.add_note(t + 3.95,    "LANE1", 0.75)

    # MESURE 55 (p3 m2)
    t = 54 * 4
    song.add_note(t + 0.65,    "LANE1", 0.25)
    song.add_note(t + 0.9, "LANE1", 3)

    # MESURE 56
    t = 55 * 4

    # MESURE 57 (p4 m1)
    t = 56 * 4
    song.add_note(t + 0.5,    "LANE1", 0.25)
    song.add_note(t + 1, "LANE1", 0.75)
    song.add_note(t + 2, "LANE1", 0.35)
    song.add_note(t + 2.5, "LANE1", 0.5)
    song.add_note(t + 3.5, "LANE1", 1.35)

    #MESURE 58 (p4 m2)
    t = 57 * 4

    # MESURE 59 (p5 m1)
    t = 58 * 4
    song.add_note(t + 1.5,    "LANE1", 0.15)
    song.add_note(t + 1.75,   "LANE1", 0.15)
    song.add_note(t + 2,      "LANE1", 0.75)
    song.add_note(t + 3,      "LANE1", 1)

    # MESURE 60 (p5 m2)
    t = 59 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 61 (p5 m3)
    t = 60 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 62 (p5 m4)
    t = 61 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 63 (p5 m5)
    t = 62 * 4
    song.add_note(t + 0,    "LANE1", 1.5)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 64 (p5 m6)
    t = 63 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 65 (p5 m7)
    t = 64 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 66 (p5 m8)
    t = 65 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 67 (p5 m9)
    t = 66 * 4
    song.add_note(t + 0,    "LANE1", 1.25)

    # MESURE 68
    t = 67 * 4

    # MESURE 69
    t = 68 * 4

    # MESURE 70
    t = 69 * 4

    # MESURE 71
    t = 70 * 4

    # MESURE 72
    t = 71 * 4

    # MESURE 73
    t = 72 * 4

    # MESURE 74
    t = 73 * 4

    # MESURE 75
    t = 74 * 4

    # MESURE 76
    t = 75 * 4

    # MESURE 77
    t = 76 * 4

    # MESURE 78 (p6 m1)
    t = 77 * 4
    song.add_note(t + 2,  "LANE1", 0.9)
    song.add_note(t + 2.9,  "LANE1", 1)

    # MESURE 79 (p6 m2)
    t = 78 * 4
    song.add_note(t + 0,  "LANE1", 0.7)
    song.add_note(t + 0.7,  "LANE1", 0.4)
    song.add_note(t + 0.9,  "LANE1", 2.85)

    # MESURE 80
    t = 79 * 4

    # MESURE 81 (p7 m1)
    t = 80 * 4
    song.add_note(t + 0.5,  "LANE1", 0.25)
    song.add_note(t + 1,  "LANE1", 0.75)
    song.add_note(t + 2,  "LANE1", 0.35)
    song.add_note(t + 2.5,  "LANE1", 0.5)
    song.add_note(t + 3.5,  "LANE1", 1.35)

    # MESURE 82 (p7 m2)
    t = 81 * 4

    # MESURE 83 (p8 m1)
    t = 82 * 4
    song.add_note(t + 1.5,    "LANE1", 0.15)
    song.add_note(t + 1.75,   "LANE1", 0.15)
    song.add_note(t + 2,      "LANE1", 0.75)
    song.add_note(t + 3,      "LANE1", 1)

    # MESURE 84 (p8 m2)
    t = 83 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 85 (p8 m3)
    t = 84 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 86 (p8 m4)
    t = 85 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 87 (p8 m5)
    t = 86 * 4
    song.add_note(t + 0,    "LANE1", 1.5)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1.25)

    # MESURE 88 (p8 m6)
    t = 87 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 1.5)

    # MESURE 89 (p8 m7)
    t = 88 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 90 (p8 m8)
    t = 89 * 4
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 0.15)
    song.add_note(t + 2.5,  "LANE1", 0.15)
    song.add_note(t + 3,    "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)

    # MESURE 91 (p8 m9)
    t = 90 * 4
    song.add_note(t + 0,    "LANE1", 1.25)
    song.add_note(t + 1.5,  "LANE1", 0.15)
    song.add_note(t + 1.75, "LANE1", 0.15)
    song.add_note(t + 2,    "LANE1", 1.5)
    song.add_note(t + 3.5,  "LANE1", 0.15)
    song.add_note(t + 3.75, "LANE1", 0.15)

    # MESURE 92 (p8 m10)
    t = 91 * 4
    song.add_note(t + 0,  "LANE1", 0.5)
    song.add_note(t + 0.5,  "LANE1", 0.5)
    song.add_note(t + 1,    "LANE1", 0.5)
    song.add_note(t + 1.5,  "LANE1", 0.5)
    song.add_note(t + 2,    "LANE1", 1)
    song.add_note(t + 3,    "LANE1", 1)

    # MESURE 93 (p8 m11)
    t = 92 * 4
    song.add_note(t + 0,    "LANE1", 2.75)
    song.add_note(t + 3, "LANE1", 0.15)
    song.add_note(t + 3.25, "LANE1", 0.15)
    song.add_note(t + 3.5,  "LANE1", 0.15)
    song.add_note(t + 3.75, "LANE1", 0.5)

    # MESURE 94 (p8 m12)
    t = 93 * 4
    song.add_note(t + 0,    "LANE1", 3.25)

    # MESURE 95 (p8 m13)
    t = 94 * 4
    song.add_note(t + 0.15,    "LANE1", 7.5)

    # MESURE 96 (p8 m14)
    t = 95 * 4

    # MESURE 97
    t = 96 * 4

    # MESURE 98

    

    return song