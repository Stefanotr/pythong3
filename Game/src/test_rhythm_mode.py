"""
SIX-STRING HANGOVER
===================
Un jeu de rythme et de combat créé pour la Piscine Python

Par : [Ton Nom]

Lancer ce fichier pour jouer !
"""

from GameController import GameController

def main():
    """Point d'entrée principal du jeu"""
    print("=" * 60)
    print("🎸 SIX-STRING HANGOVER 🍺")
    print("=" * 60)
    print()
    print("Bienvenue dans la tournée de la déchéance !")
    print("Prépare-toi à affronter des motards, des fans enragés")
    print("et ton propre taux d'alcoolémie...")
    print()
    print("=" * 60)
    print()
    
    try:
        game = GameController()
        game.run()
        
        print()
        print("Merci d'avoir joué ! 🎸")
        print()
        
    except KeyboardInterrupt:
        print()
        print("Interruption du jeu. À bientôt ! 🎸")
    except Exception as e:
        print()
        print(f"❌ Erreur fatale : {e}")
        print("Consulte les logs pour plus d'infos.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()