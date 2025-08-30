from enum import Enum
import random
from typing import List, Optional


class Suit(Enum):
    """Card suits"""
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"


class Rank(Enum):
    """Card ranks with numeric values for comparison"""
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "T")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    
    def __init__(self, numeric_value: int, symbol: str):
        self.numeric_value = numeric_value
        self.symbol = symbol
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.numeric_value < other.numeric_value
        return NotImplemented
    
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.numeric_value <= other.numeric_value
        return NotImplemented



class Card:
    """Represents a single playing card"""
    
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self) -> str:
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank.name}, {self.suit.name})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    
    def __hash__(self) -> int:
        return hash((self.rank, self.suit))


class Deck:
    """Represents a deck of 52 playing cards"""
    
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        """Reset deck to full 52 cards and shuffle"""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        self.shuffle()
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def deal_card(self) -> Optional[Card]:
        """Deal one card from the deck"""
        if self.cards:
            return self.cards.pop()
        return None
    
    def deal_cards(self, count: int) -> List[Card]:
        """Deal multiple cards from the deck"""
        dealt_cards = []
        for _ in range(count):
            card = self.deal_card()
            if card:
                dealt_cards.append(card)
            else:
                break
        return dealt_cards
    
    def cards_remaining(self) -> int:
        """Return number of cards remaining in deck"""
        return len(self.cards)
    
    def __str__(self) -> str:
        return f"Deck with {len(self.cards)} cards remaining"
