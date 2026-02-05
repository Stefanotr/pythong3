class SongModel:
    """
    Modèle de données représentant une chanson (Data Transfer Object).
    
    Responsabilités :
    1. Stocker les métadonnées (Artiste, BPM, Titre).
    2. Stocker les chemins des fichiers audio (Piste Guitare & Backing).
    3. Convertir les temps musicaux (Beats) en temps moteur (Millisecondes).
    4. Fournir une liste de notes triée chronologiquement au Contrôleur.
    """

    def __init__(self, name, artist, bpm, audio_file_guitar, audio_file_backing):
        """
        Initialise une nouvelle chanson.

        :param name: Titre de la chanson (ex: "Seven Nation Army").
        :param artist: Nom de l'artiste.
        :param bpm: Battements par minute (Tempo), crucial pour la synchro.
        :param audio_file_guitar: Chemin vers le fichier OGG de la guitare (Lead).
        :param audio_file_backing: Chemin vers le fichier OGG de l'instrumentale (Backing).
        """
        # --- MÉTADONNÉES ---
        self.name = name       # Important : utilisé pour le titre de la fenêtre pygame
        self.artist = artist
        self.bpm = bpm
        
        # --- FICHIERS AUDIO ---
        self.audio_guitar = audio_file_guitar
        self.audio_backing = audio_file_backing
        
        # --- DONNÉES DE JEU ---
        # Liste de dictionnaires contenant toutes les notes de la partition.
        # Structure d'une note : {'time': ms, 'lane': str, 'duration': ms, 'active': bool}
        self.notes = []

    def add_note(self, beat_start, lane, beat_duration=0.5):
        """
        Ajoute une note à la partition en utilisant la notation musicale (temps).
        Convertit automatiquement les temps en millisecondes.

        :param beat_start: Le temps où la note commence (ex: 0, 1.5, 4.0).
        :param lane: La colonne de la note ("LANE1", "LANE2", "LANE3", "LANE4").
        :param beat_duration: La durée de la note en temps (défaut: 0.5 = croche).
        """
        # 1. Calcul de la durée d'un temps en millisecondes
        # Formule : 60 secondes (60000 ms) / BPM
        ms_per_beat = 60000 / self.bpm
        
        # 2. Conversion Beats -> Millisecondes
        start_ms = int(beat_start * ms_per_beat)
        duration_ms = int(beat_duration * ms_per_beat)
        
        # 3. Création de l'objet Note
        new_note = {
            "time": start_ms,       # Moment exact d'apparition (hit time)
            "lane": lane,           # Colonne (Couleur)
            "duration": duration_ms,# Longueur de la queue (Sustain)
            "active": True,         # True = pas encore jouée, False = jouée/ratée
            "hit": False            # État du succès (optionnel pour le moment)
        }
        
        # 4. Ajout à la liste
        self.notes.append(new_note)

    def get_notes(self):
        """
        Retourne la liste des notes triée par ordre chronologique.
        C'est crucial pour que le jeu puisse traiter les notes dans l'ordre.
        
        :return: Liste de dictionnaires (notes).
        """
        # Tri sur la clé "time" (croissant)
        self.notes.sort(key=lambda x: x["time"])
        return self.notes