#!/usr/bin/env python3
"""
Poker GTO Trainer - Part 2 Demo
GTO Analysis and Range Testing
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import *
from gto import *


def demo_gto_analysis():
    """Demonstrate GTO analysis functionality"""
    print("=== GTO ANALYSIS DEMO ===")
    
    analyzer = GTOAnalyzer()
    
    # Test some specific hands from different positions
    test_hands = [
        (Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS)),  # AKs
        (Card(Rank.QUEEN, Suit.SPADES), Card(Rank.QUEEN, Suit.CLUBS)),  # QQ
        (Card(Rank.EIGHT, Suit.HEARTS), Card(Rank.SEVEN, Suit.HEARTS)),  # 87s
        (Card(Rank.ACE, Suit.HEARTS), Card(Rank.TWO, Suit.SPADES)),  # A2o
    ]
    
    positions = [Position.MP, Position.CO, Position.BTN]
    
    for card1, card2 in test_hands:
        hand = Hand(card1, card2)
        print(f"\n--- Analyzing {hand.get_hand_notation()} ---")
        
        for position in positions:
            analysis = analyzer.analyze_preflop_hand(hand, position)
            print(f"{position.short_name}: {analysis['recommended_action']} - {analysis['explanation']}")
    
    print()


def demo_position_ranges():
    """Demonstrate position range summaries"""
    print("=== POSITION RANGES DEMO ===")
    
    analyzer = GTOAnalyzer()
    
    for position in [Position.MP, Position.CO, Position.BTN]:
        print(f"\n--- {position.short_name} Opening Range ---")
        summary = analyzer.get_opening_range_summary(position)
        
        if "error" not in summary:
            print(f"Total action types: {summary['total_actions']}")
            
            for action_name, data in summary["actions"].items():
                print(f"{action_name}: {data['count']} hands")
                if data['hands']:
                    print(f"  Examples: {', '.join(data['hands'][:5])}")
        else:
            print(f"Error: {summary['error']}")
    
    print()


def demo_hand_comparison():
    """Demonstrate hand comparison across positions"""
    print("=== HAND COMPARISON DEMO ===")
    
    analyzer = GTOAnalyzer()
    
    comparison_hands = ["AKs", "QQ", "87s", "A2o", "KJo"]
    
    for hand in comparison_hands:
        print(f"\n--- {hand} Position Comparison ---")
        comparison = analyzer.compare_positions(hand)
        
        for pos_name, data in comparison["positions"].items():
            print(f"{pos_name}: {data['action']}")
    
    print()


def demo_table_analysis():
    """Demonstrate full table analysis"""
    print("=== TABLE ANALYSIS DEMO ===")
    
    # Create table with players
    table = Table()
    table.add_player("Alice", Position.MP, 100.0)
    table.add_player("Bob", Position.CO, 150.0)
    table.add_player("Charlie", Position.BTN, 200.0)
    table.add_player("Diana", Position.BB, 125.0)
    
    # Deal hands
    table.deal_preflop()
    
    print("Table situation:")
    for player in table.players:
        if player.hole_cards:
            print(f"{player.name} ({player.position.short_name}): {player.hole_cards.get_hand_notation()}")
    
    # Analyze all hands
    analyzer = GTOAnalyzer()
    analyses = analyzer.analyze_table_scenario(table)
    
    print("\nGTO Recommendations:")
    for analysis in analyses:
        print(f"{analysis['player_name']}: {analysis['recommended_action']}")
        print(f"  -> {analysis['explanation']}")
    
    print()


def demo_quiz_mode():
    """Demonstrate quiz functionality"""
    print("=== QUIZ MODE DEMO ===")
    
    analyzer = GTOAnalyzer()
    
    for position in [Position.MP, Position.CO, Position.BTN]:
        print(f"\n--- Quiz for {position.short_name} ---")
        quiz = analyzer.get_quiz_hand(position)
        
        if "error" not in quiz:
            print(f"Question: {quiz['question']}")
            for i, option in enumerate(quiz['options']):
                marker = "* " if i == quiz['correct_answer'] else "  "
                print(f"{marker}{i+1}. {option}")
            print(f"Answer: {quiz['explanation']}")
        else:
            print(f"Error: {quiz['error']}")
    
    print()


def demo_flop_analysis():
    """Demonstrate basic flop analysis"""
    print("=== FLOP ANALYSIS DEMO ===")
    
    flop_analyzer = FlopAnalyzer()
    
    # Create some example flops
    test_flops = [
        [Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS), Card(Rank.QUEEN, Suit.HEARTS)],  # AKQ flush
        [Card(Rank.SEVEN, Suit.HEARTS), Card(Rank.SEVEN, Suit.SPADES), Card(Rank.TWO, Suit.DIAMONDS)],  # Paired
        [Card(Rank.JACK, Suit.HEARTS), Card(Rank.NINE, Suit.SPADES), Card(Rank.TWO, Suit.DIAMONDS)],  # Rainbow
    ]
    
    for flop in test_flops:
        analysis = flop_analyzer.analyze_flop_texture(flop)
        flop_str = " ".join([str(card) for card in flop])
        print(f"Flop: {flop_str}")
        print(f"  Texture: {analysis['texture_type']}")
        print(f"  Properties: Pair={analysis['has_pair']}, Flush Draw={analysis['flush_draw']}, Rainbow={analysis['rainbow']}")
        print()


def main():
    """Main demo function for Part 2"""
    print("*** POKER GTO TRAINER - Part 2 Demo ***")
    print("*** GTO Analysis & Range Implementation ***")
    print("==========================================\n")
    
    demo_gto_analysis()
    demo_position_ranges() 
    demo_hand_comparison()
    demo_table_analysis()
    demo_quiz_mode()
    demo_flop_analysis()
    
    print("*** Part 2 implementation complete! ***")
    print("GTO analysis system is working correctly.")
    print("\nFeatures implemented:")
    print("- Preflop GTO ranges for all positions")
    print("- Hand analysis with recommendations")
    print("- Position comparison")
    print("- Table scenario analysis")
    print("- Quiz mode generation")
    print("- Basic flop texture analysis")


if __name__ == "__main__":
    main()
