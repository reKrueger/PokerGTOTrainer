from enum import Enum
from typing import Dict, List, Set, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import Position, HandRange


class Action(Enum):
    """Possible preflop actions"""
    FOLD = "fold"
    CALL = "call" 
    RAISE = "raise"
    RERAISE_ALL_IN = "reraise/all in"
    RERAISE_FOLD = "reraise/fold"
    RAISE_4BET_ALL_IN = "raise/4-bet/all in"
    RAISE_4BET_FOLD = "raise/4-bet/fold"
    RAISE_CALL = "raise/call"
    RAISE_FOLD = "raise/fold"
    CALL_IP = "call_ip"
    
    def __str__(self) -> str:
        return self.value


class GTORange:
    """Represents a GTO range for a specific position and scenario"""
    
    def __init__(self, position: Position, scenario: str = "first_in"):
        self.position = position
        self.scenario = scenario
        self.action_ranges: Dict[Action, HandRange] = {}
    
    def add_hand_to_action(self, hand_notation: str, action: Action, frequency: float = 1.0):
        """Add a hand to a specific action with frequency"""
        if action not in self.action_ranges:
            self.action_ranges[action] = HandRange()
        self.action_ranges[action].add_hand(hand_notation, frequency)
    
    def get_action_for_hand(self, hand_notation: str) -> Optional[Action]:
        """Get the recommended action for a specific hand"""
        for action, hand_range in self.action_ranges.items():
            if hand_range.get_frequency(hand_notation) > 0:
                return action
        return None
    
    def get_range_for_action(self, action: Action) -> Optional[HandRange]:
        """Get the hand range for a specific action"""
        return self.action_ranges.get(action)
    
    def get_all_actions(self) -> List[Action]:
        """Get all actions in this range"""
        return list(self.action_ranges.keys())
    
    def __str__(self) -> str:
        return f"GTO Range for {self.position} ({self.scenario}) - {len(self.action_ranges)} actions"
