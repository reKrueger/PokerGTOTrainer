"""
Poker Table Model
================

Data structure for poker table state including:
- Player positions and information
- Community cards (Flop, Turn, River)
- Betting information
- Game state
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


class TableStage(Enum):
    """Current stage of the poker hand"""
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class BetType(Enum):
    """Types of betting actions"""
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"


@dataclass
class Card:
    """Represents a playing card"""
    rank: str  # A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
    suit: str  # H, D, C, S
    
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"
    
    def to_display(self) -> str:
        """Get display representation with emoji suits"""
        suit_emojis = {'H': '♥️', 'D': '♦️', 'C': '♣️', 'S': '♠️'}
        return f"{self.rank}{suit_emojis.get(self.suit, self.suit)}"


@dataclass
class PlayerInfo:
    """Information about a player at the table"""
    position: str  # UTG, MP, CO, BTN, SB, BB
    name: str
    stack: float
    current_bet: float = 0.0
    last_action: Optional[BetType] = None
    is_active: bool = True
    is_current_player: bool = False
    hole_cards: Optional[List[Card]] = None
    
    def get_bet_display(self) -> str:
        """Get formatted bet display"""
        if self.current_bet == 0:
            return ""
        elif self.current_bet < 1.0:
            return f"{self.current_bet:.1f}x"
        else:
            return f"{self.current_bet:.0f}x"


@dataclass 
class CommunityCards:
    """Community cards on the board"""
    flop: List[Card] = None
    turn: Optional[Card] = None
    river: Optional[Card] = None
    
    def __post_init__(self):
        if self.flop is None:
            self.flop = []
    
    def get_all_cards(self) -> List[Card]:
        """Get all community cards as a list"""
        cards = self.flop.copy()
        if self.turn:
            cards.append(self.turn)
        if self.river:
            cards.append(self.river)
        return cards
    
    def get_stage(self) -> TableStage:
        """Determine current table stage based on community cards"""
        if not self.flop:
            return TableStage.PREFLOP
        elif not self.turn:
            return TableStage.FLOP
        elif not self.river:
            return TableStage.TURN
        else:
            return TableStage.RIVER


class PokerTableModel:
    """
    Model class for poker table state management
    
    Handles:
    - Player positions and information
    - Community cards (Flop, Turn, River)
    - Betting rounds and pot sizes
    - Current game state
    """
    
    def __init__(self, max_players: int = 6):
        self.max_players = max_players
        self.players: Dict[str, PlayerInfo] = {}
        self.community_cards = CommunityCards()
        self.pot_size: float = 0.0
        self.current_stage = TableStage.PREFLOP
        self.current_player_position: Optional[str] = None
        self.dealer_position: str = "BTN"
        
        # Standard 6-max positions in order
        self.positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        
        # Initialize empty seats
        self._initialize_seats()
    
    def _initialize_seats(self):
        """Initialize all seats as empty"""
        for position in self.positions:
            self.players[position] = PlayerInfo(
                position=position,
                name="",
                stack=0.0,
                is_active=False
            )
    
    def add_player(self, position: str, name: str, stack: float = 100.0):
        """Add a player to specific position"""
        if position not in self.positions:
            raise ValueError(f"Invalid position: {position}")
        
        self.players[position] = PlayerInfo(
            position=position,
            name=name,
            stack=stack,
            is_active=True
        )
    
    def remove_player(self, position: str):
        """Remove player from position"""
        if position in self.players:
            self.players[position].is_active = False
            self.players[position].name = ""
            self.players[position].stack = 0.0
    
    def set_current_player(self, position: str):
        """Set the current acting player"""
        # Clear previous current player
        for player in self.players.values():
            player.is_current_player = False
        
        # Set new current player
        if position in self.players:
            self.players[position].is_current_player = True
            self.current_player_position = position
    
    def set_player_action(self, position: str, action: BetType, bet_amount: float = 0.0):
        """Set player's action and bet amount"""
        if position in self.players:
            self.players[position].last_action = action
            self.players[position].current_bet = bet_amount
    
    def set_community_cards(self, flop: List[Card] = None, turn: Card = None, river: Card = None):
        """Set community cards"""
        if flop:
            self.community_cards.flop = flop
        if turn:
            self.community_cards.turn = turn
        if river:
            self.community_cards.river = river
        
        # Update current stage
        self.current_stage = self.community_cards.get_stage()
    
    def set_flop(self, cards: List[Card]):
        """Set flop cards"""
        if len(cards) != 3:
            raise ValueError("Flop must have exactly 3 cards")
        self.community_cards.flop = cards
        self.current_stage = TableStage.FLOP
    
    def set_turn(self, card: Card):
        """Set turn card"""
        self.community_cards.turn = card
        self.current_stage = TableStage.TURN
    
    def set_river(self, card: Card):
        """Set river card"""
        self.community_cards.river = card
        self.current_stage = TableStage.RIVER
    
    def get_active_players(self) -> List[PlayerInfo]:
        """Get list of active players"""
        return [player for player in self.players.values() if player.is_active]
    
    def get_player_by_position(self, position: str) -> Optional[PlayerInfo]:
        """Get player by position"""
        return self.players.get(position)
    
    def update_pot(self, amount: float):
        """Update pot size"""
        self.pot_size = amount
    
    def reset_betting_round(self):
        """Reset betting for new round"""
        for player in self.players.values():
            player.current_bet = 0.0
            player.last_action = None
    
    def reset_hand(self):
        """Reset for new hand"""
        self.community_cards = CommunityCards()
        self.current_stage = TableStage.PREFLOP
        self.pot_size = 0.0
        self.current_player_position = None
        
        # Reset player states
        for player in self.players.values():
            player.current_bet = 0.0
            player.last_action = None
            player.is_current_player = False
            player.hole_cards = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for serialization"""
        return {
            "max_players": self.max_players,
            "positions": self.positions,
            "current_stage": self.current_stage.value,
            "current_player": self.current_player_position,
            "dealer_position": self.dealer_position,
            "pot_size": self.pot_size,
            "players": {
                pos: {
                    "position": player.position,
                    "name": player.name,
                    "stack": player.stack,
                    "current_bet": player.current_bet,
                    "last_action": player.last_action.value if player.last_action else None,
                    "is_active": player.is_active,
                    "is_current_player": player.is_current_player
                }
                for pos, player in self.players.items()
            },
            "community_cards": {
                "flop": [str(card) for card in self.community_cards.flop],
                "turn": str(self.community_cards.turn) if self.community_cards.turn else None,
                "river": str(self.community_cards.river) if self.community_cards.river else None
            }
        }
    
    def __str__(self) -> str:
        active_count = len(self.get_active_players())
        return f"PokerTable({active_count}/{self.max_players} players, {self.current_stage.value}, pot: {self.pot_size})"
