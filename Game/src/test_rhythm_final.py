import pygame
import sys
import os

# --- AJOUT DU CHEMIN ---
# Permet de trouver les modules même si on lance depuis src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.CaracterModel import CaracterModel
from Models.RhythmModel import RhythmModel 
from Views.RhythmView import RhythmView
from Controllers.RhythmController import RhythmController

def main():
    # Correction Latence Audio (Important pour le rythme !)
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    
    # 1. Configuration Écran
    info = pygame.display.Info()
    screen_width = 1024 
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TEST RHYTHM - MODE CONCERT")

    # 2. Création des Modèles
    # Johnny (Sa vie importe peu ici, c'est la Hype qui compte)
    johnny = CaracterModel("Johnny Fuzz", x=0, y=0, type="PLAYER")
    johnny.setHealth(100) 
    
    # Modèle Rythme
    rhythm_model = RhythmModel()
    
    # 3. Création de la Vue
    rhythm_view = RhythmView(screen_width, screen_height)
    
    # 4. Création du Contrôleur
    try:
        controller = RhythmController(rhythm_model, johnny, screen_height, rhythm_view)
        print("✅ Contrôleur chargé.")
        print("🎸 Mode : CONCERT (Gagnez du Cash !)")
        print("🔊 Protection Audio : ACTIVÉE")
        print("😈 Fausses Notes : ACTIVÉES")
    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        return

    # 5. Boucle de Jeu
    clock = pygame.time.Clock()
    running = True
    
    print("--- DÉBUT DU TEST ---")
    print("Touches : C, V, B, N")

    while running:
        # A. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Input Joueur
            controller.handle_input(event)

        # B. Mise à jour Logique
        controller.update()

        # C. Vérification Game Over (Tomates)
        if controller.game_over:
            print("💀 GAME OVER : Le public vous a viré !")
            running = False # On arrête le test

        # D. Dessin
        screen.fill((0, 0, 0))
        
        # --- MODIFICATION ICI ---
        # On calcule si on doit afficher le décompte
        current_countdown = controller.current_countdown_val if controller.waiting_to_start else 0
        
        # On passe 'countdown_val' à la vue !
        rhythm_view.draw(
            screen, 
            rhythm_model, 
            johnny, 
            controller.note_speed, 
            countdown_val=current_countdown
        )
        
        pygame.display.flip()
        clock.tick(60) 

    # Fin du test
    if not controller.game_over:
        # On simule la fin pour voir le gain
        controller.end_concert()

    pygame.quit()

if __name__ == "__main__":
    main()