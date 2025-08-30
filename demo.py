#!/usr/bin/env python3
"""
Simple console demo for the Poker GTO Trainer
Part 1: Basic class structure demonstration
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import *


def demo_deck():
    """Demonstrate deck functionality"""
    print("=== DECK DEMO ===")
    deck = Deck()
    print(f"New deck: {deck}")
    
    # Deal some cards
    cards = deck.deal_cards(5)
    print(f"Dealt cards: {[str(card) for card in cards]}")
    print(f"Remaining in deck: {deck.cards_remaining()}")
    print()


def demo_positions():
    """Demonstrate position functionality"""
    print("=== POSITIONS DEMO ===")
    pos_manager = PositionManager()
    
    for position in pos_manager.positions:
        print(f"{position.short_name}: {position.full_name} (Order: {position.order})")
    
    # Test position relationships
    utg = Position.UTG
    btn = Position.BTN
    print(f"\n{btn} is in position vs {utg}: {btn.is_in_position(utg)}")
    print(f"{utg} is in position vs {btn}: {utg.is_in_position(btn)}")
    print()



def demo_hands():
    """Demonstrate hand functionality"""
    print("=== HANDS DEMO ===")
    
    # Create some example hands
    ace_hearts = Card(Rank.ACE, Suit.HEARTS)
    king_hearts = Card(Rank.KING, Suit.HEARTS)
    queen_spades = Card(Rank.QUEEN, Suit.SPADES)
    queen_clubs = Card(Rank.QUEEN, Suit.CLUBS)
    
    # Suited hand
    suited_hand = Hand(ace_hearts, king_hearts)
    print(f"Suited hand: {suited_hand}")
    print(f"Is suited: {suited_hand.is_suited()}")
    print(f"Is pair: {suited_hand.is_pair()}")
    
    # Pocket pair
    pair_hand = Hand(queen_spades, queen_clubs)
    print(f"Pocket pair: {pair_hand}")
    print(f"Is suited: {pair_hand.is_suited()}")
    print(f"Is pair: {pair_hand.is_pair()}")
    
    # Hand range demo
    hand_range = HandRange()
    hand_range.add_hand("AA", 1.0)
    hand_range.add_hand("AKs", 0.8)
    hand_range.add_hand("AKo", 0.6)
    print(f"\nHand range: {hand_range}")
    print(f"AA frequency: {hand_range.get_frequency('AA')}")
    print()



def demo_table():
    """Demonstrate table functionality"""
    print("=== TABLE DEMO ===")
    
    # Create table
    table = Table()
    
    # Add players
    table.add_player("Alice", Position.UTG, 100.0)
    table.add_player("Bob", Position.CO, 150.0)
    table.add_player("Charlie", Position.BTN, 200.0)
    table.add_player("Diana", Position.SB, 75.0)
    table.add_player("Eve", Position.BB, 125.0)
    
    print("Table setup:")
    print(table)
    
    # Deal preflop
    print("\n--- Dealing preflop ---")
    table.deal_preflop()
    table.post_blinds()
    
    print("After preflop deal and blinds:")
    print(table)
    
    # Deal flop
    print("\n--- Dealing flop ---")
    table.deal_flop()
    
    print("After flop:")
    print(table)
    print()


def main():
    """Main demo function"""
    print("*** POKER GTO TRAINER - Part 1 Demo ***")
    print("=======================================\n")
    
    demo_deck()
    demo_positions()
    demo_hands()
    demo_table()
    
    print("*** Part 1 implementation complete! ***")
    print("All basic classes are working correctly.")


if __name__ == "__main__":
    main()
