#!/usr/bin/env python3
"""
Test script to verify all 6 positions are working in GTO training
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import *
from gto import *
from utils.table_visualizer import PokerTableVisualizer


def test_all_positions():
    """Test GTO recommendations for all 6 positions"""
    print("*** TEST: ALLE 6 POSITIONEN IM GTO-TRAINING ***")
    print("=" * 55)
    
    analyzer = GTOAnalyzer()
    visualizer = PokerTableVisualizer()
    
    # Test all 6 positions
    all_positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
    
    # Test hand: AKs (should be strong from all positions)
    test_hand = Hand(Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS))
    
    print(f"\nTEST HAND: {test_hand.get_hand_notation()}")
    print("=" * 30)
    
    for i, position in enumerate(all_positions, 1):
        print(f"\n{i}/6: {position.short_name} ({position.full_name})")
        print("-" * 40)
        
        # Show position on table
        visualizer.display_compact_table(position)
        
        # Get GTO recommendation
        try:
            analysis = analyzer.analyze_preflop_hand(test_hand, position, "first_in")
            print(f"GTO EMPFEHLUNG: {analysis['recommended_action']}")
            print(f"ERKLAERUNG: {analysis['explanation']}")
        except Exception as e:
            print(f"FEHLER: {e}")
        
        print()
    
    # Test range summaries for all positions
    print("\n*** RANGE SUMMARIES FÜR ALLE POSITIONEN ***")
    print("=" * 50)
    
    for position in all_positions:
        try:
            summary = analyzer.get_opening_range_summary(position)
            if "error" not in summary:
                total_hands = sum(data['count'] for data in summary['actions'].values())
                print(f"{position.short_name}: {total_hands} Hände insgesamt")
            else:
                print(f"{position.short_name}: {summary['error']}")
        except Exception as e:
            print(f"{position.short_name}: FEHLER - {e}")
    
    print("\n*** TEST ABGESCHLOSSEN ***")


if __name__ == "__main__":
    test_all_positions()
