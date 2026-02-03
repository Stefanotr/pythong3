import pygame
from Models.CaracterModel import CaracterModel
from Models.BottleModel import BottleModel
from GuitarModel import GuitarFactory
from Controllers.CombatModel import CombatModel
from CombatController import CombatController
from CombatView import CombatView
from Utils.Logger import Logger

class Act1View:
    """
    Acte I : Le Bar "Le Gosier Sec"
    Combat contre Gros Bill
    """
    def __init__(self, screen):
        self.screen = screen
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        Logger.debug("Act1View.__init__", "Starting Act 1: Le Gosier Sec")
        
        # === CRÉER JOHNNY (JOUEUR) ===
        self.johnny = CaracterModel("Johnny Fuzz", 60, 60, "PLAYER")
        self.johnny.setHealth(100)
        self.johnny.setDamage(10)
        self.johnny.setAccuracy(0.85)  # 85% de précision
        self.johnny.setDrunkenness(0)
        self.johnny.setComaRisk(10)
        
        # Équiper Johnny avec La Pelle (guitare de départ)
        la_pelle = GuitarFactory.create_la_pelle()
        Logger.debug("Act1View.__init__", f"Johnny equipped with {la_pelle.getName()}")
        
        # Donner une bouteille à Johnny
        beer = BottleModel("Bière", 15, 3, 5)
        self.johnny.setSelectedBottle(beer)
        
        # === CRÉER GROS BILL (BOSS) ===
        self.gros_bill = CaracterModel("Gros Bill", 80, 80, "BOSS")
        self.gros_bill.setHealth(80)
        self.gros_bill.setDamage(8)
        self.gros_bill.setAccuracy(0.75)  # 75% de précision
        
        Logger.debug("Act1View.__init__", 
                    f"Boss created: {self.gros_bill.getName()}",
                    boss_hp=self.gros_bill.getHealth(),
                    boss_damage=self.gros_bill.getDamage())
        
        # === INITIALISER LE COMBAT ===
        self.combat_model = CombatModel(self.johnny, self.gros_bill)
        self.combat_controller = CombatController(self.combat_model)
        self.combat_view = CombatView(self.screen_width, self.screen_height)
        
        # === ÉTAT DE L'ACTE ===
        self.act_finished = False
        self.victory = False
        
        # === INTRO ===
        self.show_intro = True
        self.intro_timer = 180  # 3 secondes à 60fps
        
        Logger.debug("Act1View.__init__", "Act 1 initialized successfully")
    
    def run(self):
        """Boucle principale de l'Acte 1"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                # Intro
                if self.show_intro:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.show_intro = False
                        Logger.debug("Act1View.run", "Intro skipped")
                
                # Combat
                elif not self.combat_model.isCombatFinished():
                    self.combat_controller.handleInput(event)
                
                # Fin du combat
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        running = False
            
            # Mettre à jour
            if self.show_intro:
                self.intro_timer -= 1
                if self.intro_timer <= 0:
                    self.show_intro = False
            else:
                self.combat_controller.update()
            
            # Dessiner
            if self.show_intro:
                self.draw_intro()
            else:
                self.combat_view.draw(self.screen, self.combat_model)
            
            pygame.display.flip()
            clock.tick(60)
        
        # Déterminer le résultat
        if self.combat_model.getWinner() == "PLAYER":
            Logger.debug("Act1View.run", "Act 1 completed - VICTORY")
            return "ACT2"  # Passer à l'acte 2
        else:
            Logger.debug("Act1View.run", "Act 1 completed - DEFEAT")
            return "GAME_OVER"
    
    def draw_intro(self):
        """Dessiner l'intro de l'Acte 1"""
        # Fond noir
        self.screen.fill((10, 10, 15))
        
        # Fonts
        title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
        text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.025))
        small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
        
        # Titre
        title_text = "🎸 ACTE I : LE GOSIER SEC 🍺"
        title_surf = title_font.render(title_text, True, (255, 215, 0))
        title_shadow = title_font.render(title_text, True, (100, 80, 0))
        
        title_x = self.screen_width // 2 - title_surf.get_width() // 2
        title_y = self.screen_height // 4
        
        self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
        self.screen.blit(title_surf, (title_x, title_y))
        
        # Histoire
        story_lines = [
            "Tu es Johnny Fuzz, rockstar sur le déclin.",
            "",
            "Le patron du bar refuse de te payer",
            "tant que tu n'auras pas viré les motards",
            "qui squattent la scène.",
            "",
            "Affronte Gros Bill, le chef des motards,",
            "et prouve que tu es encore une légende !"
        ]
        
        story_y = title_y + 120
        for line in story_lines:
            if line:
                line_surf = text_font.render(line, True, (220, 220, 220))
                line_x = self.screen_width // 2 - line_surf.get_width() // 2
                self.screen.blit(line_surf, (line_x, story_y))
            story_y += 40
        
        # Instructions
        instruction = "Appuie sur ESPACE pour commencer"
        inst_surf = small_font.render(instruction, True, (150, 150, 150))
        inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
        self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
        
        # Animation de clignotement
        if (self.intro_timer // 30) % 2 == 0:
            skip_text = "(ou attends 3 secondes)"
            skip_surf = small_font.render(skip_text, True, (100, 100, 100))
            skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
            self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))


# === TEST STANDALONE ===
if __name__ == "__main__":
    pygame.init()
    
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    pygame.display.set_caption("Acte 1 - Le Gosier Sec")
    
    act1 = Act1View(screen)
    result = act1.run()
    
    print(f"Résultat de l'Acte 1 : {result}")
    
    pygame.quit()