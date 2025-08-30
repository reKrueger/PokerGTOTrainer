#!/usr/bin/env python3
"""
Poker GTO Trainer - Interactive Training Mode
Random game situations with GTO evaluation
"""

import sys
import os
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import *
from gto import *
from utils.table_visualizer import PokerTableVisualizer


class GTOTrainer:
    """Interactive GTO training application"""
    
    def __init__(self):
        self.analyzer = GTOAnalyzer()
        self.visualizer = PokerTableVisualizer()
        self.score = {"correct": 0, "total": 0}
        
        # Action mapping from user input to GTO actions
        self.action_mapping = {
            1: ("Passen", Action.FOLD),
            2: ("Call", Action.CALL),
            3: ("Erhöhen", Action.RAISE_FOLD),
            4: ("Erhöhen (Call 3-Bet)", Action.RAISE_CALL),
            5: ("Erhöhen (All-In)", Action.RAISE_4BET_ALL_IN)
        }
    
    def generate_random_situation(self):
        """Generate a random poker situation"""
        # All 6 positions for 6-max poker
        positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
        position = random.choice(positions)
        
        # Generate random hand
        deck = Deck()
        cards = deck.deal_cards(2)
        hand = Hand(cards[0], cards[1])
        
        # Determine scenario based on position
        if position == Position.BB:
            scenarios = ["vs_btn_sb", "vs_co", "vs_mp3"]
            scenario = random.choice(scenarios)
        else:
            scenario = "first_in"
        
        return {
            "position": position,
            "hand": hand,
            "scenario": scenario
        }
    
    def get_gto_recommendation(self, hand, position, scenario):
        """Get GTO recommendation for the situation"""
        analysis = self.analyzer.analyze_preflop_hand(hand, position, scenario)
        return analysis
    
    def map_gto_to_user_actions(self, gto_action):
        """Map complex GTO actions to simplified user actions"""
        action_map = {
            Action.FOLD: [1],  # Passen
            Action.CALL: [2],  # Call
            Action.RERAISE_FOLD: [3],  # Erhöhen
            Action.RERAISE_ALL_IN: [5],  # Erhöhen (All-In)
            Action.RAISE_FOLD: [3],  # Erhöhen
            Action.RAISE_CALL: [4],  # Erhöhen (Call 3-Bet)
            Action.RAISE_4BET_FOLD: [4],  # Erhöhen (Call 3-Bet)
            Action.RAISE_4BET_ALL_IN: [5],  # Erhöhen (All-In)
            Action.CALL_IP: [2]  # Call
        }
        
        return action_map.get(gto_action, [1])  # Default to fold if unknown
    
    def get_scenario_description(self, position, scenario):
        """Get human-readable scenario description"""
        if scenario == "first_in":
            return f"Du bist {position.short_name} und es wurde noch nicht erhöht."
        elif scenario == "vs_btn_sb":
            return f"Du bist {position.short_name} und der Button/SB hat erhöht."
        elif scenario == "vs_co":
            return f"Du bist {position.short_name} und der CO hat erhöht."
        elif scenario == "vs_mp3":
            return f"Du bist {position.short_name} und MP hat erhöht."
        else:
            return f"Du bist {position.short_name}."
    
    def display_situation(self, situation):
        """Display the current situation to the user"""
        print("=" * 60)
        print("*** NEUE SPIELSITUATION ***")
        print("=" * 60)
        
        position = situation["position"]
        hand = situation["hand"]
        scenario = situation["scenario"]
        
        # Show table visualization with current position
        self.visualizer.display_compact_table(position)
        
        # Show hand
        print(f"DEINE HAND: {hand}")
        print(f"   Notation: {hand.get_hand_notation()}")
        print()
        
        # Show scenario
        print(f"SITUATION: {self.get_scenario_description(position, scenario)}")
        print()
        
        # Show action options
        print("WAS MOECHTEST DU TUN?")
        print("-" * 40)
        for num, (action_name, _) in self.action_mapping.items():
            print(f"{num}. {action_name}")
        print()
    
    def get_user_choice(self):
        """Get user's action choice"""
        while True:
            try:
                choice = int(input("Deine Wahl (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("*** Bitte waehle eine Zahl zwischen 1 und 5.")
            except ValueError:
                print("*** Bitte gib eine gueltige Zahl ein.")
    
    def evaluate_choice(self, user_choice, situation):
        """Evaluate if the user's choice was correct according to GTO"""
        hand = situation["hand"]
        position = situation["position"]
        scenario = situation["scenario"]
        
        # Get GTO recommendation
        gto_analysis = self.get_gto_recommendation(hand, position, scenario)
        gto_action_str = gto_analysis["recommended_action"]
        
        # Convert string back to Action enum
        gto_action = None
        for action in Action:
            if action.value == gto_action_str:
                gto_action = action
                break
        
        if not gto_action:
            gto_action = Action.FOLD
        
        # Get correct user actions for this GTO recommendation
        correct_choices = self.map_gto_to_user_actions(gto_action)
        
        # Check if user choice is correct
        is_correct = user_choice in correct_choices
        
        return {
            "is_correct": is_correct,
            "user_action": self.action_mapping[user_choice][0],
            "gto_action": gto_action_str,
            "gto_explanation": gto_analysis["explanation"],
            "correct_choices": [self.action_mapping[c][0] for c in correct_choices]
        }
    
    def display_result(self, evaluation, situation):
        """Display the evaluation result"""
        print("\n" + "=" * 50)
        if evaluation["is_correct"]:
            print("*** RICHTIG! ***")
            self.score["correct"] += 1
        else:
            print("*** FALSCH! ***")
        
        self.score["total"] += 1
        
        print("=" * 50)
        print()
        
        print(f"DEINE WAHL: {evaluation['user_action']}")
        print(f"GTO EMPFEHLUNG: {evaluation['gto_action']}")
        print(f"RICHTIGE AKTIONEN: {', '.join(evaluation['correct_choices'])}")
        print()
        print(f"ERKLAERUNG: {evaluation['gto_explanation']}")
        print()
        
        # Show current score
        percentage = (self.score["correct"] / self.score["total"]) * 100
        print(f"DEIN SCORE: {self.score['correct']}/{self.score['total']} ({percentage:.1f}%)")
        print()
    
    def play_round(self):
        """Play one training round"""
        # Generate situation
        situation = self.generate_random_situation()
        
        # Display situation
        self.display_situation(situation)
        
        # Get user choice
        user_choice = self.get_user_choice()
        
        # Evaluate choice
        evaluation = self.evaluate_choice(user_choice, situation)
        
        # Display result
        self.display_result(evaluation, situation)
    
    def show_welcome(self):
        """Show welcome message"""
        print("*" * 50)
        print("  POKER GTO TRAINER - INTERACTIVE MODE")
        print("*" * 50)
        print()
        print("Willkommen zum interaktiven GTO-Training!")
        print("Du bekommst zufaellige Poker-Situationen praesentiert.")
        print("Die Tischvisualisierung zeigt deine Position an.")
        print("Triff deine Entscheidung und lerne von GTO-Empfehlungen.")
        print()
        print("Kommandos:")
        print("- Waehle 1-5 fuer deine Aktion")
        print("- 'q' zum Beenden")
        print("- 'score' fuer aktuelle Statistik")
        print("- 'table' um Tisch-Info anzuzeigen")
        print()
    
    def show_final_score(self):
        """Show final score and statistics"""
        if self.score["total"] > 0:
            percentage = (self.score["correct"] / self.score["total"]) * 100
            print("\n" + "*" * 40)
            print("  FINAL SCORE")
            print("*" * 40)
            print(f"Richtige Antworten: {self.score['correct']}")
            print(f"Gesamt gespielt: {self.score['total']}")
            print(f"Erfolgsquote: {percentage:.1f}%")
            print()
            
            if percentage >= 80:
                print("*** EXCELLENT! Du verstehst GTO sehr gut!")
            elif percentage >= 60:
                print("*** GUT! Du bist auf dem richtigen Weg!")
            elif percentage >= 40:
                print("*** OK! Weiteres Training empfohlen.")
            else:
                print("*** Keep going! Uebung macht den Meister!")
            
            print("*" * 40)
    
    def run(self):
        """Main training loop"""
        self.show_welcome()
        
        try:
            while True:
                command = input("Druecke ENTER fuer neue Situation (oder 'q'/'score'/'table'): ").strip().lower()
                
                if command == 'q' or command == 'quit':
                    break
                elif command == 'score':
                    if self.score["total"] > 0:
                        percentage = (self.score["correct"] / self.score["total"]) * 100
                        print(f"*** Aktueller Score: {self.score['correct']}/{self.score['total']} ({percentage:.1f}%)")
                    else:
                        print("*** Noch keine Runden gespielt!")
                    continue
                elif command == 'table':
                    print("\n*** POKER TISCH INFORMATIONEN ***")
                    self.visualizer.display_detailed_table()
                    continue
                
                # Play a round
                self.play_round()
                
        except KeyboardInterrupt:
            print("\n\nTraining unterbrochen!")
        
        self.show_final_score()


def main():
    """Main function"""
    trainer = GTOTrainer()
    trainer.run()


if __name__ == "__main__":
    main()
