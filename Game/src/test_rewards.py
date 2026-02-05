#!/usr/bin/env python3
"""
Test script to verify the reward calculation system.
Tests rewards for different contexts, scores, and player levels.
"""

import sys
sys.path.insert(0, '.')

from Models.PlayerModel import PlayerModel
from Models.RhythmModel import RhythmModel
from Controllers.RhythmController import RhythmController
from Views.RhythmView import RhythmView

def test_reward_calculation():
    """Test the reward calculation system"""
    
    print("=" * 60)
    print("TESTING REWARD CALCULATION SYSTEM")
    print("=" * 60)
    
    # Create a player and rhythm model
    player = PlayerModel("TestPlayer", 60, 60)
    rhythm_model = RhythmModel()
    rhythm_view = RhythmView(1024, 768)
    
    # Test 1: Act 1 rewards at different levels with different scores
    print("\n1. ACT 1 REWARDS (beginner difficulty)")
    print("-" * 60)
    
    test_cases_act1 = [
        {"level": 0, "score": 2000, "satisfaction": 50},
        {"level": 0, "score": 15000, "satisfaction": 50},
        {"level": 1, "score": 15000, "satisfaction": 50},
        {"level": 2, "score": 15000, "satisfaction": 50},
        {"level": 0, "score": 15000, "satisfaction": 100},  # Perfect crowd
    ]
    
    for i, case in enumerate(test_cases_act1):
        player.setLevel(case["level"])
        rhythm_model.score = case["score"]
        rhythm_model.crowd_satisfaction = case["satisfaction"]
        
        # Create controller with Act 1 context
        controller = RhythmController(rhythm_model, player, 768, rhythm_view, context="act1")
        reward = controller._calculate_reward()
        
        print(f"Case {i+1}: Level {case['level']}, Score {case['score']}, Satisfaction {case['satisfaction']}%")
        print(f"  → Reward: ${reward}")
    
    # Test 2: Act 2 rewards
    print("\n2. ACT 2 REWARDS (medium difficulty)")
    print("-" * 60)
    
    test_cases_act2 = [
        {"level": 0, "score": 15000, "satisfaction": 50},
        {"level": 1, "score": 15000, "satisfaction": 50},
        {"level": 2, "score": 15000, "satisfaction": 50},
    ]
    
    for i, case in enumerate(test_cases_act2):
        player.setLevel(case["level"])
        rhythm_model.score = case["score"]
        rhythm_model.crowd_satisfaction = case["satisfaction"]
        
        controller = RhythmController(rhythm_model, player, 768, rhythm_view, context="act2")
        reward = controller._calculate_reward()
        
        print(f"Case {i+1}: Level {case['level']}, Score {case['score']}, Satisfaction {case['satisfaction']}%")
        print(f"  → Reward: ${reward} (Act 2 = 1.5x Act 1)")
    
    # Test 3: RhythmCombat rewards
    print("\n3. RHYTHM COMBAT REWARDS (final boss / hardest)")
    print("-" * 60)
    
    test_cases_combat = [
        {"level": 0, "score": 15000, "satisfaction": 50},
        {"level": 1, "score": 15000, "satisfaction": 50},
        {"level": 2, "score": 15000, "satisfaction": 50},
    ]
    
    for i, case in enumerate(test_cases_combat):
        player.setLevel(case["level"])
        rhythm_model.score = case["score"]
        rhythm_model.crowd_satisfaction = case["satisfaction"]
        
        controller = RhythmController(rhythm_model, player, 768, rhythm_view, context="rhythm_combat")
        reward = controller._calculate_reward()
        
        print(f"Case {i+1}: Level {case['level']}, Score {case['score']}, Satisfaction {case['satisfaction']}%")
        print(f"  → Reward: ${reward} (Rhythm Combat = 2.5x Act 1)")
    
    # Test 4: Currency accumulation
    print("\n4. CURRENCY ACCUMULATION TEST")
    print("-" * 60)
    
    player.setCurrency(0)
    print(f"Starting currency: ${player.getCurrency()}")
    
    player.addCurrency(100)
    print(f"After adding 100: ${player.getCurrency()}")
    
    player.addCurrency(50)
    print(f"After adding 50: ${player.getCurrency()}")
    
    player.setCurrency(200)
    print(f"After setting to 200: ${player.getCurrency()}")
    
    # Test 5: Level scaling comparison
    print("\n5. LEVEL SCALING COMPARISON (Act 1, Perfect Score)")
    print("-" * 60)
    
    print(f"{'Level':<8} {'Act 1':<10} {'Act 2':<10} {'Rhythm':<10} {'Multiplier':<12}")
    print("-" * 50)
    
    rhythm_model.score = 15000
    rhythm_model.crowd_satisfaction = 50
    
    for level in range(0, 6):
        player.setLevel(level)
        
        controller1 = RhythmController(rhythm_model, player, 768, rhythm_view, context="act1")
        reward1 = controller1._calculate_reward()
        
        controller2 = RhythmController(rhythm_model, player, 768, rhythm_view, context="act2")
        reward2 = controller2._calculate_reward()
        
        controller_c = RhythmController(rhythm_model, player, 768, rhythm_view, context="rhythm_combat")
        reward_c = controller_c._calculate_reward()
        
        multiplier = level + 1
        print(f"{level:<8} ${reward1:<9} ${reward2:<9} ${reward_c:<9} {multiplier}x")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    print("\nSummary:")
    print("- Act 1 (beginner): Base 100$ at level 0")
    print("- Act 2 (medium): Base 150$ at level 0 (1.5x Act 1)")
    print("- Rhythm Combat (final boss): Base 250$ at level 0 (2.5x Act 1)")
    print("- All scales by (level + 1) multiplier")
    print("- Score and crowd satisfaction affect final reward")

if __name__ == "__main__":
    test_reward_calculation()
