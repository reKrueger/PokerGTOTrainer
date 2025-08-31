from typing import Optional, List, Dict
from ..core import Hand, Position
from .parser import GTOChartParser
from .ranges import Action, GTORange


class GTOAnalyzer:
    """Main GTO analysis engine for preflop decisions"""
    
    def __init__(self):
        self.chart_parser = GTOChartParser()
    
    def analyze_preflop_hand(self, hand: Hand, position: Position, scenario: str = "first_in") -> Dict:
        """Analyze a preflop hand and return GTO recommendation"""
        hand_notation = hand.get_hand_notation()
        
        # Get the appropriate range
        gto_range = self._get_range_for_scenario(position, scenario)
        if not gto_range:
            return {
                "hand": hand_notation,
                "position": position.short_name,
                "scenario": scenario,
                "recommended_action": "fold",
                "explanation": f"No GTO data available for {position.short_name} in scenario {scenario}"
            }
        
        # Find the action for this hand
        recommended_action = gto_range.get_action_for_hand(hand_notation)
        if not recommended_action:
            recommended_action = Action.FOLD
        
        analysis = {
            "hand": hand_notation,
            "position": position.short_name,
            "scenario": scenario,
            "recommended_action": recommended_action.value,
            "explanation": self._get_action_explanation(recommended_action, hand_notation, position),
            "confidence": "high"  # Static for now
        }
        
        return analysis
    
    def _get_range_for_scenario(self, position: Position, scenario: str) -> Optional[GTORange]:
        """Get the appropriate GTO range for position and scenario"""
        # Map position and scenario to chart keys
        if scenario == "first_in":
            if position == Position.MP:
                return self.chart_parser.charts.get("mp3_first_in")
            elif position == Position.CO:
                return self.chart_parser.charts.get("co_first_in")
            elif position == Position.BTN:
                return self.chart_parser.charts.get("btn_first_in")
            elif position == Position.SB:
                return self.chart_parser.charts.get("sb_first_in")
        elif scenario == "vs_btn_sb" and position == Position.BB:
            return self.chart_parser.charts.get("bb_vs_btn_sb")
        elif scenario == "vs_co" and position == Position.BB:
            return self.chart_parser.charts.get("bb_vs_co")
        elif scenario == "vs_mp3" and position == Position.BB:
            return self.chart_parser.charts.get("bb_vs_mp3")
        
        return None
    
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
    
    def get_opening_range_summary(self, position: Position, scenario: str = "first_in") -> Dict:
        """Get summary of opening range for a position"""
        gto_range = self._get_range_for_scenario(position, scenario)
        if not gto_range:
            return {"error": f"No GTO data for position {position.short_name} in scenario {scenario}"}
        
        # Count hands by action
        action_counts = {}
        total_hands = 0
        
        for action, hand_range in gto_range.action_ranges.items():
            count = len(hand_range.get_all_hands())
            action_counts[action.value] = count
            total_hands += count
        
        return {
            "position": position.short_name,
            "scenario": scenario,
            "total_hands": total_hands,
            "action_breakdown": action_counts,
            "percentage": round((total_hands / 169) * 100, 1)  # 169 total possible hands
        }
    
    def get_all_available_scenarios(self) -> Dict:
        """Get all available scenarios for analysis"""
        return {
            "first_in": ["MP", "CO", "BTN", "SB"],
            "vs_btn_sb": ["BB"],
            "vs_co": ["BB"], 
            "vs_mp3": ["BB"]
        }
    
    def to_dict(self) -> dict:
        """Convert analyzer to dictionary for JSON serialization"""
        return {
            "available_scenarios": self.get_all_available_scenarios(),
            "charts": self.chart_parser.to_dict()
        }
