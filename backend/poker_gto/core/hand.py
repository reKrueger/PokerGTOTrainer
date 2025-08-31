from typing import List, Tuple, Optional
from .deck import Card, Rank


class Hand:
    """Represents a poker hand with two hole cards"""
    
    def __init__(self, card1: Card, card2: Card):
        self.card1 = card1
        self.card2 = card2
        # Sort cards by rank for consistency (higher rank first)
        if card2.rank.numeric_value > card1.rank.numeric_value:
            self.card1, self.card2 = card2, card1
    
    def is_suited(self) -> bool:
        """Check if both cards are of the same suit"""
        return self.card1.suit == self.card2.suit
    
    def is_pair(self) -> bool:
        """Check if hand is a pocket pair"""
        return self.card1.rank == self.card2.rank
    
    def get_hand_notation(self) -> str:
        """Get standard poker hand notation (e.g., 'AKs', 'QQ', 'T9o')"""
        rank1_symbol = self.card1.rank.symbol
        rank2_symbol = self.card2.rank.symbol
        
        if self.is_pair():
            return f"{rank1_symbol}{rank2_symbol}"
        else:
            suited_indicator = "s" if self.is_suited() else "o"
            return f"{rank1_symbol}{rank2_symbol}{suited_indicator}"
    
    def get_cards(self) -> Tuple[Card, Card]:
        """Get the two cards as a tuple"""
        return (self.card1, self.card2)
    
    def to_dict(self) -> dict:
        """Convert hand to dictionary for JSON serialization"""
        return {
            'card1': self.card1.to_dict(),
            'card2': self.card2.to_dict(),
            'notation': self.get_hand_notation(),
            'is_suited': self.is_suited(),
            'is_pair': self.is_pair()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create hand from dictionary"""
        card1 = Card.from_dict(data['card1'])
        card2 = Card.from_dict(data['card2'])
        return cls(card1, card2)
    
    def __str__(self) -> str:
        return f"{self.card1} {self.card2} ({self.get_hand_notation()})"
    
    def __repr__(self) -> str:
        return f"Hand({self.card1}, {self.card2})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Hand):
            return (self.card1 == other.card1 and self.card2 == other.card2) or \
                   (self.card1 == other.card2 and self.card2 == other.card1)
        return False
    
    def __hash__(self) -> int:
        cards = sorted([self.card1, self.card2], key=lambda c: (c.rank.numeric_value, c.suit.value))
        return hash((cards[0], cards[1]))


class HandRange:
    """Represents a range of poker hands with frequencies"""
    
    def __init__(self):
        self.hands: dict[str, float] = {}  # hand_notation -> frequency
    
    def add_hand(self, hand_notation: str, frequency: float = 1.0):
        """Add a hand to the range with given frequency (0.0 to 1.0)"""
        if 0.0 <= frequency <= 1.0:
            self.hands[hand_notation] = frequency
        else:
            raise ValueError("Frequency must be between 0.0 and 1.0")
    
    def remove_hand(self, hand_notation: str):
        """Remove a hand from the range"""
        self.hands.pop(hand_notation, None)
    
    def get_frequency(self, hand_notation: str) -> float:
        """Get frequency for a specific hand"""
        return self.hands.get(hand_notation, 0.0)
    
    def get_all_hands(self) -> dict[str, float]:
        """Get all hands in the range with their frequencies"""
        return self.hands.copy()
    
    def is_empty(self) -> bool:
        """Check if range is empty"""
        return len(self.hands) == 0
    
    def to_dict(self) -> dict:
        """Convert hand range to dictionary for JSON serialization"""
        return {
            'hands': self.hands,
            'hand_count': len(self.hands)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create hand range from dictionary"""
        hand_range = cls()
        hand_range.hands = data['hands']
        return hand_range
    
    def __str__(self) -> str:
        if self.is_empty():
            return "Empty range"
        return f"Range with {len(self.hands)} hands"
