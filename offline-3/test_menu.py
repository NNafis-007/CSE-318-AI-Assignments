#!/usr/bin/env python3
"""
Test script to verify the AI difficulty and heuristic selection functionality
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.enums import AIDifficulty, AIHeuristic

def test_enums():
    """Test the new enum classes"""
    print("=== Testing AIDifficulty Enum ===")
    for difficulty in AIDifficulty:
        print(f"{difficulty.name}: {difficulty.display_name} (Depth: {difficulty.depth})")
    
    print("\n=== Testing AIHeuristic Enum ===")
    for heuristic in AIHeuristic:
        print(f"{heuristic.name}: {heuristic.display_name} (Key: {heuristic.key})")
    
    print("\n=== Testing Default Values ===")
    default_difficulty = AIDifficulty.MEDIUM
    default_heuristic = AIHeuristic.WEIGHTED_COMBINED
    print(f"Default Difficulty: {default_difficulty.display_name} (Depth: {default_difficulty.depth})")
    print(f"Default Heuristic: {default_heuristic.display_name} (Key: {default_heuristic.key})")

if __name__ == "__main__":
    test_enums()
    print("\n✅ All enum tests passed!")
