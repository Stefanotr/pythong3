import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.CaracterModel import CaracterModel
from Models.RhythmModel import RhythmModel 
from Views.RhythmCombatView import RhythmCombatView
from Controllers.RhythmCombatController import RhythmCombatController

def main():
    """
    TEST DU MODE COMBAT RHYTHM
    """
    # Correction Latence Audio
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    
    # Configuration Écran
    screen_width = 1024 
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TEST RHYTHM COMBAT - BOSS FINAL")

    # === CRÉATION DES COMBATTANTS ===
    
    # Johnny (Joueur)
    johnny = CaracterModel("Johnny Fuzz", x=0, y=0, type="PLAYER")
    johnny.setHealth(100)
    johnny.setDamage(10)  # Pas utilisé ici, c'est le rythme qui compte
    
    # Boss Final
    boss = CaracterModel("Le Manager Corrompu", x=0, y=0, type="BOSS")
    boss.setHealth(100)  # Ajuste selon la difficulté voulue
    boss.setDamage(10)   # Utilisé pour les MISS
    
    # Modèle Rythme
    rhythm_model = RhythmModel()
    
    # Vue spéciale combat
    combat_view = RhythmCombatView(screen_width, screen_height)
    
    # Contrôleur de combat rhythm
    try:
        controller = RhythmCombatController(
            rhythm_model, 
            johnny, 
            boss, 
            screen_height, 
            combat_view
        )
        print("✅ Contrôleur Combat Rhythm chargé.")
        print("🎸⚔️ Mode : BOSS COMBAT")
        print("📜 Règles :")
        print("   - Bonnes notes → Dégâts au BOSS")
        print("   - MISS → Dégâts au JOUEUR + Boss récupère HP")
        print("   - Victoire si Boss K.O.")
        print("   - Défaite si Joueur K.O. OU Boss survit")
    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        import traceback
        traceback.print_exc()
        return

    # Boucle de Jeu
    clock = pygame.time.Clock()
    running = True
    
    print("--- DÉBUT DU COMBAT ---")

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            controller.handle_input(event)

        # Mise à jour
        controller.update()

        # Vérification Game Over
        if controller.game_over:
            print("\n=== FIN DU COMBAT ===")
            if controller.victory:
                print("🏆 VICTOIRE !")
            else:
                print("💀 DÉFAITE !")
            
            # Attendre 3 secondes avant de fermer
            pygame.time.wait(3000)
            running = False

        # Dessin
        screen.fill((0, 0, 0))
        
        # Calcul du countdown
        current_countdown = controller.current_countdown_val if controller.waiting_to_start else 0
        
        # Dessiner la vue de combat
        combat_view.draw(
            screen, 
            rhythm_model, 
            johnny,
            boss,
            controller.note_speed, 
            countdown_val=current_countdown
        )
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()