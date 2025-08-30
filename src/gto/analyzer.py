from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import Hand, Position, Table, Player
from .parser import GTOChartParser
from .ranges import Action, GTORange


class GTOAnalyzer:
    """Main GTO analysis engine for preflop decisions"""
    
    def __init__(self):
        self.chart_parser = GTOChartParser()
    
    def analyze_preflop_hand(self, hand: Hand, position: Position, scenario: str = "first_in") -> Dict:
        """Analyze a preflop hand and return GTO recommendation"""
        hand_notation = hand.get_hand_notation()
        recommended_action = self.chart_parser.get_action_for_hand(position, hand_notation, scenario)
        
        analysis = {
            "hand": hand_notation,
            "position": position.short_name,
            "scenario": scenario,
            "recommended_action": recommended_action.value,
            "explanation": self._get_action_explanation(recommended_action, hand_notation, position)
        }
        
        return analysis
    
    def _get_action_explanation(self, action: Action, hand: str, position: Position) -> str:
        """Generate explanation for the recommended action"""
        explanations = {
            Action.RAISE_4BET_ALL_IN: f"{hand} is premium - raise and go all-in if 4-bet",
            Action.RAISE_4BET_FOLD: f"{hand} is strong - raise but fold to 4-bet",
            Action.RAISE_CALL: f"{hand} can raise and call a 3-bet",
            Action.RAISE_FOLD: f"{hand} is marginal - raise but fold to 3-bet",
            Action.CALL: f"{hand} should call from {position.short_name}",
            Action.CALL_IP: f"{hand} can call in position",
            Action.RERAISE_ALL_IN: f"{hand} is premium - reraise and go all-in",
            Action.RERAISE_FOLD: f"{hand} can reraise but fold to 4-bet",
            Action.FOLD: f"{hand} should be folded from {position.short_name}"
        }
        return explanations.get(action, "No specific recommendation")
    
    def get_opening_range_summary(self, position: Position) -> Dict:
        """Get summary of opening range for a position"""
        gto_range = self.chart_parser.get_gto_range(position)
        if not gto_range:
            return {"error": f"No GTO data for position {position.short_name}"}
        
        summary = {
            "position": position.short_name,
            "total_actions": len(gto_range.get_all_actions()),
            "actions": {}
        }
        
        for action in gto_range.get_all_actions():
            hand_range = gto_range.get_range_for_action(action)
            if hand_range:
                hands = list(hand_range.get_all_hands().keys())
                summary["actions"][action.value] = {
                    "count": len(hands),
                    "hands": hands[:10] if len(hands) > 10 else hands  # Limit display
                }
        
        return summary
    
    def compare_positions(self, hand_notation: str) -> Dict:
        """Compare how the same hand should be played from different positions"""
        comparison = {
            "hand": hand_notation,
            "positions": {}
        }
        
        # Include all 6 positions
        for position in [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]:
            action = self.chart_parser.get_action_for_hand(position, hand_notation)
            comparison["positions"][position.short_name] = {
                "action": action.value,
                "explanation": self._get_action_explanation(action, hand_notation, position)
            }
        
        return comparison
    
    def analyze_table_scenario(self, table: Table) -> List[Dict]:
        """Analyze current table scenario for all players"""
        analyses = []
        
        for player in table.get_active_players():
            if player.hole_cards:
                analysis = self.analyze_preflop_hand(
                    player.hole_cards, 
                    player.position, 
                    "first_in"
                )
                analysis["player_name"] = player.name
                analyses.append(analysis)
        
        return analyses
    
    def get_quiz_hand(self, position: Position) -> Dict:
        """Generate a random hand for quiz mode"""
        import random
        
        gto_range = self.chart_parser.get_gto_range(position)
        if not gto_range:
            return {"error": "No data for this position"}
        
        # Get all hands from all actions
        all_hands = []
        for action in gto_range.get_all_actions():
            hand_range = gto_range.get_range_for_action(action)
            if hand_range:
                all_hands.extend(list(hand_range.get_all_hands().keys()))
        
        if not all_hands:
            return {"error": "No hands found"}
        
        # Pick random hand
        random_hand = random.choice(all_hands)
        correct_action = self.chart_parser.get_action_for_hand(position, random_hand)
        
        # Generate multiple choice options
        all_actions = [Action.FOLD, Action.CALL, Action.RAISE_FOLD, Action.RAISE_CALL, 
                      Action.RAISE_4BET_FOLD, Action.RAISE_4BET_ALL_IN]
        options = [correct_action]
        
        # Add some wrong options
        while len(options) < 4:
            random_action = random.choice(all_actions)
            if random_action not in options:
                options.append(random_action)
        
        random.shuffle(options)
        correct_index = options.index(correct_action)
        
        return {
            "hand": random_hand,
            "position": position.short_name,
            "question": f"What should you do with {random_hand} from {position.short_name}?",
            "options": [action.value for action in options],
            "correct_answer": correct_index,
            "explanation": self._get_action_explanation(correct_action, random_hand, position)
        }


class FlopAnalyzer:
    """Basic flop texture analysis (simplified for now)"""
    
    def __init__(self):
        pass
    
    def analyze_flop_texture(self, flop_cards: List) -> Dict:
        """Analyze flop texture - basic implementation"""
        if len(flop_cards) != 3:
            return {"error": "Need exactly 3 flop cards"}
        
        # Basic texture analysis
        ranks = [card.rank.numeric_value for card in flop_cards]
        suits = [card.suit for card in flop_cards]
        
        # Check for pairs
        has_pair = len(set(ranks)) != 3
        
        # Check for flush draw
        flush_draw = len(set(suits)) == 2
        rainbow = len(set(suits)) == 3
        
        # Check for straight draws (simplified)
        sorted_ranks = sorted(ranks)
        straight_draw = False
        if sorted_ranks[2] - sorted_ranks[0] <= 4:  # Within 4 rank gap
            straight_draw = True
        
        texture_type = "Unknown"
        if has_pair:
            texture_type = "Paired"
        elif rainbow and not straight_draw:
            texture_type = "Dry"
        elif flush_draw or straight_draw:
            texture_type = "Wet"
        else:
            texture_type = "Medium"
        
        return {
            "flop": [str(card) for card in flop_cards],
            "texture_type": texture_type,
            "has_pair": has_pair,
            "flush_draw": flush_draw,
            "straight_draw": straight_draw,
            "rainbow": rainbow
        }
