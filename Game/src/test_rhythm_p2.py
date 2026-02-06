import pygame
import sys
import os

# Ajout du chemin racine pour trouver les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.CaracterModel import CaracterModel
from Models.RhythmModel import RhythmModel 
from Views.RhythmView import RhythmView
from Controllers.RhythmController import RhythmController

# --- 1. IMPORTER LES TROIS CHANSONS ---
# Assure-toi que les fichiers existent bien dans Assets/Songs/
from Songs.SevenNationArmy import load_seven_nation_army
from Songs.AnotherOneBitesTheDust import load_another_one
from Songs.TheFinalCountdown import load_final_countdown

def main():
    # Correction Latence Audio
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    
    # --- 2. SÉLECTION DE LA MUSIQUE ---
    print("\n====================================")
    print("🎸 CHOISIS TA MUSIQUE :")
    print("1. Seven Nation Army (The White Stripes)")
    print("2. Another One Bites the Dust (Queen)")
    print("3. The Final Countdown (Europe)")
    print("====================================")
    
    choix = input("Tape 1, 2 ou 3 et valide avec Entrée : ")
    
    selected_song = None
    
    if choix == "3":
        selected_song = load_final_countdown()
        print("✅ Choix : EUROPE (C'est parti pour le synthé !)")
    elif choix == "2":
        selected_song = load_another_one()
        print("✅ Choix : QUEEN (Attention à la basse !)")
    else:
        # Par défaut on charge Seven Nation Army
        selected_song = load_seven_nation_army()
        print("✅ Choix : WHITE STRIPES (Tuto)")

    # --- 3. LANCEMENT DU JEU ---
    screen_width = 1024 
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(f"CONCERT : {selected_song.name} - {selected_song.artist}")

    # Initialisation des Modèles
    johnny = CaracterModel("Johnny Fuzz", x=0, y=0, type="PLAYER")
    johnny.setHealth(100) 
    rhythm_model = RhythmModel()
    rhythm_view = RhythmView(screen_width, screen_height)
    
    # Création du Contrôleur avec la chanson choisie
    try:
        controller = RhythmController(rhythm_model, johnny, screen_height, rhythm_view, selected_song)
        print("✅ Contrôleur chargé avec succès.")
    except Exception as e:
        print(f"❌ Erreur critique au chargement : {e}")
        import traceback
        traceback.print_exc()
        return

    clock = pygame.time.Clock()
    running = True
    
    print("--- DÉBUT DU CONCERT ---")
    print("Touches : C (Vert), V (Rouge), B (Jaune), N (Bleu)")

    # --- BOUCLE DE JEU ---
    while running:
        # A. Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # On passe les inputs au contrôleur
            controller.handle_input(event)

        # B. Mise à jour (Logique)
        controller.update()

        # C. Vérification Fin de partie
        if controller.game_over:
            # Petit délai pour laisser comprendre le joueur
            pygame.time.delay(1000)
            running = False 

        # D. Dessin
        screen.fill((0, 0, 0)) # Fond noir
        
        # Gestion de l'affichage du décompte
        current_countdown = controller.current_countdown_val if controller.waiting_to_start or controller.is_paused else 0
        
        rhythm_view.draw(
            screen, 
            rhythm_model, 
            johnny, 
            controller.note_speed, 
            countdown_val=current_countdown
        )
        
        pygame.display.flip()
        clock.tick(60) 

    # Fin du programme
    if not controller.game_over:
        controller.end_concert()

    pygame.quit()

if __name__ == "__main__":
    main()