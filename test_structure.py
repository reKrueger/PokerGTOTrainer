#!/usr/bin/env python3
"""
Simple test to validate Django backend structure
"""

import sys
import os

# Add the poker_gto directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def test_imports():
    """Test that all modules can be imported"""
    print("Testing Django Backend Structure")
    print("=" * 40)
    
    try:
        # Test core imports
        print("Testing core imports...")
        from poker_gto.core import Card, Deck, Hand, Position, Rank, Suit
        from poker_gto.core.position import PositionManager
        print("Core imports successful")
        
        # Test GTO imports  
        print("Testing GTO imports...")
        from poker_gto.gto import Action, GTORange, GTOChartParser, GTOAnalyzer
        print("GTO imports successful")
        
        # Test basic functionality
        print("Testing basic functionality...")
        deck = Deck()
        cards = deck.deal_cards(2)
        hand = Hand(cards[0], cards[1])
        print(f"Generated hand: {hand} ({hand.get_hand_notation()})")
        
        # Test GTO analysis
        analyzer = GTOAnalyzer()
        analysis = analyzer.analyze_preflop_hand(hand, Position.BTN, "first_in")
        print(f"GTO Analysis: {analysis['recommended_action']}")
        
        # Test JSON serialization
        hand_dict = hand.to_dict()
        print(f"JSON serialization: {hand_dict['notation']}")
        
        print("\nAll tests passed! Django backend structure is valid.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
