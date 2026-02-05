"""
Main Entry Point Module

Initializes and runs the game application.
Handles the welcome page and game startup.
"""

import pygame
from Views.WelcomePageView import WelcomPageView
from Utils.Logger import Logger


# === MAIN FUNCTION ===

def main():
    """
    Main entry point for the game application.
    Initializes pygame and starts the welcome page view.
    """
    try:
        Logger.debug("main.main", "Game application starting")
        
        # Pygame initialization is handled by WelcomePageView (single init point)
        
        # Create and run welcome page
        try:
            welcome_page = WelcomPageView(
                "Menu",
                800,
                800,
                0,  # Non-resizable (0 flags)
                "Game/Assets/welcomePage.png"
            )
            Logger.debug("main.main", "Welcome page created, starting run loop")
            welcome_page.run()
        except Exception as e:
            Logger.error("main.main", e)
            raise
        
        Logger.debug("main.main", "Game application ended normally")
        
    except KeyboardInterrupt:
        Logger.debug("main.main", "Game interrupted by user (KeyboardInterrupt)")
        try:
            pygame.quit()
        except Exception:
            pass
    except Exception as e:
        Logger.error("main.main", e)
        try:
            pygame.quit()
        except Exception:
            pass
        raise


# === ENTRY POINT ===

if __name__ == "__main__":
    main()



