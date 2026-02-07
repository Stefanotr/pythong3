#!/usr/bin/env python3
"""
Test script to verify JSON configuration loading works correctly.
"""

import sys
import os

# Add Game/src to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Game', 'src'))

from Utils.AssetManager import AssetManager
from Utils.Logger import Logger

print("\n" + "="*60)
print("Testing JSON Configuration Loading")
print("="*60 + "\n")

# Initialize AssetManager
print("[1] Initializing AssetManager...")
try:
    asset_manager = AssetManager()
    print("✓ AssetManager initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize AssetManager: {e}")
    sys.exit(1)

# Test loading player config
print("\n[2] Loading player configuration...")
try:
    player_config = asset_manager.load_player_config()
    print(f"✓ Player config loaded")
    print(f"  - ID: {player_config.get('id', 'N/A')}")
    print(f"  - Name: {player_config.get('name', 'N/A')}")
    print(f"  - Base name: {player_config.get('base_name', 'N/A')}")
    
    if 'actions' in player_config:
        print(f"  - Actions available: {len(player_config['actions'])}")
        for action_name in list(player_config['actions'].keys())[:5]:
            action_value = player_config['actions'][action_name]
            if isinstance(action_value, list):
                print(f"    • {action_name}: [animation with {len(action_value)} frames]")
            else:
                print(f"    • {action_name}: {action_value}")
    else:
        print(f"  ✗ No 'actions' key found in player config!")
        
    if 'sizes' in player_config:
        print(f"  - Sizes configured for modes: {list(player_config['sizes'].keys())}")
    else:
        print(f"  ✗ No 'sizes' key found in player config!")
        
except Exception as e:
    print(f"✗ Failed to load player config: {e}")
    sys.exit(1)

# Test loading bosses config
print("\n[3] Loading bosses configuration...")
try:
    bosses_config = asset_manager.load_bosses_config()
    if 'bosses' in bosses_config:
        print(f"✓ Bosses config loaded with {len(bosses_config['bosses'])} bosses")
        for boss in bosses_config['bosses']:
            print(f"  - {boss.get('name', 'Unknown')} (Act {boss.get('act', '?')})")
    else:
        print(f"✗ No 'bosses' key found in bosses config!")
except Exception as e:
    print(f"✗ Failed to load bosses config: {e}")
    sys.exit(1)

# Test getting boss by name
print("\n[4] Testing boss lookup by name...")
try:
    boss = asset_manager.get_boss_by_name("Gros Bill")
    if boss:
        print(f"✓ Found boss: {boss.get('name', 'Unknown')}")
        if 'actions' in boss:
            print(f"  - Actions: {len(boss['actions'])}")
        if 'backgrounds' in boss:
            print(f"  - Backgrounds: {list(boss['backgrounds'].keys())}")
    else:
        print(f"✗ Boss 'Gros Bill' not found")
except Exception as e:
    print(f"✗ Failed to get boss by name: {e}")

print("\n" + "="*60)
print("Configuration loading test completed!")
print("="*60 + "\n")
