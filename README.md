# Login
username:admin
password:admin123


# Six-String Hangover

A rhythm-based puzzle adventure game where the player must defeat enemies through rhythm combat and navigate a town to reach different acts.

## Game Overview

- **Genre**: Rhythm Puzzle Adventure
- **Platform**: PC (Python/Pygame)
- **Status**: In Development
- **Version**: 1.0.0
- **Last Updated**: February 8, 2026

## Controls

### General Controls
- **ESCAPE** - Open/Close Pause Menu
- **Arrow Keys / WASD** - Move character
- **E** - Interact with objects (enter shop, start dialogue)
- **SPACE** - Confirm/Continue actions, launch transitions

### Rhythm Combat Controls
- **C** - Lane 1
- **V** - Lane 2
- **B** - Lane 3
- **N** - Lane 4

### Dialogue/Choices
- **LEFT/UP arrow** - Previous choice
- **RIGHT/DOWN arrow** - Next choice
- **SPACE** - Select choice

## Hidden Commands (Testing & Debug)

### Testing Commands
- **P** - Add 1000 money to player (for testing shop system)

### Debug Commands
- **F11** - Toggle fullscreen mode
- **F1** - Toggle debug overlay (shows map info, collision rects, shop positions)
- **1-8** - Jump directly to any stage/act (bypasses normal progression)
  - 1 = Act 1
  - 2 = Act 2
  - 3 = Rhythm Combat
  - 4-8 = Additional stages (if available)

## Game Structure

### Views (Screens)
- **WelcomePageView** - Main menu
- **MapPageView** - Overworld navigation
- **Act1View / Act2View** - Story sequences
- **RhythmCombatView** - Rhythm-based combat encounters
- **ShopPageView** - Beverage/item shop
- **PauseMenuView** - Pause menu overlay

### Game States
- MAP - Overworld exploration
- ACT1 - First story act
- ACT2 - Second story act
- RHYTHM - Rhythm combat
- SHOP - Shop interaction
- QUIT - Exit game

## Features

### Map System
- Tile-based map loaded from TMX format
- Multiple tilesets support
- Tile flip transformations (horizontal/vertical mirroring)
- Object layers for:
  - Shop locations (randomly chosen for drink menu)
  - Building collisions (ville layer)
  - Vehicle positions (voiture layer - visual only)
- Camera system that follows the player

### Shop System
- Multiple shops on the map
- One randomly selected shop opens the drink menu each playthrough
- Shows "OPEN" for the active drink shop
- Shows "CLOSED" for inactive shops
- Drink shop door detection and auto-entry

### Collision System
- World collision rectangles loaded from TMX object layers
- Player collision detection with buildings
- Door interaction zones with forgiveness inflation

### Player Progression
- Drunkenness tracking
- Coma risk management
- Inventory system for bottles/items
- Currency system for purchases
- Level progression through acts

## Project Structure

```
Game/
├── src/
│   ├── main.py                 # Entry point
│   ├── Controllers/            # Game logic controllers
│   ├── Models/                 # Data models
│   ├── Views/                  # Display/UI views
│   ├── Songs/                  # Rhythm song definitions
│   ├── Utils/                  # Utilities (Logger, etc)
│   └── __init__.py
├── Assets/
│   ├── maps/                   # TMX map files and tilesets
│   └── Sounds/                 # Audio files
└── logs/                       # Debug and error logs
```

## Installation & Running

### Requirements
- Python 3.8+
- Pygame
- xml.etree.ElementTree (standard library)

### Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install pygame

# Run the game
python Game/src/main.py
```

### Debug Logs
Debug and error logs are saved in `Game/logs/` with timestamps. Check recent logs if encountering issues.

## Development Notes

### Map Format (TMX)
The game uses Tiled Map Editor format (.tmx files):
- Multiple tileset support with automatic loading
- Object layers for dynamic content placement:
  - `shop` layer - Beverage shop locations
  - `ville` layer - Building collision obstacles
  - `voiture` layer - Vehicle positions (visual reference)

### Hidden Features During Development
- Yellow shop access square is hidden but code is preserved (can be re-enabled)
- Debug overlay shows real-time map information
- Stage skip shortcuts for rapid testing
- Money cheat for testing shop interactions

## Known Issues & TODOs

- [ ] Complete NPC dialogue system
- [ ] Implement all boss encounters
- [ ] Sound effects integration
- [ ] Music sync with rhythm combat
- [ ] Additional acts/stages
- [ ] Mobile/controller support

## Documentation

- [API Documentation](docs/API.md) - Complete class and method reference with detailed descriptions
- [Game Design Document](docs/SCENARIO.md) - Game story and design specifications

## Credits

- **Game Design & Development**: Team Six-String

---

*Last Updated: February 8, 2026*

