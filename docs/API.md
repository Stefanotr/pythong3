# Six-String Hangover - API Documentation

Complete reference for all classes, methods, and attributes in the game engine.

---

## Table of Contents

1. [Models](#models)
2. [Views](#views)
3. [Controllers](#controllers)
4. [Utilities](#utilities)

---

## MODELS

Data models representing game entities and game state.

### BottleModel

Represents a beverage item that can affect player stats.

```python
class BottleModel:
    def __init__(name: str, alcohol_level: int, bonus_damage: int, accuracy_penalty: int)
```

**Attributes:**
- `_name`: str - Bottle name/type
- `_alcohol_level`: int - Drunkenness increase when consumed
- `_bonus_damage`: int - Damage bonus provided to player
- `_accuracy_penalty`: int - Accuracy reduction when drunk

**Methods:**
- `getName() -> str` - Get bottle name
- `setName(name: str) -> None` - Set bottle name
- `getAlcoholLevel() -> int` - Get alcohol content
- `setAlcoholLevel(level: int) -> None` - Set alcohol content
- `getBonusDamage() -> int` - Get damage bonus
- `setBonusDamage(damage: int) -> None` - Set damage bonus
- `getAccuracyPenalty() -> int` - Get accuracy penalty
- `setAccuracyPenalty(penalty: int) -> None` - Set accuracy penalty

---

### BossModel

Represents a boss enemy in combat.

```python
class BossModel(CaracterModel):
    def __init__(name: str, x: int = 175, y: int = 175)
```

**Inherits from:** CaracterModel

**Methods:**
- `@classmethod from_config(boss_config: dict, x: int, y: int) -> BossModel` - Create boss from config dictionary
- `scale(player: PlayerModel) -> None` - Scale boss difficulty based on player level

**Type Checking:**
- If `boss_config` is not a dictionary, returns default boss to prevent crashes

---

### CaracterModel

Base class for all characters (player and enemies).

```python
class CaracterModel:
    def __init__(name: str, x: int, y: int, type: str = "character")
```

**Attributes:**
- `_type`: str - Character type identifier
- `_name`: str - Character name
- `_x`: int - X coordinate position
- `_y`: int - Y coordinate position
- `_health`: int - Current health points
- `_damage`: int - Base damage stat
- `_accuracy`: float - Attack accuracy percentage
- `_drunkenness`: int - Drunkenness level (0-100)
- `_coma_risk`: int - Risk of falling into coma
- `_selected_bottle`: BottleModel - Currently held bottle
- `_current_action`: str - Current action being performed
- `_action_timer`: int - Frames remaining for current action
- `_currency`: int - Money/currency amount

**Methods:**
- `getType() -> str` - Get character type
- `setType(type: str) -> None` - Set character type
- `getName() -> str` - Get character name
- `setName(name: str) -> None` - Set character name
- `getX() -> int` - Get X position
- `setX(x: int) -> None` - Set X position
- `getY() -> int` - Get Y position
- `setY(y: int) -> None` - Set Y position
- `getHealth() -> int` - Get current health
- `setHealth(health: int) -> None` - Set health
- `getDamage() -> int` - Get damage stat
- `setDamage(damage: int) -> None` - Set damage stat
- `getAccuracy() -> float` - Get accuracy percentage
- `setAccuracy(accuracy: float) -> None` - Set accuracy percentage
- `getCurrentAction() -> str` - Get current action
- `setCurrentAction(action: str, duration: int) -> None` - Set action with duration
- `getActionTimer() -> int` - Get remaining action frames
- `updateActionTimer() -> None` - Decrement action timer
- `getDrunkenness() -> int` - Get drunkenness level
- `setDrunkenness(level: int) -> None` - Set drunkenness level
- `@staticmethod attack(char1: CaracterModel, char2: CaracterModel) -> None` - Perform attack between two characters

---

### PlayerModel

Represents the player character with inventory and progression.

```python
class PlayerModel(CaracterModel):
    def __init__(name: str, x: int, y: int)
```

**Inherits from:** CaracterModel

**Additional Attributes:**
- `_coma_risk`: int - Risk percentage of falling into coma
- `_selected_bottle`: BottleModel - Currently selected bottle
- `_drunkenness`: int - Player drunkenness level
- `_level`: int - Player progression level
- `inventory`: InventoryModel - Player's inventory system

**Additional Methods:**
- `getComaRisk() -> int` - Get coma risk percentage
- `setComaRisk(risk: int) -> None` - Set coma risk
- `getSelectedBottle() -> BottleModel` - Get current bottle
- `setSelectedBottle(bottle: BottleModel) -> None` - Set current bottle
- `getLevel() -> int` - Get player level
- `setLevel(level: int) -> None` - Set player level
- `drink(bottle: BottleModel) -> None` - Consume a bottle

---

### CombatModel

Manages combat state between player and enemy.

```python
class CombatModel:
    def __init__(player: PlayerModel, enemy: CaracterModel)
```

**Attributes:**
- `_player`: PlayerModel - Player character in combat
- `_enemy`: CaracterModel - Enemy character in combat
- `_player_max_health`: int - Player's starting health
- `_enemy_max_health`: int - Enemy's starting health
- `_turn`: int - Current turn number
- `_is_player_turn`: bool - Whether it's player's turn
- `_combat_log`: list - History of combat actions
- `_combat_finished`: bool - Combat end state
- `_winner`: str - "player" or "enemy"
- `_player_status`: dict - Player status effects
- `_enemy_status`: dict - Enemy status effects

**Methods:**
- `getPlayer() -> PlayerModel` - Get player character
- `getEnemy() -> CaracterModel` - Get enemy character
- `getPlayerMaxHealth() -> int` - Get player max health
- `getEnemyMaxHealth() -> int` - Get enemy max health
- `getTurn() -> int` - Get current turn
- `setTurn(turn: int) -> None` - Set turn
- `incrementTurn() -> None` - Increase turn counter
- `isPlayerTurn() -> bool` - Check if player's turn

---

### RhythmModel

Manages rhythm game state and scoring.

```python
class RhythmModel:
    def __init__()
```

**Attributes:**
- `score`: int - Current score
- `combo`: int - Current hit combo count
- `max_combo`: int - Best combo achieved
- `total_hits`: int - Total successful hits
- `crowd_satisfaction`: int - Crowd mood/satisfaction level
- `cash_earned`: int - Money earned this session
- `feedback`: str - Current feedback message
- `feedback_timer`: int - Frames to display feedback
- `hit_line_y`: int - Y position of hit detection line
- `lanes`: list - Lane configurations
- `notes`: list - Active notes to hit

**Methods:**
- `get_crowd_status() -> str` - Get crowd satisfaction description
- `reset() -> None` - Reset all scores and state

---

### ShopModel

Manages shop inventory and transactions.

```python
class ShopModel:
    def __init__(player: PlayerModel)
```

**Attributes:**
- `player`: PlayerModel - Player shopping
- `available_items`: list - List of items available for purchase

---

### MapModel

Represents the game map with tiles and objects.

```python
class MapModel:
    def __init__(map_file: str, tile_kinds: list, tile_size: int)
```

**Attributes:**
- `tile_kinds`: dict - Tile type definitions
- `tile_size`: int - Size of each tile in pixels
- `tiles`: list - 2D array of tile data
- `layer_ordered`: list - Ordered layer list
- `object_layers`: dict - Named object layers (shop, ville, voiture)
- `width`: int - Map width in tiles
- `height`: int - Map height in tiles

**Methods:**
- `get_spawn_points() -> list` - Get valid spawn locations from TMX

---

### LoginModel

Manages user authentication.

```python
class LoginModel:
    def __init__()
```

**Attributes:**
- `user_manager`: UserManager - User authentication system
- `current_user`: str - Currently logged in user
- `is_admin`: bool - Admin status
- `login_error`: str - Login error message
- `registration_error`: str - Registration error message

**Methods:**
- `login(username: str, password: str) -> bool` - Authenticate user
- `register(username: str, password: str, password_confirm: str) -> bool` - Create new account

---

### InventoryModel

Manages player item inventory.

```python
class InventoryModel:
    def __init__()
```

**Attributes:**
- `items`: list - List of items in inventory
- `selected_index`: int - Currently selected item index
- `max_slots`: int - Maximum inventory capacity

**Methods:**
- `add_item(item: BottleModel) -> bool` - Add item to inventory
- `remove_item(name: str) -> BottleModel` - Remove item by name
- `consume_selected() -> BottleModel` - Use selected item
- `get_all_items() -> list` - Get all items
- `get_selected_item() -> BottleModel` - Get current item
- `get_selected_index() -> int` - Get selection index
- `count_by_type() -> dict` - Count items by type
- `get_unique_bottles() -> list` - Get unique item types
- `select_next() -> None` - Select next item
- `select_prev() -> None` - Select previous item

---

### GuitarModel

Represents a guitar weapon with special effects.

```python
class GuitarModel:
    def __init__(name: str, base_damage: int, special_effect: str, effect_chance: int)
```

**Attributes:**
- `_name`: str - Guitar name
- `_base_damage`: int - Base damage value
- `_special_effect`: str - Special effect description
- `_effect_chance`: int - Chance to trigger effect (0-100)

**Methods:**
- `getName() -> str` - Get guitar name
- `setName(name: str) -> None` - Set guitar name
- `getBaseDamage() -> int` - Get damage stat
- `setBaseDamage(damage: int) -> None` - Set damage stat
- `getSpecialEffect() -> str` - Get special effect
- `setSpecialEffect(effect: str) -> None` - Set special effect
- `getEffectChance() -> int` - Get effect trigger chance
- `setEffectChance(chance: int) -> None` - Set effect trigger chance
- `getDescription() -> str` - Get full description

**GuitarFactory Class:**
- `@staticmethod createLaPelle() -> GuitarModel` - Create basic guitar
- `@staticmethod createElectroChoc() -> GuitarModel` - Create electric shock guitar
- `@staticmethod createHacheDeGuerre() -> GuitarModel` - Create war axe guitar

---

### SongModel

Represents a playable rhythm song.

```python
class SongModel:
    def __init__(name: str, artist: str, bpm: int, audio_file_guitar: str, audio_file_backing: str)
```

**Attributes:**
- `name`: str - Song title
- `artist`: str - Artist name
- `bpm`: int - Beats per minute
- `audio_guitar`: str - Path to guitar audio track
- `audio_backing`: str - Path to backing track audio
- `notes`: list - List of note timing data

**Methods:**
- `add_note(beat_start: int, lane: int, beat_duration: int) -> None` - Add note to song
- `get_notes() -> list` - Get all notes in song

---

### TileModel

Represents a single tile type.

```python
class TileModel:
    def __init__(name: str, image: str, is_solid: bool)
```

**Attributes:**
- `name`: str - Tile type name
- `is_solid`: bool - Whether tile blocks movement
- `image`: pygame.Surface - Tile image texture

**Methods:**
- `getName() -> str` - Get tile name
- `setName(name: str) -> None` - Set tile name
- `getImage() -> pygame.Surface` - Get tile texture
- `setImage(image: str) -> None` - Set tile texture
- `isSolid() -> bool` - Check if solid
- `setSolid(solid: bool) -> None` - Set solidity

---

### BuildingModel

Placeholder for building data.

```python
class BuildingModel:
    def __init__()
```

*(Currently empty - reserved for future expansion)*

---

## VIEWS

UI and rendering components.

### PageView

Base class for all game pages/screens.

```python
class PageView:
    def __init__(name: str, width: int, height: int, flags: int, background_image: str)
```

**Attributes:**
- `name`: str - Page name/title
- `width`: int - Screen width
- `height`: int - Screen height
- `screen`: pygame.Surface - Game display surface
- `background`: pygame.Surface - Background image
- `resizable`: int - Pygame window flags

**Methods:**
- `set_window_size(width: int, height: int, flags: int) -> None` - Resize window
- `load_background(path: str) -> None` - Load background image
- `update_background() -> None` - Refresh background
- `handle_window_resize(new_width: int, new_height: int) -> None` - Handle resize events

---

### ButtonView

Represents a clickable button on screen.

```python
class ButtonView:
    def __init__(image_path: str, position: tuple, size: tuple)
```

**Attributes:**
- `image`: pygame.Surface - Button texture
- `rect`: pygame.Rect - Button hit box

**Methods:**
- `draw(screen: pygame.Surface) -> None` - Draw button
- `set_position(position: tuple) -> None` - Move button
- `is_clicked(mouse_pos: tuple) -> bool` - Check if clicked

---

### CaracterView

Renders character sprites with animations.

```python
class CaracterView:
    def __init__(image_path: str, base_name: str, sprite_size: tuple, character_config: dict, game_mode: str)
```

**Attributes:**
- `base_image_path`: str - Path to character image
- `base_name`: str - Character identifier
- `sprite`: pygame.Surface - Current sprite texture
- `sprite_size`: tuple - (width, height) in pixels
- `animation_frame`: int - Current animation frame
- `animation_speed`: int - Frames per animation cycle
- `action_sprites`: dict - Sprites for different actions

**Methods:**
- `_loadSprite(path: str) -> None` - Load sprite from file
- `resetToBaseSprite() -> None` - Reset to base appearance
- `_getActionImagePath(base_name: str, action: str) -> str` - Get action sprite path
- `loadActionSprite(action: str, path: str) -> None` - Load action sprite
- `update(action: str, drunkenness: int, combo: int) -> None` - Update sprite based on state
- `draw(screen: pygame.Surface, x: int, y: int) -> None` - Draw character
- `drawHealthBar(screen, x, y, max_health, current_health) -> None` - Render health bar

---

### CombatView

Renders combat interface.

```python
class CombatView:
    def __init__(screen_width: int, screen_height: int, background_image_path: str)
```

**Attributes:**
- `screen_width`: int - Display width
- `screen_height`: int - Display height
- `background_image`: pygame.Surface - Combat background
- `time`: int - Frame counter for animations

**Methods:**
- `draw(screen: pygame.Surface, combat: CombatModel) -> None` - Render entire combat screen
- `drawBackground(screen) -> None` - Draw background
- `drawTitle(screen, combat) -> None` - Draw title
- `drawFightersInfo(screen, combat) -> None` - Draw fighter stats
- `drawCombatLog(screen, combat) -> None` - Draw action log
- `drawActions(screen, combat, x, y) -> None` - Draw action buttons

---

### InventoryView

Renders player inventory display.

```python
class InventoryView:
    def __init__(screen_width: int, screen_height: int)
```

**Methods:**
- `draw_inventory_display(screen, inventory, x, y) -> None` - Draw inventory in game
- `draw_shop_inventory(screen, inventory, x, y) -> None` - Draw inventory in shop

---

### MapView

Renders the game map.

```python
class MapView:
    def __init__(map: MapModel)
```

**Methods:**
- `draw(screen: pygame.Surface, offset: tuple) -> None` - Draw map with camera offset

---

### MapPageView

Main overworld/map screen.

```python
class MapPageView(PageView):
    def __init__(screen: pygame.Surface, current_act: int, player: PlayerModel, sequence_controller: GameSequenceController)
```

**Attributes:**
- `lola`: PlayerModel - Player character
- `current_act`: int - Current act number (1-3)
- `map`: MapModel - Game map
- `player_view`: CaracterView - Player sprite renderer
- `shops`: list - List of shops on map
- `drink_shop_index`: int - Which shop is open
- `world_collision_rects`: list - Collision rectangles

**Methods:**
- `run() -> str` - Main game loop, returns next state
- `drawTransitionPrompt() -> None` - Show act transition prompt
- `drawShopPrompt() -> None` - Show shop entry prompt
- `_run_shop() -> str` - Run shop interaction
- `_drawShopBuilding(offset) -> None` - Draw shop on map
- `_drawLevelDisplay() -> None` - Draw level/stats
- `_toggle_fullscreen() -> None` - Toggle fullscreen mode

---

### Act1View / Act2View

Story/dialogue screens for acts.

```python
class ActView(PageView):
    def __init__(screen: pygame.Surface, player: PlayerModel, sequence_controller: GameSequenceController, act_config: dict)
```

**Methods:**
- `run() -> str` - Main loop, returns next state
- `@classmethod create_act2() -> ActView` - Factory for Act 2

---

### RhythmView

Renders rhythm game UI.

```python
class RhythmView:
    def __init__(screen_width: int, screen_height: int, background_image_path: str, character_view: CaracterView)
```

**Methods:**
- `create_particles(x, y, color) -> None` - Create visual effect
- `update_particles() -> None` - Update particle animations
- `draw(screen, rhythm: RhythmModel) -> None` - Render entire rhythm screen

---

### RhythmPageView

Standalone rhythm game page.

```python
class RhythmPageView(PageView):
    def __init__(screen: pygame.Surface, player: PlayerModel, sequence_controller: GameSequenceController, context: dict)
```

**Methods:**
- `run() -> str` - Main rhythm game loop

---

### RhythmCombatView

Rhythm combat encounter visual.

```python
class RhythmCombatView:
    def __init__(screen_width: int, screen_height: int, boss_max_health: int, player_max_health: int, background_image_path: str)
```

**Methods:**
- `create_particles(x, y, color) -> None` - Create visual effect
- `update_particles() -> None` - Update animations
- `draw(screen, rhythm, player, boss) -> None` - Render combat

---

### RhythmCombatPageView

Full-screen rhythm combat encounter.

```python
class RhythmCombatPageView(PageView):
    def __init__(screen: pygame.Surface, player: PlayerModel, boss: BossModel, sequence_controller: GameSequenceController)
```

**Methods:**
- `run() -> str` - Main combat loop

---

### LoginPageView

User login/registration screen.

```python
class LoginPageView(PageView):
    def __init__(name: str, width: int, height: int, flags: int, background_image: str)
```

**Methods:**
- `setup_buttons() -> None` - Initialize login buttons
- `run() -> tuple` - Run login flow, returns (username, progression) or (None, None)
- `handle_login() -> None` - Process login
- `switch_to_register() -> None` - Switch to registration mode
- `handle_register() -> None` - Process registration
- `handle_events() -> None` - Handle input
- `draw() -> None` - Render login screen

---

### WelcomePageView

Main menu screen.

```python
class WelcomPageView(PageView):
    def __init__(name: str, width: int, height: int, flags: int, background_image: str)
```

**Methods:**
- `run() -> str` - Run menu, returns selected action
- `handle_events() -> None` - Handle menu input
- `draw() -> None` - Render menu

---

### PauseMenuView

In-game pause menu overlay.

```python
class PauseMenuView:
    def __init__(screen: pygame.Surface)
```

**Methods:**
- `draw(screen) -> None` - Draw pause menu
- `handle_events(events) -> str` - Handle menu input, returns action

---

### ShopPageView

Shop interaction screen.

```python
class ShopPageView:
    def __init__(screen: pygame.Surface, shop: ShopModel)
```

**Methods:**
- `draw(player: PlayerModel) -> None` - Render shop interface
- `handle_input(event) -> None` - Process shop input

---

### FinTransitionPageView

End-of-act transition screen.

```python
class FinTransitionPageView(PageView):
    def __init__(screen: pygame.Surface, message: str, next_stage_name: str, duration_seconds: int)
```

**Methods:**
- `run() -> str` - Show transition, returns next state

---

## CONTROLLERS

Game logic and input handling.

### GameState

Enumeration of all possible game states.

```python
class GameState(Enum):
    QUIT = "QUIT"
    LOGOUT = "LOGOUT"
    MAIN_MENU = "MAIN_MENU"
    ACT1 = "ACT1"
    ACT2 = "ACT2"
    RHYTHM = "RHYTHM"
    MAP = "MAP"
    GAME_OVER = "GAME_OVER"
    COMPLETE = "COMPLETE"
    START_GAME = "START_GAME"
    CONTINUE = "CONTINUE"
```

---

### GameSequenceController

Manages game flow and stage progression.

```python
class GameSequenceController:
    def __init__()
```

**Game Stages:**
```python
class GameStage(Enum):
    RHYTHM_PAGE_1 = 1
    MAP_1 = 2
    ACT_1 = 3
    MAP_2 = 4
    ACT_2 = 5
    RHYTHM_PAGE_2 = 6
    MAP_3 = 7
    RHYTHM_COMBAT = 8
```

**Attributes:**
- `current_stage`: int - Current game stage
- `player`: PlayerModel - Active player
- `boss`: BossModel - Current boss (if any)
- `is_admin`: bool - Admin mode flag

**Methods:**
- `set_player(player: PlayerModel) -> None` - Set player character
- `get_player() -> PlayerModel` - Get player character
- `set_boss(boss: BossModel) -> None` - Set boss
- `get_boss() -> BossModel` - Get boss
- `get_current_stage() -> int` - Get stage number
- `get_current_stage_name() -> str` - Get stage name
- `set_stage(stage: int) -> bool` - Jump to stage
- `advance_stage() -> bool` - Go to next stage
- `get_next_view() -> dict` - Get next view configuration
- `is_last_stage() -> bool` - Check if final stage

---

### ButtonController

Manages button click detection and actions.

```python
class ButtonController:
    def __init__(button: ButtonView, action: str)
```

**Attributes:**
- `button`: ButtonView - Button being controlled
- `action`: str - Action when clicked

**Methods:**
- `isClicked(mouse_pos: tuple) -> bool` - Detect click
- `handleClick() -> str` - Return action state
- `handle_input(event) -> str` - Handle input event
- `handleEvents(event) -> str` - Alternate event handler
- `quitGame() -> None` - Quit game

---

### CombatController

Manages combat turn logic and actions.

```python
class CombatController:
    def __init__(combat: CombatModel)
```

**Attributes:**
- `combat`: CombatModel - Combat state
- `player`: PlayerModel - Player in combat
- `enemy`: CaracterModel - Enemy in combat
- `action_delay`: int - Frames until next action
- `action_cooldown`: int - Cooldown duration

**Methods:**
- `update() -> None` - Update combat state
- `handle_input(event) -> None` - Handle player action
- `handleInput(event) -> None` - Alternate input handler
- `playerSimpleAttack() -> None` - Basic attack
- `playerPowerChord() -> None` - Power chord attack
- `playerDegueulando() -> None` - Special vomit attack
- `playerDrink() -> None` - Consume bottle
- `endPlayerTurn() -> None` - Skip turn
- `enemyTurn() -> None` - AI turn

---

### PlayerController

Handles player movement and collision.

```python
class PlayerController:
    def __init__(screen: pygame.Surface, player: PlayerModel, collision_rects: list = None)
```

**Attributes:**
- `player`: PlayerModel - Player being controlled
- `collision_rects`: list - Collision rectangles
- `PLAYER_SIZE`: int - Player sprite size (50 pixels)
- `SPEED`: int - Movement speed (5 pixels/frame)

**Methods:**
- `handle_input(event) -> None` - Handle movement input
- `handleInput(event) -> None` - Alternate input handler
- `handle_events(events) -> None` - Handle event list

---

### RhythmController

Manages rhythm game mechanics.

```python
class RhythmController:
    def __init__(rhythm: RhythmModel, character: CaracterModel, screen_height: int, view: RhythmView, song_data: dict, context: dict)
```

**Attributes:**
- `rhythm`: RhythmModel - Rhythm game state
- `character`: CaracterModel - Player character
- `view`: RhythmView - Rhythm view
- `current_song`: SongModel - Playing song
- `track_guitar`: pygame.mixer.Sound - Guitar audio
- `track_backing`: pygame.mixer.Sound - Backing audio
- `is_playing`: bool - Playing state
- `is_paused`: bool - Paused state
- `game_over`: bool - End state
- `key_map`: dict - Key to lane mapping

**Methods:**
- `playRandomFail() -> None` - Play fail sound
- `stop_all_audio() -> None` - Stop music
- `pause_audio() -> None` - Pause music
- `resume_audio() -> None` - Resume music
- `handle_input(event) -> None` - Handle note input
- `update(dt: float) -> None` - Update game state

---

### RhythmCombatController

Manages rhythm-based boss battles.

```python
class RhythmCombatController:
    def __init__(rhythm: RhythmModel, player: PlayerModel, boss: BossModel, screen_height: int, view: RhythmCombatView, song_loader)
```

**Methods:**
- `play_random_fail() -> None` - Play fail sound
- `play_random_hit() -> None` - Play hit sound
- `stop_all_audio() -> None` - Stop music
- `pause_audio() -> None` - Pause music
- `resume_audio() -> None` - Resume music
- `handle_input(event) -> None` - Handle note hits
- `update(dt: float) -> None` - Update battle state

---

### LoginController

Manages user authentication flow.

```python
class LoginController:
    def __init__()
```

**Attributes:**
- `login_model`: LoginModel - Authentication system
- `login_view`: LoginPageView - Login UI

**Methods:**
- `start_login_flow() -> str` - Run login process
- `get_current_user() -> str` - Get logged in user
- `get_user_progression() -> dict` - Get player progression
- `save_progression(progression: dict) -> bool` - Save progress
- `logout() -> None` - Log out user

---

### PauseMenuController

Manages pause menu interaction.

```python
class PauseMenuController:
    def __init__(button_controllers: list)
```

**Attributes:**
- `button_controllers`: list - Menu buttons
- `selected_index`: int - Selected button

**Methods:**
- `handle_events(events) -> str` - Handle input, returns action
- `handle_input(event) -> str` - Alternative event handler
- `_map_button_action(action) -> str` - Map button to game state

---

### ShopController

Manages shop interaction logic.

```python
class ShopController:
    def __init__(shop: ShopModel, view: ShopPageView)
```

**Attributes:**
- `shop_model`: ShopModel - Shop state
- `view`: ShopPageView - Shop UI

**Methods:**
- `handle_input(event) -> str` - Handle shop input

---

## UTILITIES

Helper and utility classes.

### Logger

Static logging utility for debugging.

```python
class Logger:
    ENABLED = True
    LOG_DIR = "Game/logs"
```

**Methods:**
- `@staticmethod error(function_name: str, exception: Exception) -> None` - Log error with traceback
- `@staticmethod debug(function_name: str, message: str, **values) -> None` - Log debug message with context

**Output:**
- Creates timestamped log files in `Game/logs/`
- Separate files for errors and general debug logs

---

### AssetManager

Manages asset loading and caching.

```python
class AssetManager:
    def __init__(base_path: str = "Game/Assets")
```

**Attributes:**
- `base_path`: str - Assets root directory
- `bosses_config_path`: str - Boss config file location
- `player_config_path`: str - Player config file location

**Methods:**
- `load_bosses_config() -> dict` - Load boss definitions
- `save_bosses_config(config: dict) -> None` - Save boss definitions
- `get_boss_by_name(name: str) -> dict` - Get specific boss config
- `load_player_config() -> dict` - Load player configuration
- `save_player_config(config: dict) -> None` - Save player configuration

---

### UserManager

Manages user accounts and progression.

```python
class UserManager:
    def __init__()
```

**Attributes:**
- `PROGRESSION_DIR`: str - User progression directory
- `CREDENTIALS_FILE`: str - Credentials storage
- `cipher`: Fernet - Password encryption cipher

**Methods:**
- `register_user(username: str, password: str) -> bool` - Create account
- `authenticate_user(username: str, password: str) -> bool` - Verify login
- `user_exists(username: str) -> bool` - Check if user registered
- `load_progression(username: str) -> dict` - Load player save
- `save_progression(username: str, data: dict) -> bool` - Save player progress
- `_encrypt_password(password: str) -> str` - Hash password
- `_decrypt_password(encrypted: str) -> str` - Verify password

---

## Quick Reference

### Creating Objects

```python
from Models.PlayerModel import PlayerModel
from Models.BossModel import BossModel

player = PlayerModel("Lola Coma", 100, 100)
boss = BossModel.from_config(boss_config, 200, 200)
```

### Accessing Properties

```python
player.setHealth(100)
health = player.getHealth()

position_x = player.getX()
player.setX(150)
```

### Rhythm Game

```python
from Models.RhythmModel import RhythmModel
rhythm = RhythmModel()
rhythm.score += 100
rhythm.combo += 1
```

### Game State Management

```python
from Controllers.GameState import GameState
return GameState.QUIT.value
```

---

## File Organization

```
Game/src/
├── Models/          (14 classes) - Game entity data
├── Views/           (18 classes) - UI rendering
├── Controllers/     (10 classes) - Game logic
├── Utils/           (3 classes)  - Helper functions
├── Songs/           (3 classes)  - Song definitions
└── main.py          - Entry point
```

---

*API Documentation v1.0.0 - February 8, 2026*
