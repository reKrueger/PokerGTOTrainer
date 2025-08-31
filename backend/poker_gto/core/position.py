from enum import Enum
from typing import List, Optional


class Position(Enum):
    """Poker positions for different table sizes"""
    # 6-max positions
    UTG = ("UTG", "Under The Gun", 0)
    MP = ("MP", "Middle Position", 1) 
    CO = ("CO", "Cut Off", 2)
    BTN = ("BTN", "Button", 3)
    SB = ("SB", "Small Blind", 4)
    BB = ("BB", "Big Blind", 5)
    
    def __init__(self, short_name: str, full_name: str, order: int):
        self.short_name = short_name
        self.full_name = full_name
        self.order = order
    
    def __str__(self) -> str:
        return self.short_name
    
    def is_in_position(self, opponent_position: 'Position') -> bool:
        """Check if this position acts after opponent position"""
        return self.order > opponent_position.order
    
    def to_dict(self) -> dict:
        """Convert position to dictionary for JSON serialization"""
        return {
            'short_name': self.short_name,
            'full_name': self.full_name,
            'order': self.order
        }
    
    @classmethod
    def from_string(cls, position_str: str):
        """Create position from string"""
        for position in cls:
            if position.short_name.upper() == position_str.upper():
                return position
        raise ValueError(f"Invalid position: {position_str}")


class PositionManager:
    """Manages positions for different table sizes"""
    
    SIX_MAX_POSITIONS = [
        Position.UTG, Position.MP, Position.CO,
        Position.BTN, Position.SB, Position.BB
    ]
    
    def __init__(self, max_players: int = 6):
        self.max_players = max_players
        self.positions = self._get_positions_for_table_size()
    
    def _get_positions_for_table_size(self) -> List[Position]:
        """Get appropriate positions for table size"""
        if self.max_players == 6:
            return self.SIX_MAX_POSITIONS.copy()
        else:
            # For now, only support 6-max
            raise NotImplementedError(f"Table size {self.max_players} not implemented")
    
    def get_position_by_name(self, name: str) -> Optional[Position]:
        """Get position by short name"""
        for position in self.positions:
            if position.short_name.upper() == name.upper():
                return position
        return None
    
    def get_next_position(self, current_position: Position) -> Position:
        """Get the next position in order"""
        current_index = self.positions.index(current_position)
        next_index = (current_index + 1) % len(self.positions)
        return self.positions[next_index]
    
    def to_dict(self) -> dict:
        """Convert position manager to dictionary for JSON serialization"""
        return {
            'max_players': self.max_players,
            'positions': [pos.to_dict() for pos in self.positions]
        }
