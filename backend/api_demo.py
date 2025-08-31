#!/usr/bin/env python3
"""
API Demo Script - Test Django endpoints without starting server
"""

import sys
import os
import json

# Add the poker_gto directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from poker_gto.core import Card, Deck, Hand, Position, Rank, Suit
from poker_gto.gto import GTOAnalyzer


def demo_api_functionality():
    """Demo the core API functionality"""
    print("Django API Backend Demo")
    print("=" * 40)
    
    analyzer = GTOAnalyzer()
    
    # 1. Generate random situation (like /api/random-situation/)
    print("\n1. RANDOM TRAINING SITUATION:")
    print("-" * 30)
    
    # Generate random position
    import random
    positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
    position = random.choice(positions)
    
    # Generate random hand
    deck = Deck()
    cards = deck.deal_cards(2)
    hand = Hand(cards[0], cards[1])
    
    # Determine scenario
    if position == Position.BB:
        scenarios = ["vs_btn_sb", "vs_co", "vs_mp3"]
        scenario = random.choice(scenarios)
    else:
        scenario = "first_in"
    
    # Get GTO analysis
    analysis = analyzer.analyze_preflop_hand(hand, position, scenario)
    
    situation = {
        'situation_id': random.randint(1000, 9999),
        'position': position.to_dict(),
        'hand': hand.to_dict(),
        'scenario': scenario,
        'scenario_description': _get_scenario_description(position, scenario),
        'gto_analysis': analysis
    }
    
    print(f"Position: {position.short_name} ({position.full_name})")
    print(f"Hand: {hand} ({hand.get_hand_notation()})")
    print(f"Scenario: {scenario}")
    print(f"GTO Recommendation: {analysis['recommended_action']}")
    print(f"Explanation: {analysis['explanation']}")
    
    # 2. Position ranges (like /api/position-ranges/)
    print("\n2. POSITION RANGES:")
    print("-" * 30)
    
    positions_to_test = [Position.MP, Position.CO, Position.BTN]
    for pos in positions_to_test:
        range_summary = analyzer.get_opening_range_summary(pos, "first_in")
        if 'error' not in range_summary:
            print(f"{pos.short_name}: {range_summary['total_hands']} hands ({range_summary['percentage']}%)")
        else:
            print(f"{pos.short_name}: {range_summary['error']}")
    
    # 3. Available scenarios (like /api/scenarios/)
    print("\n3. AVAILABLE SCENARIOS:")
    print("-" * 30)
    
    scenarios = analyzer.get_all_available_scenarios()
    for scenario_name, positions_list in scenarios.items():
        print(f"{scenario_name}: {', '.join(positions_list)}")
    
    # 4. Action validation demo
    print("\n4. ACTION VALIDATION DEMO:")
    print("-" * 30)
    
    # Test with premium hand
    test_deck = Deck()
    test_cards = []
    
    # Find AA
    for card in test_deck.cards:
        if card.rank == Rank.ACE:
            test_cards.append(card)
            if len(test_cards) == 2:
                break
    
    if len(test_cards) == 2:
        premium_hand = Hand(test_cards[0], test_cards[1])
        premium_analysis = analyzer.analyze_preflop_hand(premium_hand, Position.BTN, "first_in")
        
        print(f"Test Hand: {premium_hand} ({premium_hand.get_hand_notation()})")
        print(f"Position: BTN")
        print(f"GTO Action: {premium_analysis['recommended_action']}")
        
        # Simulate user actions
        user_actions = ["fold", "call", "raise", "reraise"]
        gto_action = premium_analysis['recommended_action']
        
        for user_action in user_actions:
            is_correct = _validate_action(user_action, gto_action)
            status = "CORRECT" if is_correct else "WRONG"
            print(f"  User: {user_action} -> {status}")
    
    print("\n" + "=" * 40)
    print("API Demo completed successfully!")
    print("The Django backend is ready to serve these endpoints:")
    print("- GET  /api/health/")
    print("- GET  /api/random-situation/")
    print("- GET  /api/position-ranges/")
    print("- GET  /api/scenarios/")
    print("- POST /api/analyze-hand/")
    print("- POST /api/validate-action/")


def _get_scenario_description(position: Position, scenario: str) -> str:
    """Get human-readable scenario description"""
    if scenario == "first_in":
        return f"You are {position.short_name} and no one has raised yet."
    elif scenario == "vs_btn_sb":
        return f"You are {position.short_name} and the Button/SB has raised."
    elif scenario == "vs_co":
        return f"You are {position.short_name} and the CO has raised."
    elif scenario == "vs_mp3":
        return f"You are {position.short_name} and MP has raised."
    else:
        return f"You are {position.short_name}."


def _validate_action(user_action: str, gto_action: str) -> bool:
    """Simple action validation"""
    # Map actions for flexible matching
    action_mapping = {
        'fold': ['fold'],
        'call': ['call', 'call_ip'],
        'raise': ['raise', 'raise_fold', 'raise_call', 'raise_4_bet_fold', 'raise_4_bet_all_in'],
        'reraise': ['reraise_fold', 'reraise_all_in']
    }
    
    # Check if user action maps to GTO action
    for user_mapped, gto_mapped_list in action_mapping.items():
        if user_action.lower() == user_mapped:
            return any(gto_mapped in gto_action.lower().replace('-', '_') for gto_mapped in gto_mapped_list)
    
    return user_action.lower() == gto_action.lower()


if __name__ == "__main__":
    demo_api_functionality()
