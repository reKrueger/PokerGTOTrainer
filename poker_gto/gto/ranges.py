from enum import Enum
from typing import Dict, List, Set, Optional
from ..core import Position, HandRange


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
    
    def to_dict(self) -> dict:
        """Convert action to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'value': self.value
        }
    
    @classmethod
    def from_string(cls, action_str: str):
        """Create action from string"""
        for action in cls:
            if action.value == action_str:
                return action
        raise ValueError(f"Invalid action: {action_str}")


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
    
    def to_dict(self) -> dict:
        """Convert GTO range to dictionary for JSON serialization"""
        return {
            'position': self.position.to_dict(),
            'scenario': self.scenario,
            'action_ranges': {
                action.value: hand_range.to_dict()
                for action, hand_range in self.action_ranges.items()
            }
        }
    
    def __str__(self) -> str:
        return f"GTO Range for {self.position} ({self.scenario}) - {len(self.action_ranges)} actions"
