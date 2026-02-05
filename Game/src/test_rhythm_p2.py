import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.CaracterModel import CaracterModel
from Models.RhythmModel import RhythmModel 
from Views.RhythmView import RhythmView
from Controllers.RhythmController import RhythmController

# --- 1. IMPORTER LES DEUX CHANSONS ---
from Songs.SevenNationArmy import load_seven_nation_army
from Songs.AnotherOneBitesTheDust import load_another_one

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    
    # --- 2. SÉLECTION DE LA MUSIQUE ---
    print("====================================")
    print("🎸 CHOISIS TA MUSIQUE :")
    print("1. Seven Nation Army (Tuto)")
    print("2. Another One Bites the Dust (Queen)")
    print("====================================")
    
    choix = input("Tape 1 ou 2 et valide : ")
    
    if choix == "2":
        selected_song = load_another_one()
        print("✅ Choix : QUEEN !")
    else:
        selected_song = load_seven_nation_army()
        print("✅ Choix : WHITE STRIPES !")

    screen_width = 1024 
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(f"CONCERT : {selected_song.name}")

    johnny = CaracterModel("Johnny Fuzz", x=0, y=0, type="PLAYER")
    johnny.setHealth(100) 
    rhythm_model = RhythmModel()
    rhythm_view = RhythmView(screen_width, screen_height)
    
    # --- 3. ON PASSE LA CHANSON CHOISIE AU CONTROLEUR ---
    try:
        # Note le dernier argument : selected_song
        controller = RhythmController(rhythm_model, johnny, screen_height, rhythm_view, selected_song)
        print("✅ Contrôleur chargé.")
    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        import traceback
        traceback.print_exc()
        return

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controller.handle_input(event)

        controller.update()

        if controller.game_over:
            # Petit délai avant de fermer
            pygame.time.delay(1000)
            running = False 

        screen.fill((0, 0, 0))
        
        current_countdown = controller.current_countdown_val if controller.waiting_to_start else 0
        
        rhythm_view.draw(
            screen, 
            rhythm_model, 
            johnny, 
            controller.note_speed, 
            countdown_val=current_countdown
        )
        
        pygame.display.flip()
        clock.tick(60) 

    if not controller.game_over:
        controller.end_concert()

    pygame.quit()

if __name__ == "__main__":
    main()